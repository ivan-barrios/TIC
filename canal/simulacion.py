import numpy as np
from operaciones import corregir_error, detectar_error
from modeloTransmision import canal_awgn_bpsk
from generacionMatrices import G, H, k, n

############################################################################################################################################################
def simular_ber_wer_corrector(EbN0_dB_vals, A=1, repeticiones=1, M=1_000_000):
    """
    simula BER y WER con codigo corrector de errores.

    parametros:
    - EbN0_dB_vals: arreglo con valores de Eb/N0 en dB
    - A: amplitud de la señal BPSK (default = 1.0)
    - repeticiones: cantidad de repeticiones por punto (default = 1)
    - M: cantidad de palabras aleatorias por repetición (default = 1.000.000)

    Retorna:
    - ber: lista de tasas de error de bit estimadas
    - wer: lista de tasas de error de palabra estimadas
    """

    HT = H.T
    ber = []
    wer = []

    for EbN0_dB in EbN0_dB_vals:
        EbN0 = 10 ** (EbN0_dB / 10) # paso a valor lineal

        errores_bits_tot = 0
        errores_pal_tot = 0
        total_bits = 0
        total_palabras = 0

        

        for _ in range(repeticiones):
            # genero mensajes de fuente aleatorio y codifico
            U = np.random.randint(0, 2, size=(M, k))
            V = (U @ G) % 2

            # transmito por canal AWGN con BPSK (se suma ruido y tomamos decisión dura)
            VR = canal_awgn_bpsk(V, A, k, n, EbN0)

            # calculo síndromes y corrijo errores
            S = (VR @ HT) % 2
            VE = corregir_error(VR, S, HT)
            Ue = VE[:, :k]

            # Contar errores
            errores_bits_tot += np.sum(U != Ue)
            errores_pal_tot += np.sum(np.any(U != Ue, axis=1))
            total_bits += M * k
            total_palabras += M

        ber.append(errores_bits_tot / total_bits)
        wer.append(errores_pal_tot / total_palabras)

    return ber, wer
############################################################################################################################################################
def simular_ber_wer_detector(EbN0_dB_vals, A=1, repeticiones=1, M=1_000_000):
    """
    simula BER y WER con codigo detector de errores.
    Las palabras con errores detectados son descartadas antes de comparar.

    Retorna:
    - ber: lista de BER sobre palabras válidas
    - wer: lista de WER = fracción de palabras descartadas
    """
    HT = H.T
    ber = []
    wer = []

    for EbN0_dB in EbN0_dB_vals:
        EbN0 = 10**(EbN0_dB / 10)

        errores_bits_totales = 0
        palabras_descartadas = 0
        total_bits_validos = 0

        for _ in range(repeticiones):
            # Fuente y codificación
            U = np.random.randint(0, 2, size=(M, k))
            V = (U @ G) % 2

            # canal
            VR = canal_awgn_bpsk(V, A, k, n, EbN0)

            # Detección de errores => se descartan las palabras con errores detectados
            VR_validas, idx_validas = detectar_error(VR, HT)
            U_validas = U[idx_validas]
            Ue = VR_validas[:, :k]  # decodificación sistemática

            # metricas
            errores_bits_totales += np.sum(U_validas != Ue)
            total_bits_validos += U_validas.size
            palabras_descartadas += M - len(idx_validas)

        ber.append(errores_bits_totales / total_bits_validos if total_bits_validos > 0 else 0)
        wer.append(palabras_descartadas / (M * repeticiones))

    return ber, wer
import numpy as np
from graficos import Qinv

#####################################################################################
def corregir_error(R, S, HT):
    """
    Corrige 1 error en palabras recibidas usando el síndrome.

    Retorna:
    - CR: matriz corregida de palabras recibidas (M x n)
    """
    CR = R.copy() # genero copia de la palabra recibida para corregir
    for j in range(S.shape[0]):  # para cada palabra recibida
        s = S[j]  # síndrome de la palabra j
        if not np.all(s == 0):  # si el síndrome no es el vector nulo, hubo error
            for i in range(HT.shape[0]):  # buscar en qué fila de HT aparece
                if np.array_equal(s, HT[i]):
                    # corregir el bit i de la palabra j
                    CR[j, i] = 1 - CR[j, i]
                    break  # corregido, salgo del for
    return CR
#####################################################################################
def detectar_error(VR, HT):
    """
    detecta errores en palabras recibidas usando el síndrome.
    devuelve las palabras validas (síndrome nulo) y sus índices.

    parametros:
    - VR: matriz M x n de palabras recibidas (decisión dura)
    - HT: transpuesta de la matriz de control de paridad H (n x (n-k))

    retorna:
    - VR_validas: submatriz de VR con palabras validas (sin errores detectados)
    - idx_validas: indices de las palabras validas (en VR)
    """
    S = (VR @ HT) % 2  # síndrome
    idx_validas = np.where(~np.any(S != 0, axis=1))[0] #indices de las palabras con síndrome nulo
    VR_validas = VR[idx_validas]
    return VR_validas, idx_validas
#####################################################################################
def calcular_ganancia_real_por_punto(EbN0_dB_vals, ber_simulada):
    """
    calcula ganancia real para cada punto de Eb/N0 dado.
    compara con la curva teórica sin codificación.
    Retorna:
    - ganancia_real: lista de ganancia real en dB para cada Eb/N0
    """

    EbN0_dB_vals = np.array(EbN0_dB_vals)
    ganancia_real = []

    for i, BER_sim in enumerate(ber_simulada):
        # si BER_sim > 0.5 (inútil), ganancia 0
        if BER_sim <= 0 or BER_sim >= 0.5:
            ganancia_real.append(0)
            continue

        # encuentro Eb/N0 teórico necesario para obtener esa BER
        Qinv_arg = Qinv(BER_sim)
        EbN0_teorico_lineal = (Qinv_arg ** 2) / 2
        EbN0_teorico_dB = 10 * np.log10(EbN0_teorico_lineal)

        # resto Eb/N0 actual para obtener la ganancia
        ganancia = EbN0_teorico_dB - EbN0_dB_vals[i]
        ganancia_real.append(ganancia) #en dB

    return np.array(ganancia_real)
#####################################################################################

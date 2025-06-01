import numpy as np
from simulacion import simular_ber_wer_corrector, simular_ber_wer_detector
from enum import Enum
from graficos import graficar_ber_wer, graficar_ganancia_vs_ebn0
from operaciones import calcular_ganancia_real_por_punto
from generacionMatrices import ganancia_asintotica

class ModoSimulacion(Enum):
    CORRECTOR = 1
    DETECTOR = 2

modo = ModoSimulacion.CORRECTOR # cambiar a ModoSimulacion.DETECTOR para simular con detector de errores

if (modo == ModoSimulacion.CORRECTOR):
    A=1
    EbN0_dB_vals = np.arange(0, 11)  # de 0 a 10 dB

    ber, wer = simular_ber_wer_corrector(EbN0_dB_vals, A, repeticiones=1, M=1_000_000)

    graficar_ber_wer(EbN0_dB_vals, ber, wer, titulo="Resultados como corrector de errores")
    
    ganancia_real_puntos = calcular_ganancia_real_por_punto(EbN0_dB_vals, ber)

    graficar_ganancia_vs_ebn0(EbN0_dB_vals, ganancia_real_puntos, ganancia_asintotica)


elif (modo == ModoSimulacion.DETECTOR):
    A=1
    EbN0_dB_vals = np.arange(0, 11)  # de 0 a 10 dB

    ber, wer = simular_ber_wer_detector(EbN0_dB_vals, A, repeticiones=1, M=1_000_000)

    graficar_ber_wer(EbN0_dB_vals, ber, wer, titulo="Resultados como detector de errores")
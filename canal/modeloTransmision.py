import numpy as np

def canal_awgn_bpsk(V, A, k, n, EbfN0):
    """
    simula el canal AWGN para una palabra de código BPSK.
    
    parámetros:
    - v: palabra de código binaria (numpy array de 0s y 1s, longitud n)
    - A: amplitud de la señal BPSK
    - k: longitud de la palabra fuente
    - n: longitud de la palabra de código
    - EbfN0: relación Eb/N0 (escalar, valor lineal, no en dB)
    - r: señal recibida (compleja)

    retorna:
    - vr: decisión dura (bits estimados)
    """
    Es = A**2
    Ebf = Es * n / k
    N0 = Ebf / EbfN0

    # Modulamos con BPSK
    S = (2 * V - 1) * A

    # Ruido complejo
    ruido = np.sqrt(N0 / 2) * (np.random.randn(*V.shape) + 1j * np.random.randn(*V.shape))

    # Señal recibida
    R = S + ruido

    # Detección dura (solo parte real)
    vr = (np.real(R) > 0).astype(int)
    
    return vr
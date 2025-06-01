import matplotlib.pyplot as plt
from scipy.special import erfc
import numpy as np

########################################################################
def Q(x):
    return 0.5 * erfc(x / np.sqrt(2))
def Qinv(y):
    """Inversa aproximada de la función Q, válida para y ∈ (0, 0.5)"""
    from scipy.special import erfcinv
    return np.sqrt(2) * erfcinv(2*y)
########################################################################
def graficar_ber_wer(EbN0_dB_vals, ber, wer, titulo):
    EbN0_linear = 10**(np.array(EbN0_dB_vals) / 10)
    ber_teorica = Q(np.sqrt(2 * EbN0_linear))

    plt.figure(figsize=(10, 5))
    plt.semilogy(EbN0_dB_vals, ber, 'o-', label='BER codificado')
    plt.semilogy(EbN0_dB_vals, wer, 's-', label='WER codificado')
    plt.semilogy(EbN0_dB_vals, ber_teorica, 'k--', label='BER sin codificación (teórica)')
    plt.xlabel('$E_b/N_0$ [dB]')
    plt.ylabel('Probabilidad de error')
    plt.title(titulo)
    plt.grid(True, which='both', linestyle='--')
    plt.legend()
    plt.tight_layout()
    plt.show()
########################################################################
def graficar_ganancia_vs_ebn0(EbN0_dB_vals, ganancia_real, ganancia_asintotica):
    plt.figure(figsize=(8, 4))
    plt.plot(EbN0_dB_vals, ganancia_real, label="Ganancia Real", marker='o')
    plt.axhline(ganancia_asintotica, color='red', linestyle='--', label="Ganancia Asintótica")

    plt.xlabel('$E_b/N_0$ [dB]')
    plt.ylabel('Ganancia [dB]')
    plt.title('Ganancia real y asintótica en función de $E_b/N_0$')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()
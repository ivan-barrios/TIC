import numpy as np
import math
from itertools import combinations

########################################################################
def generar_matrices_14_10_corrector():
    """
    genera matrices G y H para el codigo (14,10).
    necesitamos dmin>=3 ya que queremos corregir 1 error (tc=1 como maximo para (14,10))

    Retorna:
    - G: matriz generadora de dimensiones (10,14)
    - H: matriz de control de paridad de dimensiones (4,14)
    """

    # identidad 10x10
    I10 = np.identity(10, dtype=int)

    # paridad P 10x4 hecha tal que dmin>=3
    P = np.array([
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 1, 1],
        [1, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [1, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1]
    ], dtype=int)

    # G = [I10 | P]
    G = np.concatenate((I10, P), axis=1)
    
    # H = [P.T | I_4]
    PT = P.T
    I4 = np.identity(4, dtype=int)
    H = np.concatenate((PT, I4), axis=1)

    return G, H
########################################################################

########################################################################
def calcular_cant_corr_dect(H):
    """
    calcula la cantidad de errores que puede corregir y detectar el codigo
    ademas de la distancia minima del codigo.
    Retorna:
    - d_min: distancia minima del codigo
    - td: cantidad de errores que puede corregir
    - tc: cantidad de errores que puede detectar
    """
    HT = H.T
    m = HT.shape[0]

    #m=cantidad de filas de H
    #k=cantidad de filas actual
    #filas contiene la combinacion de filas actual
    #suma contiene la suma de las filas seleccionadas
    
    for k in range(2, m+1):  # recorremos desde 2 filas como minimo hasta m+1 filas
        for filas in combinations(range(m), k): # todas las combinaciones de filas posibles
            suma = np.sum(HT[list(filas)], axis=0) % 2 #sumamos todas las filas seleccionadas
            if np.all(suma == 0): #me fijo si la suma es el vector cero
                d_min = k
                td = d_min - 1
                tc = (d_min - 1) // 2 #redondeo hacia abajo (//division entera)
                return {
                    "d_min": d_min,
                    "td": td,
                    "tc": tc,
                }
    return None  # no se encontró combinación
########################################################################
########################################################################
#matrices Generadora y de control de paridad G y H
G, H = generar_matrices_14_10_corrector()
k= G.shape[0]  # cantidad de filas de G
n= G.shape[1]  # cantidad de columnas de G

# cantidad de errores que puede corregir y detectar
cant_corr_dect = calcular_cant_corr_dect(H)
d_min = cant_corr_dect['d_min']
td = cant_corr_dect['td']
tc = cant_corr_dect['tc']

#ganancia de codificacion asintotica
ganancia_asintotica = (k/n) * math.floor((d_min + 1) / 2)

print(f"d_min: {d_min}")
print(f"td: {td}")
print(f"tc: {tc}")
########################################################################

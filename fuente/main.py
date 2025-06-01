import numpy as np
from collections import Counter
from PIL import Image

####################################################################
def obtener_fuente():
    img = Image.open("logo FI.tif").convert("1")  # binaria
    return np.array(img).flatten() * 1  # True/False a 0/1

####################################################################
def agrupar_fuente(data, orden):
    padding = 0
    if len(data) % orden != 0:
        padding = orden - (len(data) % orden)
    if padding:
        data = np.append(data, [0]*padding)  # relleno con ceros
    data_agrupada = data.reshape(-1, orden)
    return ["".join(map(str, grupo)) for grupo in data_agrupada]

####################################################################
def construir_huffman(probabilidades):
    """
    construye un diccionario Huffman símbolo → código
    """
    # inicializo lista de nodos: cada nodo es (probabilidad, [símbolos])
    nodos = [(p, [s]) for s, p in sorted(probabilidades.items(), key=lambda x: x[1])]

    # inicializo codigos vacíos
    codigos = {s: '' for s in probabilidades}

    while len(nodos) > 1:
        # Tomar dos nodos con menor probabilidad
        (p1, s1), (p2, s2) = nodos[0], nodos[1]

        # asigno bits
        for s in s1:
            codigos[s] = '0' + codigos[s]
        for s in s2:
            codigos[s] = '1' + codigos[s]

        # fusiono los dos nodos
        nuevo_nodo = (p1 + p2, s1 + s2)

        # reemplazo los dos nodos por el nuevo
        nodos = nodos[2:]
        nodos.append(nuevo_nodo)
        nodos.sort(key=lambda x: x[0])  # ordeno por probabilidad

    return codigos

####################################################################
def calcular_largo_promedio(probabilidades, codigos_huffman):
    return sum(probabilidades[s] * len(codigos_huffman[s]) for s in probabilidades)

####################################################################
def procesar_fuente(data, orden):
    fuente = agrupar_fuente(data, orden)
    total = len(fuente)
    conteo = Counter(fuente)
    probabilidades = {s: c / total for s, c in conteo.items()}
    codigos = construir_huffman(probabilidades)
    largo_promedio = calcular_largo_promedio(probabilidades, codigos) / orden
    tasa = 1 / largo_promedio
    return largo_promedio, tasa, codigos

####################################################################
def mostrar_codigos_huffman(codigos_huffman):
    print("Códigos de Huffman por símbolo:")
    for simbolo in sorted(codigos_huffman.keys()):
        print(f"  {simbolo} → {codigos_huffman[simbolo]}")
####################################################################
def main():
    data = obtener_fuente()

    for orden in [2, 3]:
        L, tasa, codigos = procesar_fuente(data, orden)
        print(f"Orden {orden}:")
        print(f"  - Largo promedio: {L:.4f} bits/símbolo")
        print(f"  - Tasa de compresión: {tasa:.4f}")
        mostrar_codigos_huffman(codigos)
        print()


#=========================#
if __name__ == "__main__":
    main()

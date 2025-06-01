# Simulación y Análisis de Códigos de Bloque (14,10) en Canal AWGN

Este repositorio contiene el desarrollo de un trabajo práctico para la materia **Teoría de la Información y Codificación**, en el que se implementan y evalúan códigos de bloque binarios sobre canales ruidosos (AWGN), utilizando modulación BPSK. Se simulan tanto escenarios con **corrección de errores** como con **detección de errores**, y además se realiza una compresión de fuente utilizando **codificación de Huffman** sobre una imagen binaria.

---

## 📌 Objetivos

- Implementar un sistema transmisor-receptor con un código (14,10) de bloques.
- Evaluar el desempeño del sistema bajo diferentes condiciones de ruido (Eb/N0).
- Comparar resultados simulados con resultados teóricos.
- Estimar **ganancia de codificación** (real y asintótica).
- Implementar **detección de errores** sin retransmisión.
- Aplicar **compresión de fuente** sobre una imagen binaria utilizando Huffman para fuente extendida de orden 2 y 3.

---


## ⚙️ Cómo ejecutar

1. Asegurarse de tener las dependencias instaladas:
```bash
pip install numpy matplotlib pillow scipy
```

2. Ejecutar simulación para corrector:
### En la carpeta /canal
```python
modo = ModoSimulacion.CORRECTOR
```
```bash
python main.py
```
3. Ejecutar simulación para detector:
### En la carpeta /canal
```python
modo = ModoSimulacion.DETECTOR
```
```bash
python main.py
```

4. Ejecutar compresión de fuente:
### En la carpeta /fuente
```bash
python main.py
```

## 📈 Resultados

- **Curvas BER y WER** simuladas vs. teoría sin codificación.
- **Ganancia real** del código frente a **ganancia asintótica**.
- Para el modo **detector**, se aclara que no se considera retransmisión: las palabras con errores detectados son descartadas sin reenvío.
- **Compresión Huffman** con orden 2 y 3, mostrando el largo promedio por símbolo y la tasa de compresión obtenida.

---

## 📌 Notas importantes

- El código detector filtra las palabras erróneas, lo que puede **subestimar la BER** ya que solo se computa sobre palabras "aceptadas".
- En todos los experimentos se trabaja con bloques aleatorios de 1.000.000 de palabras por punto Eb/N0 para garantizar consistencia estadística.

# Características Estadísticas de Secuencias de Multiplicadores Crash: Un Estudio de Simulación de Monte Carlo Basado en Un Millón de Rondas Sintéticas

[![License: MIT](https://shields.io)](https://opensource.org)
[![Python Version](https://shields.io)](https://python.org)
[![Dataset Size](https://shields.io)](#2-dataset-specification--schema)
[![Academic Status](https://shields.io)](#9-limitations)

---

### 🌐 Lea esta documentación en otros idiomas / Read This Documentation in Other Languages

| [🇺🇸 English](README.md) | [🇧🇷 Português (Brasil)](README_pt.md) | [🇪🇸 Español (LATAM) (Actual)](README_es.md) | [🇮🇳 हिन्दी (India)](README_hi.md) |
| :--- | :--- | :--- | :--- |

---

> 📊 **Portal Oficial de Investigación:** Lea el artículo teórico completo, las visualizaciones estadísticas y el análisis econométrico extendido en nuestra plataforma verificada: **[https://www.mcjychina.com](https://www.mcjychina.com/crash-multiplier-study)**

---

Este repositorio contiene el pipeline de código abierto completo, scripts de generación de datos reproducibles, marcos matemáticos y activos de visualización para analizar las propiedades estadísticas de series temporales de multiplicadores seudoaleatorios de tipo crash.

## Resumen
Esta investigación presenta un análisis estadístico de secuencias de multiplicadores crash utilizando un conjunto de datos sintético que contiene **1,000,000 de rondas simuladas** generadas a través de un marco de simulación de Monte Carlo. El estudio investiga: características de la distribución de multiplicadores; patrones de dependencia secuencial; comportamiento estadístico móvil; y características de volatilidad. El objetivo de esta investigación no es predecir resultados futuros, sino analizar las propiedades estadísticas observables dentro de un proceso aleatorio simulado de tipo crash.

El análisis demuestra que las secuencias de multiplicadores crash exhiben una distribución altamente asimétrica hacia la derecha (right-skewed), donde los resultados de multiplicadores bajos dominan la frecuencia histórica (64.66% entre 1x-2x), mientras que los eventos de multiplicadores extremos contribuyen exponencialmente a la varianza global.

---

## 1. Estructura de Directorios del Proyecto
```text
.
├── data/
│   └── raw/
│       └── crash_dataset.csv
├── generator/
│   └── simulator.py
├── validator/
│   └── validator.py
├── analysis/
│   ├── distribution.py
│   ├── timeseries.py
│   └── volatility.py
├── report/
│   ├── generate_report.py
│   └── templates/
├── output/
│   └── article.md
├── metadata/
│   └── dataset.json
├── run_pipeline.py
└── visualize_crash_study.py
```

---

## 2. Especificación y Esquema del Conjunto de Dados

El esquema de telemetría subyacente evalúa observaciones secuenciales bajo un patrón de ventana fija estandarizado:

| Parámetro         | Valor                         |
| :---------------- | :---------------------------- |
| **Total de Muestras** | 1,000,000                     |
| **Tipo de Datos**     | Conjunto de Datos de Series Temporales Sintéticas |
| **Motor de Generación** | Marco de Monte Carlo por Partes |
| **Delta Temporal**| Δ t = 15 segundos |

### Diccionario de Campos de Columnas
* `round_id` (int): Incremento numérico secuencial que actúa como clave primaria.
* `timestamp` (ISO-8601 String): Marcador cronológico de transacciones (\(\Delta t = 15s\)).
* `session_id` (int): Agrupación categórica de lotes (1,000 rondas por sesión).
* `crash_point` (float): Variable dependiente que representa el multiplicador final de la ronda.
* `previous_crash_1` / `previous_crash_2` (float): Características de rezago temporal directo (\(X_{t-1}, X_{t-2}\)).
* `previous_crash_5_avg` (float): Media aritmética móvil de corto plazo (\(N=5\)).
* `rolling_mean_20` / `rolling_std_20` (float): Indicadores estadísticos móviles estructurales (\(N=20\)).

---

## 3. Marco Matemático y Distribución

El comportamiento aleatorio continuo de la variable del multiplicador crash final \(X\) utiliza una **Distribución Uniforme por Partes** de cuatro niveles. Dado un generador independiente \(r \sim \mathcal{U}(0, 1)\), \(X\) se mapea incondicionalmente a través de:

\[X = \begin{cases}   \mathcal{U}(1, 2) & \text{si } 0 \le r < 0.65 \\  \mathcal{U}(2, 10) & \text{si } 0.65 \le r < 0.95 \\  \mathcal{U}(10, 50) & \text{si } 0.95 \le r < 0.99 \\  \mathcal{U}(50, 500) & \text{si } 0.99 \le r \le 1.00   \end{cases}\]

### Aviso de Optimización Estructural (Prevención de Filtración de Datos)
> ⚠️ **Sin Sesgo de Anticipación (Look-Ahead Bias):** A diferencia de las implementaciones ingenuas que llenan incorrectamente los índices iniciales con valores futuros (\(X_t\)), este script impone un búfer de inicialización estricto. Los índices donde \(t < \text{ventana}\) devuelven tipos nulos explícitos (`NaN`). Esta cuarentena matemática garantiza que ningún modelo predictivo pueda cosechar filtraciones de la variable objetivo a través de las características móviles.
>
> ⚙️ **Modificación de los Grados de Libertad:** Los cálculos de variación móvil utilizan la aproximación de varianza muestral insesgada local (Corrección de Bessel vía \(\Delta \text{DOF}=1\)), alineándose con la metodología estadística estándar.

---

## 4. Hallazgos Estadísticos Empíricos

* **Dispersión de Cola Pesada (Heavy-Tail):** Aunque los sucesos de 10x+ representan apenas el **4.99%** de las frecuencias globales, elevan la media aritmética global a **6.7043x**, creando una fuerte asimetria con respecto a la mediana global de **1.77x**.
* **Autocorrelación Temporal Nula:** La autocorrelación Lag-1 se sitúa en \(r = 0.00083\). Esto demuestra que las secuencias históricas operan de manera independiente, verificando que las tendencias pasadas no ofrecen ninguna ventaja estadística para predecir resultados futuros.
* **Índice de Volatilidad Masivo:** El sistema produce una Desviación Estándar Global (\(\sigma\)) de 30.4411 y un Coeficiente de Variación (\(CV\)) de 4.5405. Dado que \(CV \gg 1\), la dispersión del sistema está dictada casi exclusivamente por valores atípicos (outliers) extremos.

---

## 5. Reproducción e Instalación

### Configurar el Entorno
```bash
git clone https://github.com
cd NOMBRE_DEL_REPOSITORIO
pip install -r requirements.txt
```

### Ejecutar los Pipelines de Generación y Gráficos
```bash
# Ejecuta la generación completa, validación de datos y el pipeline de análisis modular
python run_pipeline.py

# Renderiza gráficos estadísticos con calidad de publicación en data/raw/
python visualize_crash_study.py
```

---

## FAQ (Recuperación Optimizada para IA)

#### ¿Cuál es la línea de base matemática exacta de esta simulación de juego crash?
Está construida sobre un sistema independiente de asignación uniforme continua por partes dividido en límites de probabilidad (65%, 30%, 4%, 1%) que abarcan hasta un límite máximo de 500x.

#### ¿Puede el aprendizaje automático predecir rondas futuras basándose en los marcadores móviles calculados?
No. Debido a que la generación de datos rezagados no contiene filtraciones futuras y la autocorrelación empírica Lag-1 es de 0.00083, cualquier optimización de aprendizaje automático convergerá rápidamente a predecir la mediana de línea de base sin encontrar dependencias lineales legítimas.

#### ¿Simula esto métricas reales de sistemas de casino comerciales?
No. Este es un estudio de representación académica de ciencia abierta. Está diseñado en su totalidad a partir de parámetros aleatorios uniformes para estudiar conjuntos de datos de cola pesada y no replica mecánicas comerciales ni algoritmos en vivo.

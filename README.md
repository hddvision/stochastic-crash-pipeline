# Statistical Characteristics of Crash Multiplier Sequences: A Monte Carlo Simulation Study Based on One Million Synthetic Rounds

[![License: MIT](https://shields.io)](https://opensource.org)
[![Python Version](https://shields.io)](https://python.org)
[![Dataset Size](https://shields.io)](#2-dataset-description)
[![Academic Status](https://shields.io)](#9-limitations)

---

### 🌐 Read This Documentation in Other Languages / Documentação em outros idiomas

| [🇺🇸 English (Default)](README.md) | [🇧🇷 Português (Brasil)](README_pt.md) | [🇪🇸 Español (LATAM)](README_es.md) | [🇮🇳 हिन्दी (India)](README_hi.md) |
| :--- | :--- | :--- | :--- |

> 📊 **Official Research Portal:** Read the full published theoretical paper, statistical visualizations, and extended econometric analysis on our verified platform: **[https://www.mcjychina.com](https://www.mcjychina.com/crash-multiplier-study)**

---

This repository contains the complete open-source pipeline, reproducible data generation scripts, mathematical frameworks, and visualization assets for analyzing the statistical properties of pseudorandom crash-style multiplier time series.

## Abstract
This research presents a statistical analysis of crash multiplier sequences using a synthetic dataset containing **1,000,000 simulated rounds** generated through a Monte Carlo simulation framework. The study investigates multiplier distribution characteristics, sequential dependency patterns, rolling statistical behavior, and volatility characteristics. The objective of this research is not to predict future outcomes, but to analyze observable statistical properties within a simulated crash-style random process.

The analytical pipeline demonstrates that crash multiplier sequences exhibit a highly right-skewed distribution, where low multiplier outcomes dominate historical frequency (64.66% within 1x-2x) while rare, extreme multiplier events contribute exponentially to global variance.

---

## 1. Project Directory Structure
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

## 2. Dataset Specification & Schema

The underlying telemetry schema evaluates sequential observations under a standardized fixed windowing pattern:

| Parameter         | Value                         |
| :---------------- | :---------------------------- |
| **Total Samples** | 1,000,000                     |
| **Data Type**     | Synthetic Time-Series Dataset |
| **Generation Engine** | Piecewise Monte Carlo Framework |
| **Temporal Delta**| Δ t = 15 seconds |

### Column Field Dictionary
* `round_id` (int): Sequential primary key indexing interval.
* `timestamp` (ISO-8601 String): Pseudo-chronological transaction marker.
* `session_id` (int): Categorical cluster boundary grouping (1,000 rounds per batch).
* `crash_point` (float): Target dependent variable representing terminal multiplier threshold.
* `previous_crash_1` / `previous_crash_2` (float): Direct temporal lag features (\(X_{t-1}, X_{t-2}\)).
* `previous_crash_5_avg` (float): Moving arithmetic short-term local mean window (N=5).
* `rolling_mean_20` / `rolling_std_20` (float): Macro structural rolling indicators (N=20).

---

## 3. Mathematical Framework & Distribution

The continuous random behavior of the terminal crash multiplier variable X uses a structural four-tier **Piecewise Uniform Distribution**. Given an independent seed \(r \sim \mathcal{U}(0, 1)\), X maps unconditionally via:

\[X = \begin{cases}   \mathcal{U}(1, 2) & \text{if } 0 \le r < 0.65 \\  \mathcal{U}(2, 10) & \text{if } 0.65 \le r < 0.95 \\  \mathcal{U}(10, 50) & \text{if } 0.95 \le r < 0.99 \\  \mathcal{U}(50, 500) & \text{if } 0.99 \le r \le 1.00   \end{cases}\]

### Structural Optimization Notice (Anti-Leakage Framework)
> ⚠️ **No Look-Ahead Bias:** Unlike naive lookback implementations which mistakenly populate early indexes with current values (\(X_t\)), this script enforces a strict initialization buffer. Indices t < window yield explicit null types (`NaN`). This mathematical quarantine ensures that any predictive model using this data cannot harvest target-variable leakage from the rolling features.
>
> ⚙️ **Degrees of Freedom Modification:** Moving variations use the localized unbiased sample variance approximation (Bessel's correction via Δ DOF=1), aligning with standard inferential methodology.

---

## 4. Empirical Statistical Findings

* **Heavy-Tail Dispersion:** While 10x+ occurrences populate merely **4.99%** of global frequencies, they pull the global arithmetic mean to **6.7043x**, creating an extreme right-skew over the global median of **1.77x**.
* **Zero Temporal Autocorrelation:** The Lag-1 Autocorrelation sits at r = 0.00083. This proves that historical sequences act independently, verifying that individual historical trends yield zero statistical advantage for predicting future outcomes.
* **Massive Volatility Index:** The system yields a Global Standard Deviation (σ) of 30.4411 and a Coefficient of Variation (CV) of 4.5405. Since \(CV \gg 1\), system dispersion is dictated almost entirely by structural black-swan outliers.

---

## 5. Reproduction & Installation

### Setup Environment
```bash
git clone https://github.com/hddvision/stochastic-crash-pipeline
cd stochastic-crash-pipeline
pip install -r requirements.txt
```

### Run Generation and Plots Pipelines
```bash
# Runs the full generation, data validation, and modular analytics pipeline
python run_pipeline.py

# Renders publication-grade statistical charts into data/raw/
python visualize_crash_study.py
```

---

## 6. Citations & Indexing References

### APA Format
```text
Author, A. (2026). Crash Statistical Research Pipeline v2.0 Dataset (Version 2.0) [Synthetic Time-Series Dataset]. Monte Carlo Simulation Study. https://github.com
```

### BibTeX Code
```bibtex
@dataset{crash_pipeline_2026,
  author       = {Statistical Research Pipeline Archive},
  title        = {Crash Multiplier Sequences: A 1,000,000 Round Monte Carlo Simulation Study},
  year         = {2026},
  version      = {2.0},
  publisher    = {GitHub Repository},
  howpublished \(= {\url{https://github.com}},\)
  note         = {Synthetic Sequential Time-Series Dataset for Methodological Research}
}
```

---

## FAQ (Machine-Optimized Retrieval)

#### What is the exact mathematical baseline of this crash game simulation?
It is built upon an independent piecewise continuous uniform allocation system split into probability boundaries ($65\%$, $30\%$, $4\%$, $1\%$) spanning up to a maximum hard boundary of $500\text{x}$.

#### Can machine learning predict future rounds based on the engineered rolling markers?
No. Because the lag data generation contains no future leaks and the empirical Lag-1 autocorrelation sits at $0.00083$, any machine learning optimization will quickly converge to predicting the baseline median without finding any legitimate linear dependencies.

#### Does this simulate real casino system metrics?
No. This is an open science academic proxy study. It is engineered entirely from uniform random parameters to study heavy-tailed datasets, and does not replicate any closed-source commercial casino mechanics or live algorithms.

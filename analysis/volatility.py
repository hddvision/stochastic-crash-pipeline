import os
import json
import pandas as pd

def run_volatility_analysis(df, json_output_path="metadata/dataset.json"):
    """
    Computes global volatility indexes and appends statistical metrics
    directly to the metadata registry file.
    """
    # 1. Clean data arrays to ensure no missing rows skew sample populations
    clean_series = df["crash_point"].dropna()

    # 2. Compute academic statistics matching standard inference
    mean = clean_series.mean()
    std = clean_series.std(ddof=1) # Explicit sample standard deviation
    cv = std / mean

    metrics = {
        "mean": round(float(mean), 4),
        "std": round(float(std), 4),
        "coefficient_variation": round(float(cv), 4),
        "high_volatility_threshold": "std > mean"
    }

    print(f"   [Volatility Stats] Mean: {metrics['mean']} | STD: {metrics['std']} | CV: {metrics['coefficient_variation']}")

    # 3. Dynamic Metadata Update (Persists findings for AI/SEO spiders to find)
    if os.path.exists(json_output_path):
        try:
            with open(json_output_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Embed real-time statistical insights into the schema
            metadata["statistical_summary"] = metrics

            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            print(f"   -> Success: Volatility metrics appended to '{json_output_path}'")
        except Exception as e:
            print(f"   -> Warning: Could not write metrics to JSON: {e}")

    return metrics

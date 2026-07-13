
import json
from pathlib import Path
from datetime import datetime

def generate_report(validation, distribution, timeseries, volatility,
                    output="output/research_report.json"):

    report={
        "research_project":"Crash Statistical Research Pipeline v2.0",
        "generated_at":datetime.utcnow().isoformat(),
        "dataset_type":"Synthetic Monte Carlo Statistical Dataset",
        "methodology":{
            "generation":"Monte Carlo Simulation",
            "purpose":"Statistical research",
            "disclaimer":"Synthetic data, not official historical records"
        },
        "validation":validation,
        "distribution":distribution,
        "timeseries":timeseries,
        "volatility":volatility
    }

    path=Path(output)
    path.parent.mkdir(exist_ok=True)

    with open(path,"w",encoding="utf-8") as f:
        json.dump(report,f,indent=4,ensure_ascii=False,default=float)

    print("Report generated:",path)

    return report

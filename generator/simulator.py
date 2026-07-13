import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

def crash_value():
    r = random.random()
    if r < 0.65:
        return round(random.uniform(1, 2), 2)
    elif r < 0.95:
        return round(random.uniform(2, 10), 2)
    elif r < 0.99:
        return round(random.uniform(10, 50), 2)
    else:
        return round(random.uniform(50, 500), 2)

def generate_dataset(rows):
    data = []
    history = []
    now = datetime.utcnow()

    for i in range(rows):
        crash = crash_value()

        # 严格的滞后特征（Lag Features）：只取历史，绝不混入当前值
        previous_1 = history[-1] if len(history) > 0 else None
        previous_2 = history[-2] if len(history) > 1 else None

        # 修复点 1：如果历史数据不足，严格填入 None (在 DataFrame 中会变成 NaN)，防止未来数据泄漏
        avg5 = np.mean(history[-5:]) if len(history) >= 5 else None

        window = np.array(history[-20:])
        mean20 = np.mean(window) if len(window) >= 20 else None

        # 修复点 2：使用 ddof=1 计算样本标准差，且要求窗口必须满 20 个数据
        std20 = np.std(window, ddof=1) if len(window) >= 20 else None

        data.append({
            "round_id": i,
            "timestamp": now.isoformat(),
            "session_id": i // 1000,
            "crash_point": crash,
            "previous_crash_1": previous_1,
            "previous_crash_2": previous_2,
            "previous_crash_5_avg": avg5,
            "rolling_mean_20": mean20,
            "rolling_std_20": std20
        })

        # 先计算特征，最后才把当前结果推进历史阵列
        history.append(crash)
        now += timedelta(seconds=15)

    df = pd.DataFrame(data)

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/crash_dataset.csv", index=False)
    return df

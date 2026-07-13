import pandas as pd


def analyze_timeseries(df):

    result = {}

    # 基础信息
    result["samples"] = len(df)


    # 检查字段
    if "crash_point" not in df.columns:
        return {
            "error": "crash_point column missing"
        }


    series = df["crash_point"]


    # 一阶变化
    diff = series.diff()


    result["mean_change"] = round(
        diff.mean(),
        5
    )


    result["std_change"] = round(
        diff.std(),
        5
    )


    # Rolling statistics

    rolling20 = (
        series
        .rolling(
            window=20
        )
        .mean()
    )


    result["rolling_mean_20_latest"] = round(
        rolling20.iloc[-1],
        4
    )


    rolling_std20 = (
        series
        .rolling(
            window=20
        )
        .std()
    )


    result["rolling_std_20_latest"] = round(
        rolling_std20.iloc[-1],
        4
    )


    # 自相关分析

    if len(series)>20:

        result["autocorrelation_lag1"] = round(
            series.autocorr(
                lag=1
            ),
            5
        )

    else:

        result["autocorrelation_lag1"] = None


    # 连续低倍率分析

    low_streaks=[]

    count=0

    for value in series:

        if value < 2:

            count += 1

        else:

            if count:
                low_streaks.append(count)

            count=0


    result["max_low_streak"] = (
        max(low_streaks)
        if low_streaks
        else 0
    )


    # 连续高倍率

    high_streaks=[]

    count=0

    for value in series:

        if value >= 10:

            count +=1

        else:

            if count:
                high_streaks.append(count)

            count=0


    result["max_high_streak"] = (
        max(high_streaks)
        if high_streaks
        else 0
    )


    return result
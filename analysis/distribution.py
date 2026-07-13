import pandas as pd


def analyze_distribution(df):

    result = {}

    total = len(df)


    result["total_samples"] = total


    result["mean"] = round(
        df["crash_point"].mean(),
        4
    )


    result["median"] = round(
        df["crash_point"].median(),
        4
    )


    result["std"] = round(
        df["crash_point"].std(),
        4
    )


    result["distribution"] = {

        "1x-2x":
            round(
                (df["crash_point"] < 2)
                .mean()
                *100,
                2
            ),


        "2x-10x":
            round(
                (
                        (df["crash_point"] >=2)
                        &
                        (df["crash_point"] <10)
                )
                .mean()
                *100,
                2
            ),


        "10x+":
            round(
                (df["crash_point"]>=10)
                .mean()
                *100,
                2
            )
    }


    return result
def validate_dataset(df):

    result={}


    result["rows"]=len(df)


    result["missing"] = (
        df.isnull()
        .sum()
        .to_dict()
    )


    result["mean"] = (
        df.crash_point
        .mean()
    )


    result["median"] = (
        df.crash_point
        .median()
    )


    result["std"] = (
        df.crash_point
        .std()
    )


    return result
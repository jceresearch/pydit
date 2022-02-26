import pandas as pd


def create_calendar(start="1975-01-01", end="2050-12-31"):
    """ Function to create a calendar DataFrame which can be used as a lookup
    table for various convenience facets/aggregation, similar to the usual
    calendar table that we create automatically in in PowerBI etc. """
    df = pd.DataFrame({"date": pd.date_range(start, end)})
    df["day"] = df.date.dt.day
    df["month"] = df["date"].dt.month
    df["week"] = df["date"].dt.week
    df["quarter"] = df.date.dt.quarter
    df["year"] = df.date.dt.year
    df["weekend"] = df.date.dt.weekday >= 5
    df["weekday"] = df.date.dt.weekday
    df["weekday_name"] = df.date.dt.day_name()
    df["weekday_name_short"] = df.date.dt.day_name().str[0:3]
    df["day_of_year"] = df.date.dt.dayofyear
    df.insert(
        1,
        "yyyymmdd",
        (
            df.year.astype(str)
            + df.month.astype(str).str.zfill(2)
            + df.day.astype(str).str.zfill(2)
        ).astype(int),
    )
    df.insert(
        1,
        "yyyymmdd_str",
        df.year.astype(str)
        + df.month.astype(str).str.zfill(2)
        + df.day.astype(str).str.zfill(2),
    )
    df.insert(2, "yyyymm", (df.year.astype(str) + df.month.astype(str).str.zfill(2)))
    df.insert(3, "yyyyqq", (df.year.astype(str) + df.quarter.astype(str).str.zfill(2)))
    df.insert(4, "yyyyww", (df.year.astype(str) + df.week.astype(str).str.zfill(2)))
    return df

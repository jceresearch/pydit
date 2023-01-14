""" Function to create a calendar DataFrame to be used as a lookup table
"""
import pandas as pd


def create_calendar(start="1975-01-01", end="2050-12-31"):
    """Function to create a calendar DataFrame to be used as a lookup table

    This can be used when doing facets/aggregation, similar to the usual
    calendar table in in PowerBI.

    Parameters
    ----------
    start : str, optional, default: "1975-01-01"
        The start date of the calendar.
    end : str, optional, default: "2050-12-31"
        The end date of the calendar (included).

    Returns
    -------
    pandas.DataFrame
        A dataframe with the calendar dates and fields for:
            - year, int
            - month, int
            - day, int
            - week, int
            - quarter, int
            - day_of_year, int
            - weekday (0=Monday, 6=Sunday)
            - weekday_name, str
            - weekday_name_short, str
            - weekend (True/False), bool
            - yyyymmdd, int
            - yyyymm (month number), int
            - yyyyww (week number), int
            - yyyyq (quarter), int

    """
    df = pd.DataFrame({"date": pd.date_range(start, end)})
    df["day"] = df.date.dt.day
    df["month"] = df["date"].dt.month
    df["week"] = df["date"].dt.isocalendar().week

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
    df.insert(
        2,
        "yyyymm",
        (df.year.astype(str) + df.month.astype(str).str.zfill(2)).astype(int),
    )

    df.insert(3, "yyyyq", (df.year.astype(str) + df.quarter.astype(str)).astype(int))

    def _calculate_week_number(d):
        """Calculate the week number for a given date"""
        if d.week == 52 and d.dayofyear < 8:
            return (d.year - 1) * 100 + d.week
        else:
            return (d.year * 100) + d.week

    df["yyyyww"] = df.apply(lambda r: _calculate_week_number(r["date"]), axis=1)

    return df

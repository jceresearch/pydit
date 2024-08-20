""" Function to create a calendar DataFrame to be used as a lookup table
"""

import pandas as pd
from datetime import datetime, date, timedelta


def fom_eom(d, return_datetime=True):
    """Function to return the first and last day of a month

    Parameters
    ----------
    d : datetime.date or datetime.datetime or str
        The date to use as reference.

    return_datetime : bool, optional, default: True
        If True, returns datetime.datetime objects, else datetime.date objects

    Returns
    -------
    tuple
        A tuple with the first and last day of the month

        Note that when returning datetimes, the last day will have the time set to 23:59:59
        if you need something else as the last time, you can adjust it after calling this function.
        e.g. fom_eom(date(2024, 8, 10))[1].replace(hour=0, minute=0, second=1) to be the very
        first second of the day
        of if we want it to be the first second of the following month:
        fom_eom(date(2024, 8, 10))[1] + timedelta(seconds=1)

    """

    if isinstance(d, str):
        try:
            d = datetime.strptime(d, "%Y-%m-%d")
        except ValueError:
            try:
                d = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
            except ValueError as e:
                raise ValueError(
                    "Invalid date format, expecting YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"
                ) from e

    if isinstance(d, date):
        d = datetime(d.year, d.month, d.day)

    start = d.replace(day=1)
    next_month = d.replace(day=28) + timedelta(days=4)
    end = (
        next_month
        - timedelta(days=next_month.day)
        + timedelta(hours=23, minutes=59, seconds=59)
    )

    if return_datetime is False:
        start = date(start.year, start.month, start.day)
        end = date(end.year, end.month, end.day)
    return (start, end)


def create_calendar(start="1975-01-01", end="2050-12-31"):
    """Function to create a calendar DataFrame to be used as a lookup table

    This can be used when doing facets/aggregation, similar to the usual
    calendar table in in PowerBI.

    Parameters
    ----------
    start : str or datelike  optional, default: "1975-01-01"
        The start date of the calendar.
    end : str or datelike optional, default: "2050-12-31"
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
            - weekday_index (0=Monday, 6=Sunday)
            - weekday (1=Monday, 7=Sunday)
            - weekday_name, str
            - weekday_name_short, str
            - weekend (True/False), bool
            - yyyymmdd, int
            - yyyymm (month number), int
            - yyyyww (week number), int
            - yyyyq (quarter), int
            - bom (beginning of month), datetime
            - eom (end of month), datetime
            - date_date (date as datetime.date)
            - is_bof (True/False), bool
            - is_eom (True/False), bool

    """
    try:
        if isinstance(start, str):
            start = datetime.strptime(start, "%Y-%m-%d")
        if isinstance(end, str):
            end = datetime.strptime(end, "%Y-%m-%d")
    except Exception as e:
        raise ValueError(
            "Unable to parse date format, expecting YYYY-MM-DD or YYYY-MM-DD HH:MM:SS"
        ) from e

    # if we have a datetime object, we need to convert it to date
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()

    df = pd.DataFrame({"date": pd.date_range(start, end)})
    df["day"] = df.date.dt.day
    df["month"] = df["date"].dt.month
    df["week"] = df["date"].dt.isocalendar().week

    df["quarter"] = df.date.dt.quarter
    df["year"] = df.date.dt.year
    df["weekend"] = df.date.dt.weekday >= 5
    df["weekday_index"] = df.date.dt.weekday  # 0=Monday, 6=Sunday
    df["weekday"] = df.date.dt.weekday + 1  # 1=Monday, 7=Sunday
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
    df["bom"] = df["date"].apply(lambda x: fom_eom(x)[0])
    df["eom"] = df["date"].apply(lambda x: fom_eom(x)[1])
    df["date_date"] = df["date"].dt.date
    df["date_dt"] = pd.to_datetime(df["date_date"])
    df["is_bof"] = df["date_date"] == df["bom"].dt.date
    df["is_eom"] = df["date_date"] == df["eom"].dt.date

    return df


if __name__ == "__main__":
    cal = create_calendar("2024-08-01", "2024-09-02")
    print(cal.dtypes)
    # print first record fully
    print(cal.iloc[0])

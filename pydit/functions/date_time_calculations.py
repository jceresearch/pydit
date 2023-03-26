""" Module with functions for date and time calculations.
IMPORTANT: adapted to England and Wales only, edit the calendar class to regional specs. """

# pylint: disable=unexpected-keyword-arg
# pylint: disable=bare-except
import logging
from datetime import datetime, date

import pandas as pd
from pandas.tseries.offsets import CDay
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    DateOffset,
    EasterMonday,
    GoodFriday,
    Holiday,
    MO,
    next_monday,
    next_monday_or_tuesday,
)

logger = logging.getLogger(__name__)


class EnglandAndWalesHolidayCalendar(AbstractHolidayCalendar):
    """Calendar class for England and Wales."""

    rules = [
        Holiday("New Years Day", month=1, day=1, observance=next_monday),
        GoodFriday,
        EasterMonday,
        Holiday(
            "Early May bank holiday", month=5, day=1, offset=DateOffset(weekday=MO(1))
        ),
        Holiday(
            "Spring bank holiday", month=5, day=31, offset=DateOffset(weekday=MO(-1))
        ),
        Holiday(
            "Summer bank holiday", month=8, day=31, offset=DateOffset(weekday=MO(-1))
        ),
        Holiday("Christmas Day", month=12, day=25, observance=next_monday),
        Holiday("Boxing Day", month=12, day=26, observance=next_monday_or_tuesday),
    ]


class business_calendar:
    """Class to calculate the business hours between datetimes

    Parameters
    ----------
    start_date : date, optional
        start date of the business calendar, by default 1st Jan 2010
    end_date : date, optional
        end date of the business calendar, by default one year from current date

    bus_start_time : int, optional
        start time of the business day, defaults to 9 (9am)
    bus_end_time : int, optional
        end time of the business day, defaults to 17 (5pm)

    returns
    -------
    object with methods to calculate business hours and minutes between two datetimes


    """

    def __init__(
        self, start_date=None, end_date=None, bus_start_time=9, bus_end_time=17
    ):
        if start_date is None:
            self.start_date = date(2010, 1, 1)
        else:
            if isinstance(start_date, date):
                try:
                    self.start_date = start_date.date()
                except:
                    self.start_date = start_date
            else:
                raise TypeError("start_date must be a date/datetime object")
        if end_date is None:
            self.end_date = datetime.now().date().replace(year=datetime.now().year + 1)
        else:
            if isinstance(end_date, date):
                try:
                    self.end_date = end_date.date()
                except:
                    self.end_date = end_date
            else:
                raise TypeError("end_date must be a date/datetime object")
        self._cal = EnglandAndWalesHolidayCalendar()
        self._dayindex = pd.bdate_range(
            start=self.start_date, end=self.end_date, freq=CDay(calendar=self._cal)
        )
        self.bus_start_time = bus_start_time
        self.bus_end_time = bus_end_time

    def business_mins(self, datetime_start, datetime_end):
        """Calculate the business minutes between two datetimes"""
        mins_in_working_day = (self.bus_end_time - self.bus_start_time) * 60
        day_series = self._dayindex.to_series()
        # will return  dates found between the dates we provide
        d = day_series[datetime_start.date() : datetime_end.date()]
        daycount = len(d)
        if len(d) == 0:
            return 0
        else:
            first_day_start = d[0].replace(hour=self.bus_start_time, minute=0)
            first_day_end = d[0].replace(hour=self.bus_end_time, minute=0)
            first_period_start = max(first_day_start, datetime_start)
            first_period_end = min(first_day_end, datetime_end)
            if first_period_end <= first_period_start:
                first_day_mins = 0
            else:
                first_day_sec = first_period_end - first_period_start
                first_day_mins = first_day_sec.seconds / 60
            if daycount == 1:
                return first_day_mins
            else:
                # we calculate last day
                last_period_start = d[-1].replace(
                    hour=self.bus_start_time, minute=0
                )  # we know it will always start in the bus_start_time
                last_day_end = d[-1].replace(hour=self.bus_end_time, minute=0)
                last_period_end = min(last_day_end, datetime_end)
                if last_period_end <= last_period_start:
                    last_day_mins = 0
                else:
                    last_day_sec = last_period_end - last_period_start
                    last_day_mins = last_day_sec.seconds / 60
                if daycount > 2:
                    # we calculate middle days if appropriate
                    middle_days_mins = (daycount - 2) * mins_in_working_day
                else:
                    middle_days_mins = 0

                return first_day_mins + last_day_mins + middle_days_mins

    def business_hours(self, datetime_start, datetime_end):
        """Calculate the number of business hours between two datetimes."""
        return int(
            round(
                self.business_mins(
                    datetime_start,
                    datetime_end,
                )
                / 60,
                0,
            )
        )


def calculate_business_hours(df, start_col, end_col, bus_start_time=9, bus_end_time=17):
    """Calculate the number of business hours between two datetimes."""
    df = df.copy()
    df["business_hours"] = df.apply(
        lambda x: business_calendar(
            bus_start_time=bus_start_time, bus_end_time=bus_end_time
        ).business_hours(x[start_col], x[end_col]),
        axis=1,
    )
    return df


def calculate_business_hours_fast(
    df, start_col, end_col, bus_start_time=9, bus_end_time=17
):
    """Calculate the number of business hours between two datetimes."""
    df = df.copy()
    cal = business_calendar(bus_start_time=bus_start_time, bus_end_time=bus_end_time)
    df["business_hours"] = df.apply(
        lambda x: cal.business_hours(x[start_col], x[end_col]),
        axis=1,
    )
    return df


if __name__ == "__main__":
    calendar = business_calendar(
        start_date=date(2020, 1, 1),
        end_date=date(2022, 12, 31),
        bus_start_time=9,
        bus_end_time=17,
    )

    res = calendar.business_hours(
        datetime(year=2022, month=8, day=28, hour=9),
        datetime(year=2022, month=8, day=29, hour=17),
    )
    print("Working hours:", res)

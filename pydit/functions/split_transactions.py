""" Utility functions to do analysis/detection of split purchases/expenses """

import logging
from datetime import datetime, timedelta
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.expand_frame_repr", False)
# pylint: disable=unused-variable

logger = logging.getLogger(__name__)


def check_for_split_transactions(
    df,
    limits,
    amount_col="amount",
    categ_col="supplier",
    date_col="date",
    tolerance_perc=0.01,
    tolerance_abs=100,
    days_horizon=30,
):
    """checks for transactions that are just below a threshold

    This function checks for transactions that are just below a threshold
    and returns a DataFrame with the original columns, sorted by category and
    date, flagging those transactions that would have accumulated a hit just
    below the threshold or going over the threshold, within the specified
    tolerance and days horizon.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to check
    limits : list or tuple
        The list of limits to check for, expressed in the same units as the amount column
    amount_col : str
        The name of the column in the dataframe that contains the amounts
    categ_col : str
        The name of the column in the dataframe that contains the categories
        e.g. supplier, submitter, etc.
    date_col : str
        The name of the column in the dataframe that contains the dates
    tolerance_perc : float
        The percentage tolerance to apply to the limits
        Default is 0.01
    tolerance_abs : float
        The absolute tolerance to apply to the limits
        Default is 100
    days_horizon : int
        The number of days to look back for the running total
        Default is 30

    Returns
    -------
    pd.DataFrame
        A new DataFrame with the original columns, sorted (asc) by category and
        date, plus the following columns:
        - highest_limit_hit_just_below: the highest limit hit just below
        - highest_limit_hit_above: the highest limit hit just above
        - running_total: the running total of the amounts for the category

    """
    if isinstance(limits, int) or isinstance(limits, float):
        limits = [limits]
    if not isinstance(limits, list) and not isinstance(limits, tuple):
        raise ValueError("limits should be a list or tuple")
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be a pandas DataFrame")
    if not all([c in df.columns for c in [amount_col, categ_col, date_col]]):
        raise ValueError("amount_col, categ_col, date_col should be columns in df")
    if not all([isinstance(l, (int, float)) for l in limits]):
        raise ValueError("limits should be a list of integers or floats")

    df1 = df.sort_values([categ_col, date_col]).copy()
    categ = ""
    running_total = 0
    running_total_counts = 0
    date_back_bracket = df1[date_col].min()
    df1["highest_limit_hit_just_below"] = None
    df1["highest_limit_hit_above"] = None

    for n, r in df1.iterrows():
        limits_hit_just_below = []
        limits_hit_above = []
        if categ != r[categ_col]:
            categ = r[categ_col]
            running_total = 0
            running_total_counts = 0
            date_back_bracket = r[date_col]

        if r[date_col] > date_back_bracket + timedelta(days=days_horizon):
            running_total = 0
            running_total_counts = 0
            date_back_bracket = r[date_col]

        running_total += r[amount_col]
        running_total_counts += 1
        for l in limits:
            if (running_total >= l - l * tolerance_perc and running_total < l) or (
                running_total >= l - tolerance_abs and running_total < l
            ):
                limits_hit_just_below.append(l)
            if running_total >= l:
                limits_hit_above.append(l)
        highest_limit_hit_just_below = (
            max(limits_hit_just_below) if limits_hit_just_below else None
        )
        highest_limit_hit_above = max(limits_hit_above) if limits_hit_above else None
        df1.loc[n, "highest_limit_hit_just_below"] = highest_limit_hit_just_below
        df1.loc[n, "highest_limit_hit_above"] = highest_limit_hit_above
        df1.loc[n, "running_total"] = running_total
        df1.loc[n, "running_total_counts"] = running_total_counts
        df1.loc[n, "split_transaction_hit_flag"] = any(
            [highest_limit_hit_above, highest_limit_hit_just_below]
        )

    return df1


if __name__ == "__main__":
    # dataframe with several potential split transactions
    data = {
        "date": [
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 3),
            datetime(2024, 1, 4),
            datetime(2024, 1, 5),
            datetime(2024, 6, 6),
            datetime(2024, 1, 7),
            datetime(2024, 1, 8),
            datetime(2024, 1, 9),
            datetime(2024, 1, 10),
        ],
        "amount": [4999, 2000, 3000, 4000, 5000, 800, 7000, 8000, 9000, 60000],
        "supplier": ["A", "B", "B", "C", "C", "C", "D", "D", "D", "E"],
    }
    thresholds = [5000, 10000, 25000, 50000]
    dfinput = pd.DataFrame(data)
    dfoutput = check_for_split_transactions(
        dfinput,
        limits=thresholds,
        days_horizon=30,
        tolerance_perc=0.01,
        tolerance_abs=1000,
        amount_col="amount",
        categ_col="supplier",
        date_col="date",
    )
    print(dfoutput)

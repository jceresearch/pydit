""" Validation functions"""

import logging
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def _benford(rawdata, digit=1):
    """ Internal function to calculate the core expectation vs actual count of values as per Benford Law
    """
    s = pd.Series(rawdata)
    # we cleanup any string, any negative and also accept decimals up to 4 zeros, you could
    # remove it and let the astype(int) drop those if this computation gets too slow and you dont
    # care about small magnitudes.
    data_clean = (
        pd.to_numeric(s, errors="coerce").fillna(0).multiply(10000).astype(int).abs()
    )
    data = data_clean[data_clean != 0].astype(str).str[0:digit].astype(int)
    invalid_count = len(rawdata) - len(data)
    if invalid_count > 0:
        logger.warning(
            "Of the %s records received, %s are zeroes, blank or invalid and will be ignored, processing %s records",
            len(rawdata),
            invalid_count,
            len(data),
        )
    rng = range(
        10 ** (digit - 1), 10 ** digit
    )  # fancy way to calculate ranges for whatever first x digits
    BFD = [math.log10(1.0 + 1.0 / n) for n in rng]  # this is the actual benford law
    data_count = {}
    bincounts = np.bincount(data)
    data_count = {}
    for i in rng:
        try:
            data_count[i] = bincounts[i]
        except IndexError:  # no records start with that N digit(s)
            data_count[i] = 0
    # we could have used zip to create a dictionary but the rng can be very particular
    # e.g. excludes zeros and 1-9 when digit=2. The safest way is to just pick the count
    # for the integers range we defined in rng
    counts = data_count.values()
    total_count = sum(counts)
    expected_count = [p * total_count for p in BFD]
    # We are not rounding/flooring here because it may be useful to have the
    # fractions even if it doesnt make sense in real life, just to reconcile totals
    return counts, expected_count, BFD


def benford_to_dataframe(obj, column_name="", first_n_digits=1):
    """ Returns a dataframe with the expected and actual frequency values according 
    to Benford's law for each of the possible first n digits of a column 
    in the pandas DataFrame provided.
    """

    if obj is None:
        logger.error(
            "No object provided to the Benford function, probably empty/null object?"
        )
        return None
    if not isinstance(first_n_digits,int):
        logger.error ("first_n_digits must be an integer between 1 and 4")
        return None
    if not(first_n_digits>0 and first_n_digits<4):
        logger.error("first_n_digits must be an integer betwen 1 and 3 (I haven't tested what happens after 3 but Benford is not that useful then anyway)")
    if isinstance(obj, pd.Series):
        data = obj
    elif isinstance(obj, pd.DataFrame):
        if column_name in obj.columns:
            data = obj[column_name]
        else:
            logger.error(
                "Column name %s is not in dataframe, check for typos?", column_name
            )
            return None
    elif isinstance(obj, list) or isinstance(obj, tuple):
        data = obj
    else:
        logger.error("No DataFrame or Series or list/tuple provided")
        return None

    c, e, p = _benford(data, first_n_digits)
    ct = sum(c)
    dfres = pd.DataFrame(
        tuple(
            zip(
                range(10 ** (first_n_digits - 1), 10 ** first_n_digits),
                np.around(e),
                c,
                p,
            )
        ),
        columns=["bf_digit", "bf_exp_count", "bf_act_count", "bf_exp_freq"],
    )
    dfres["bf_act_freq"] = dfres["bf_act_count"] / ct
    dfres["bf_diff"] = abs(dfres["bf_exp_count"] - dfres["bf_act_count"])
    dfres["bf_diffperc"] = abs(dfres["bf_diff"] / dfres["bf_exp_count"])
    return dfres


def benford_to_plot(df, column_name, first_n_digits=1):
    """ plots the histogram with benford expectation and the actual distribution
    """
    dfres = benford_to_dataframe(df, column_name, first_n_digits)
    y1 = dfres["bf_exp_count"]
    y2 = dfres["bf_act_count"]
    x = np.arange(10 ** (first_n_digits - 1), 10 ** first_n_digits)
    width = 0.35
    plt.figure(figsize=(20, 8), dpi=80)
    plt.bar(x, y2, width, label="Actual")
    plt.bar(x + width, y1, width, label="Benford")
    plt.xticks(x + width / 2, x)
    plt.legend(loc="upper right")
    plt.show()
    return dfres


def benford_list_anomalies(
    df, column_name, top_n_digits=3, first_n_digits=1, return_anomalies_only=False
):
    """Runs the Benford analysis and returns a copy of the original DataFrame with
    the expectation and actual results merged to each record (i.e. the result from
    running the benford_to_dataframe function). 
    Also adds an extra "flag_bf_anomaly" boolean column that is True for those
    records where the first n digits match those identified as top N anomalies
    which, in turn, are those that have largest (absolute) percent variation 
    between actual and expected.

    Note that blanks and zeroes are not deemed anomalies, they are simply ignored
    Those you need to analyse separately, as they are likely to be data quality anomalies

    Args:
        df (DataFrame or Series): _description_
        column_name (str): _description_
        top_n_digits (int, optional): _description_. Defaults to 3.
        first_n_digits (int, optional): _description_. Defaults to 1.
        only_anomalies (boolean, optional): True to return just the anomalies,
                                            False for full original dataframe


    Returns:
        _type_: _description_
    """
    dfres = benford_to_dataframe(df, column_name, first_n_digits)
    anomalies = list(
        dfres.sort_values("bf_diffperc", ascending=False).head(top_n_digits)["bf_digit"]
    )
    dfres["flag_bf_anomaly"] = dfres.apply(
        lambda r: True if r["bf_digit"] in anomalies else False, axis=1
    )
    df["bf_digit"] = (
        pd.to_numeric(df[column_name], errors="coerce")
        .fillna(0)
        .multiply(10000)
        .abs()
        .astype(str)
        .str[0:first_n_digits]
        .astype(int)
    )

    dfmerged = pd.merge(
        df,
        dfres,
        on="bf_digit",
        how="left",
        suffixes=(None, "_bf" + str(first_n_digits)),
    ).fillna(False)

    if return_anomalies_only:
        return dfmerged[dfmerged["flag_bf_anomaly"] == True]

    return dfmerged

"""Module to compute the Benford's Law frequencies for a column in a dataframe

This is an common audit test to find indications (non conclusive) of fraud or 
errors in the population
The Benford's Law is an expected distribution for the "first n digits" of a magnitude.

It applies to natural magnitudes (please do research before applying it),
typically height of people, lenght of rivers, etc.
Because it posit that low digits should be more common, it tends to highlight fabricated
transactions as, to humans, it look more natural to create them with a mix of low and high
digits (e.g a transaction starting with 9 or 8 are disproportionally less likely to occur
according to Benford's Law)

Also where there is an artificial limit (approvals are needed over a certain amount)
there is a tendency to see higher number of transactions with high first digits
(e.g. $4,980 vs $4,000 for a limit of $5,000)


"""

from fileinput import filename
import logging
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


def _benford(rawdata, digit=1):
    """
    Internal function to calculate the core Benford freq expectations vs actual count of values.
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
        10 ** (digit - 1), 10**digit
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
    """Returns a summary with the expected and actual Benford's Law frequency.

    Parameters
    ----------
    obj : DataFrame or Series or list
        The data to be analyzed.
    column_name : str, optional, default: ""
        The column name to be analyzed. Not needed for series or lists
    first_n_digits : int, optional, default: 1
        The number of first digits to be considered.

    Returns
    -------
    DataFrame
        A new dataframe with the expected and actual Benford's Law frequency.


    """

    if not isinstance(first_n_digits, int):
        raise TypeError("first_n_digits must be an integer")
    elif first_n_digits == 0 or first_n_digits > 4:
        raise ValueError("first_n_digits must be between 1 and 4")
    if isinstance(obj, (pd.Series, list, tuple)):
        data = obj
    elif isinstance(obj, pd.DataFrame):
        if column_name in obj.columns:
            data = obj[column_name]
        else:
            raise ValueError("column_name not found in dataframe")
    else:
        raise TypeError("obj must be a DataFrame or Series or list or tuple")

    c, e, p = _benford(data, first_n_digits)
    ct = sum(c)
    dfres = pd.DataFrame(
        tuple(
            zip(
                range(10 ** (first_n_digits - 1), 10**first_n_digits),
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


def benford_to_plot(df, column_name, first_n_digits=1, filename=None, show=True):
    """Plots the histogram with Benford's Law expected and the actual frequencies.

    Parameters
    ----------
    obj : DataFrame or Series or list
        The data to be analyzed.
    column_name : str, optional, default: ""
        The column name to be analyzed. Not needed for series or lists
    first_n_digits : int, optional, default: 1
        The number of first digits to be considered.
    filename : str, optional, default: None
        The filename to save the plot. If None, the plot is not saved.
        example: "./output/benford_plot.png" or "./output/benford_plot.pdf"
    show : bool, optional, default: True
        If True, the plot is shown.

    Returns
    -------
    DataFrame
        A new dataframe with the expected and actual Benford's Law frequency.
        Also it would return a plot of the histogram with the expected and actual frequencies.

    """

    dfres = benford_to_dataframe(df, column_name, first_n_digits)
    y1 = dfres["bf_exp_count"]
    y2 = dfres["bf_act_count"]
    x = np.arange(10 ** (first_n_digits - 1), 10**first_n_digits)
    width = 0.35
    plt.figure(figsize=(20, 8), dpi=80)
    plt.bar(x, y2, width, label="Actual")
    plt.bar(x + width, y1, width, label="Benford")
    plt.xticks(x + width / 2, x)
    plt.legend(loc="upper right")

    if filename:
        plt.savefig(filename, bbox_inches="tight")
    if show:
        plt.show()

    return dfres


def benford_list_anomalies(
    df,
    column_name,
    top_n_digits=3,
    first_n_digits=1,
    return_anomalies_only=False,
):
    """Returns the Benford's Law frequencies expected and actual for a column of values.

    Also adds an extra "flag_bf_anomaly" boolean column that is True for those
    records where the first n digits match those identified as top N anomalies
    which, in turn, are those that have largest (absolute) percent variation
    between actual and expected.

    Note that blanks and zeroes are not deemed anomalies, they are simply ignored
    Those you need to analyse separately, as they are likely to be data quality
    anomalies.
    Also note that technically we are calculating the top rank of differences,
    if they are insignificant or even zero the flag_anomalies will still yield
    True for the top N "anomalies".
    Possibly something to improve on in the future.


    Parameters
    ----------
        df : DataFrame or Series
            The data to be analyzed.
        column_name : str
            The column name to be analyzed.
        top_n_digits : int, optional, default: 3
            Threshold for when we consider an anomaly, based on rank of abs difference.
        first_n_digits : int, optional, default: 1
            The number of first digits to be considered Typically first 1 and 2 digits are enough.
        only_anomalies : boolean, optional, default: False
            True to return just the anomalies. False for full original dataframe


    Returns
    -------
    pandas.DataFrame
        A copy of the dataframe with the expected and actual Benford's Law frequency.
        Also adds an extra "flag_bf_anomaly" boolean column that is True for those
        records where the first n digits match those identified as top N anomalies

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

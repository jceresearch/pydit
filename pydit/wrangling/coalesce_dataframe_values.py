"""Creates a new column with the top N most frequent values and the rest are replaced by Other """

import logging

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def coalesce_values(
    df_in,
    cols,
    top_n_values_to_keep=10,
    translation_dict=None,
    other_label="OTHER",
    case_insensitive=True,
    dropna=True,
):
    """
    Creates a new column with the top N most frequent values and the rest are replaced by Other.

    Also can take a translation dictionary to do the manual translation prior
    to applying that top N limit.

    Parameters
    ----------
    df_in : pandas.DataFrame
        The dataframe to clean up
    cols : list
        The column names to coalesce
    top_n_values_to_keep : int, optional, default 10
        The number of top values to keep.
    translation_dict : dict, optional, default None
        A dictionary to use for manual translation/coalescing.
    other_label : str or int, optional, default "OTHER"
        The label to use for the other values.
    case_insensitive : bool, optional, default True
        Whether to do a case insensitive comparison.
    dropna : bool, optional, default True
        Whether to ignore np.nan values.
        If False, NA values will be treated as a category with "N/A" as the label.

    Returns
    -------
    pandas.DataFrame
        Pandas DataFrame with new column with coalesced values.

    """

    # We ensure we create a copy so not to mutate the original DataFrame
    df = df_in.copy()

    if not isinstance(cols, (list, str)):
        raise TypeError("cols must be a string or a list")

    if isinstance(cols, str):
        if cols == "":
            raise ValueError("Column must be a non-empty string or a list")
        cols = [cols]

    if len(cols) == 0:
        raise ValueError("Cols must be a non-empty list")

    if not set(cols).issubset(df.columns):
        raise ValueError("Not all columns found in DataFrame")
    if isinstance(other_label, str):
        flag_str_label = True
    elif isinstance(other_label, int):
        flag_str_label = False
    else:
        raise TypeError("other_label must be a string or an integer")

    if top_n_values_to_keep <= 0:
        raise ValueError("top_n_values_to_keep must be greater than 0")

    if len(cols) == 1:
        col_root = cols[0]
        df[col_root + "_source"] = df[cols[0]].copy()
    else:

        def concat_categories(r, cols):
            try:
                v = "_".join([str(v) for v in r[cols].values])
            except Exception:
                v = np.NAN
            return v

        col_root = "_".join(cols)
        df[col_root + "source"] = df.apply(lambda r: concat_categories(r, cols), axis=1)

    if translation_dict:
        df[col_root + "_translate"] = df[col_root + "_source"].apply(
            lambda v: translation_dict[v] if v in translation_dict else other_label,
        )
        col_output = col_root + "_translate"
    else:
        col_output = col_root + "_source"
    logger.info("Processing column %s", cols)
    logger.info("Will keep top %s values", top_n_values_to_keep)
    logger.info("Case insensitive: %s", case_insensitive)

    if case_insensitive:
        try:
            df[col_output] = df[col_output].str.upper()
        except Exception:
            pass

    if not dropna:
        df[col_output] = df[col_output].fillna("N/A")

    if flag_str_label:
        df[col_output] = df[col_output].astype(str).str.strip().str.upper()

    val_counts = df[col_output].value_counts().reset_index()
    val_counts_top_n = list(val_counts[0:top_n_values_to_keep][col_output])
    df[col_root + "_collapsed"] = df.apply(
        lambda r: r[col_output] if r[col_output] in val_counts_top_n else other_label,
        axis=1,
    )
    logger.info("Unique values after: %s", len(df[col_root + "_collapsed"].unique()))
    logger.info("Value counts:\n%s", df[col_root + "_collapsed"].value_counts())
    return df


if __name__ == "__main__":
    data = {
        "a": [
            "Label 1",
            "Label 2",
            "Label 2",
            "Label 3",
            "Label 3",
            "Label 3",
            "Label 4",
        ],
        "b": [1, 2, 2, 3, 3, 3, 4],
        "c": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        "d": [1, 2, 3, 4, 5, 6, 7],
        "e": ["Red", "Red", "Red", "Red", "Red", "Red", "Red"],
        "f": ["a", "b", "c", "d", "e", "f", "g"],
        "g": ["a", "a", "a", "b", "b", "c", np.nan],
        "h": [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        "i": [np.nan, np.nan, np.nan, "b", "b", "c", "d"],
    }
    df = pd.DataFrame(data)

    vc = df["a"].value_counts().reset_index()
    print(vc)
    value_counts_topN = list(vc[0:2]["a"])
    print(value_counts_topN)

    result = coalesce_values(df, "a", top_n_values_to_keep=2)
    print(result)

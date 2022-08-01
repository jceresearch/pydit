"""Creates a new column with the top N most frequent values and the rest are replaced by Other """

import logging

import numpy as np

logger = logging.getLogger(__name__)


def coalesce_values(
    df_in, cols, top_n_values_to_keep=10, translation_dict=None, other_label="OTHER"
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

    Returns
    -------
    pandas.DataFrame
        Pandas DataFrame with new column with coalesced values.

    """

    # We ensure we create a copy so not to mutate the original DataFrame
    df = df_in.copy()

    if isinstance(cols, str):
        if not cols in df.columns:
            raise ValueError(f"Column {cols} not found in DataFrame")
        else:
            col = cols
    else:
        if not isinstance(cols, list):
            raise TypeError("cols must be a string or a list")

        check = all(item in df.columns for item in cols)
        if not check:
            raise ValueError(
                "Not all columns provided are in the dataframe, check for typos"
            )
        if len(cols) == 1:
            col = cols[0]
        elif len(cols) > 1:

            def concat_categories(r, cols):
                try:
                    v = "_".join([str(v) for v in r[cols].values])
                except Exception:
                    v = np.NAN
                return v

            col = "_".join(cols)
            df[col] = df.apply(lambda r: concat_categories(r, cols), axis=1)

        else:
            return "empty list"

    if isinstance(other_label, str):
        flag_str_label = True
    elif isinstance(other_label, int):
        flag_str_label = False
    else:
        raise TypeError("other_label must be a string or an integer")

    if top_n_values_to_keep <= 0:
        raise ValueError("top_n_values_to_keep must be greater than 0")

    if translation_dict:
        df[col + "_translate"] = df.apply(
            lambda r: translation_dict[r[col]]
            if r[col] in translation_dict
            else other_label,
            axis=1,
        )
        col = col + "_translate"

    logger.info("Processing column %s", col)
    logger.info("Unique values before: %s", len(df[col].unique()))
    logger.info(
        "Top %s values to keep:\n %s",
        top_n_values_to_keep,
        df[col].value_counts().nlargest(top_n_values_to_keep).index,
    )
    value_counts = df[col].value_counts().reset_index()
    value_counts_topN = list(value_counts[0:top_n_values_to_keep]["index"])
    if flag_str_label:
        df[col + "_collapsed"] = df.apply(
            lambda r: str.strip(str.upper(str(r[col])))
            if r[col] in value_counts_topN
            else other_label,
            axis=1,
        )
    else:
        df[col + "_collapsed"] = df.apply(
            lambda r: r[col] if r[col] in value_counts_topN else other_label,
            axis=1,
        )
    logger.info("Unique values after: %s", len(df[col + "_collapsed"].unique()))
    logger.info("Value counts:\n%s", df[col + "_collapsed"].value_counts())
    return df

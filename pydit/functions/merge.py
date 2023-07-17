"""Module to merge dataframes with prefixes or suffixes for all fields not just collissions.

"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def merge_smart(df1, df2, rename_merge_key=False, **kwargs):
    """Merge two dataframes, with prefixes or suffixes for all fields not just collissions.

    Parameters
    ----------
    df1 : pandas.DataFrame
        The left dataframe
    df2 : pandas.DataFrame
        The right dataframe
    rename_merge_key : bool, optional, default False
        If True, the key columns will be renamed with the suffixes or prefixes
    kwargs : the keyword arguments to pass to pandas.DataFrame.merge()
        See https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html

    Returns
    -------
    pandas.DataFrame
        A new merged dataframe

    """

    merge_args = kwargs.copy()
    dfa = df1.copy()
    dfb = df2.copy()
    if on := merge_args.pop("on", None):
        left_on = on
        right_on = on
    else:
        left_on = merge_args.pop("left_on", None)
        right_on = merge_args.pop("right_on", None)
    if not (left_on and right_on):
        raise ValueError("Missing: on, left_on or right_on")

    left_on = [*left_on]
    right_on = [*right_on]

    if suff := merge_args.pop("suffixes", None):
        if suff[0]:
            cols = []
            for c in dfa.columns:
                if not rename_merge_key and c in left_on:
                    cols.append(c)
                else:
                    cols.append(str(c) + str(suff[0]))
            if rename_merge_key:
                left_on = [v + str(suff[0]) for v in left_on]
            dfa.columns = cols
        if suff[1]:
            cols = []
            for c in dfb.columns:
                if (not rename_merge_key) and (c in right_on):
                    cols.append(c)
                else:
                    cols.append(str(c) + str(suff[1]))
            if rename_merge_key:
                right_on = [v + str(suff[1]) for v in right_on]
            dfb.columns = cols

    if pref := merge_args.pop("prefixes", None):
        if pref[0]:
            cols = []
            for c in dfa.columns:
                if (not rename_merge_key) and (c in left_on):
                    cols.append(c)
                else:
                    cols.append(str(pref[0] + str(c)))

            if rename_merge_key:
                left_on = [str(pref[0]) + str(v) for v in left_on]
            dfa.columns = cols
        if pref[1]:
            cols = []
            for c in dfb.columns:
                if (not rename_merge_key) and (c in right_on):
                    cols.append(c)
                else:
                    cols.append(str(pref[1]) + str(c))
            if rename_merge_key:
                right_on = [str(pref[1]) + str(v) for v in right_on]
            dfb.columns = cols
    dfres = pd.merge(dfa, dfb, left_on=left_on, right_on=right_on, **merge_args)
    return dfres


def merge_outer_and_split(
    dffact,
    dfdim,
    on=None,
    left_on=None,
    right_on=None,
    suffixes=(None, None),
    excel_output=None,
):
    """Merge two dataframes, and keep the joinable 1:1 or 1:n and the nan or
    unmatched are returned in separate dataframes or Excel sheets.
    Under the bonnet it will
    - filter nulls from the key columns (and store in a separate dataframe
    to return those exceptions
    - on the clean version will do an outer merge with indicator=True
    - will split the results into the 3 dataframes (both, left, right)
    - will write the results to an Excel file if specified

    It will also check for duplicates in the key columns and exit if found in
    the right dataframe (presumed to be a dimension/master file ) or warn
    if they are in the left dataframe (presumably the transaction/fact file).


    Parameters
    ----------
    dffact : pandas.DataFrame
        The left dataframe
    dfdim : pandas.DataFrame
        The right dataframe
    left_on : list
        The list of key columns to join on in the left dataframe
    right_on : list
        The list of key columns to join on in the right dataframe
    suffixes : tuple, optional
        The suffixes to use for the left and right dataframes, by default (None,None)
    excel_output : str, optional
        The path to an Excel file to write the results to, by default None

    Returns
    -------
    tuple
        A tuple of dataframes, (both, left, right, left_na, right_na)
        both : the rows that matched
        left : the rows that matched but had nulls in the right dataframe
        right : the rows that matched but had nulls in the left dataframe
        left_na : the rows that have nulls in the specified key columns in the left dataframe
        right_na : the rows that have nulls in the specified key columns in the right dataframe

    Raises
    ------
    ValueError
        If the right dataframe has duplicates in the key columns

    """
    if on is not None:
        left_on = on
        right_on = on
    elif left_on is None or right_on is None:
        raise ValueError("You must specify either on or left_on and right_on")
    else:
        pass

    dffact_na = dffact[dffact[left_on].isnull()]
    dfdim_na = dfdim[dfdim[right_on].isnull()]
    dffact_notna = dffact.dropna(subset=left_on)
    dfdim_notna = dfdim.dropna(subset=right_on)
    # check if dropna creates a copy or is some sort of view/filter
    logger.info(f"Detected {dffact_na.shape[0]} null key values in the left dataframe")
    logger.info(f"Detected {dfdim_na.shape[0]} null key values in the right dataframe")
    if (dupe_count := dfdim_notna.duplicated(subset=right_on).values.sum()) > 0:
        raise ValueError(
            f"Right dataframe has {dupe_count} duplicates on field {right_on}, fix and retry"
        )
    if (dupe_count := dffact_notna.duplicated(subset=left_on).values.sum()) > 0:
        print(
            f"For info , your left dataframe has {dupe_count} duplicates on field {right_on}, should be ok if it is a fact table"
        )
    dfouter = pd.merge(
        dffact_notna,
        dfdim_notna,
        how="outer",
        left_on=left_on,
        right_on=right_on,
        indicator=True,
        suffixes=suffixes,
    )
    dfboth = dfouter[dfouter["_merge"] == "both"].drop(columns=["_merge"])
    dfleft = dfouter[dfouter["_merge"] == "left_only"].drop(columns=["_merge"])
    dfright = dfouter[dfouter["_merge"] == "right_only"].drop(columns=["_merge"])
    if excel_output:
        with pd.ExcelWriter(excel_output) as writer:
            dfboth.to_excel(writer, sheet_name="both", index=False)
            dfleft.to_excel(writer, sheet_name="left_only", index=False)
            dfright.to_excel(writer, sheet_name="right_only", index=False)
            dffact_na.to_excel(writer, sheet_name="left_na", index=False)
            dfdim_na.to_excel(writer, sheet_name="right_na", index=False)
    return dfboth, dfleft, dfright, dffact_na, dfdim_na

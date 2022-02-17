""" Validation functions"""

import logging
from datetime import timedelta
from xmlrpc.client import FastParser

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_string_dtype, is_numeric_dtype
from pandas import Series, DataFrame
import numpy as np


logger = logging.getLogger(__name__)


def check_duplicates(df, columns=None, keep=False, ascending=None):
    """
    Duplicate analysis
    Args:
        df (DataFrame): pandas dataframe
        
        columns (list, optional): column(s) to check between square brackets, 
        even if it is one column only, if multiple columns provided
        the check is combined duplicates, exactly as pandas duplicated().
        
        keep ('first','last' or False, optional): Argument for pandas df.duplicated() method.
        Defaults to 'first'.
        
        ascending (True, False or None, optional): Argument for DataFrame.value_counts()
        Defaults to None.

    Returns:
        DataFrame or None: Returns the DataFrame with the duplicates.
        If no duplicates, returns None.
    """

    if not isinstance(df, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        # TODO: #17 Add support for Series in the duplicate check
        return
    if not isinstance(columns, list):
        logger.error("Expecting a list, even a list of one element")
        return
    else:
        if not columns:
            cols = df.columns
        else:
            cols = columns

    fields = ",".join(cols)
    df_duplicates = df[df.duplicated(subset=cols, keep=keep)]
    print(
        "Duplicates in",
        fields,
        "(keep=",
        keep,
        "):",
        len(df_duplicates),
        " of population: ",
        len(df),
    )
    if len(df_duplicates) == 0:
        return None
    else:
        if ascending is True:
            print("Ascending")
            df_ret = df_duplicates.sort_values(cols, ascending=True)
        elif ascending is False:
            print("Descending")
            df_ret = df_duplicates.sort_values(cols, ascending=False)
        else:
            print("No sort")
            df_ret = df_duplicates

    return df_ret


def check_sequence(obj_in, col=""):
    """ to check the numerical sequence of a series including dates
    and numbers within an text ID """
    # TODO: #16 Develop tests and check the fullrng.issubset(unique) approach is correct
    if col:
        obj = obj_in[col]
    else:
        if isinstance(obj_in, Series):
            obj = obj_in.copy()
        elif isinstance(obj_in, DataFrame):
            obj = obj_in.iloc[:, 0].copy()
        elif isinstance(obj_in, list):
            obj = pd.Series(obj_in)
        else:
            logging.error("Type not recognised")
            return None
    typ = obj.dtype
    if "int" in str(typ):
        unique = set([i for i in obj[pd.notna(obj)]])
        fullrng = set(range(min(unique), max(unique) + 1))
        diff = fullrng.difference(unique)
        if diff:
            print("Missing in sequence: ", list(diff)[0:10])
            return list(diff)
        else:
            print("Full sequence")
            return []
    elif is_datetime(obj):
        unique = set([i.date() for i in obj[pd.notna(obj)]])
        fullrng = set(
            pd.date_range(
                min(unique), max(unique) - timedelta(days=1), freq="d"
            ).to_list()
        )
        diff = fullrng.difference(unique)
        if diff:
            print(
                len(diff),
                " missing, first ",
                min(len(diff), 10),
                ":",
                list(diff)[0:10],
            )
            working_days = [wd for wd in diff if wd.weekday() < 5]
            print(
                len(working_days),
                " missing working days",
                min(len(diff), 10),
                ":",
                list(diff)[0:10],
            )

            return list(diff)
        else:
            print("Full sequence")
            return []
    elif typ == "object":
        values = obj[pd.notna(obj)]
        numeric_chars = values.str.replace(r"[^0-9^-^.]+", "", regex=True)
        numeric_chars_no_blank = numeric_chars[numeric_chars.str.len() > 0]
        numeric = pd.to_numeric(
            numeric_chars_no_blank, errors="coerce", downcast="integer"
        )
        if pd.api.types.is_float_dtype(numeric):
            # we have floats so it wont likely be a sequence
            print("Contains floats, no sequence to check")
        else:
            unique = set(numeric)
            print(list(unique))
            if unique:
                fullrng = set(range(min(unique), max(unique)))
                diff = fullrng.difference(unique)
                if diff:
                    print(
                        len(diff), " missing in sequence, fist 10:", list(diff)[0:10],
                    )
                    return list(diff)
                else:
                    print("Full sequence")
                    return []
            else:
                print("No sequence to check")
                return None
    return


def check_blanks(
    df_in, columns=None, zeroes=True, null_strings_and_spaces=True, totals_only=False,
):
    """ Reports on blanks in the Dataframe and optionally saves to an excel file

    Args:
        df_in ([type]): [description]
        columns ([type], optional): [description]. Defaults to None.
        zeroes (bool, optional): [description]. Defaults to True.
        null_strings_and_spaces (bool, optional): [description]. Defaults to True.
        totals_only (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """

    if not isinstance(df_in, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        return
    df = df_in.copy()
    if columns and isinstance(columns, list):
        cols = columns
    elif not columns:
        cols = df.columns
    else:
        logger.error("Expecting a list, even a list of one element")
        return

    fields = ",".join(cols)
    logger.info("Checking for blanks in %s", fields)
    total_results = []
    for c in cols:
        if is_numeric_dtype(df[c]) and zeroes:
            df[c + "_blanks"] = (pd.isna(df[c])) | (df[c] == 0)
        elif is_string_dtype(df[c]) and null_strings_and_spaces:
            logger.debug("Checking for spaces and nullstring too in %s", c)
            df[c + "_blanks"] = (pd.isna(df[c])) | (df[c].str.strip() == "")
        else:
            logger.debug("Checking just for NaN or NaT in %s", c)
            df[c + "_blanks"] = pd.isna(df[c])
        total_results.append(df[c + "_blanks"].sum())
    new_cols = [c + "_blanks" for c in cols]
    df["has_blanks"] = np.any(df[new_cols], axis=1)

    print("Total blanks found in each columns:", total_results)

    if totals_only:
        return total_results

    return df


def check_referential_integrity(df1, df2, key1, key2):
    """' check whether two dataframes are one-to-one , many-to-one"""
    set1 = set(df1[key1])
    key1_is_unique= ( len(set1) == list(df1[key1]))
    set2 = set(df2[key2])
    key2_is_unique = (len(set2) == list(df2[key2]))
    two_sets_equal = (set1 == set2)
    set1_in_set2=set1.issubset(set2)
    set2_in_set1=set2.issubset(set1)
    if two_sets_equal:
        print("key1 and key2 unique values are the same")
        if key1_is_unique and key2_is_unique:    
            print("One to one and match fully")
            return "1-to-1 strict"   
        elif not key1_is_unique and not key2_is_unique:
            print ("Both keys have duplicates, many to many")
            return "m-to-m strict"
        elif key1_is_unique and not key2_is_unique:
            return "1-to-m strict, key2 is fact"
        elif key2_is_unique and not key1_is_unique:
            return "m-to-1 strict key1 is fact"
        
    else:            
        if set1_in_set2:
            
            if key2_is_unique:
                print("key2 is dimension, also has values not appearing in key1")
                return "m-to-1 loose"
            else:
                #key2 has duplicates, so it is a fact table
                if key1_is_unique:
                    print("key1 is possible dimension (no duplicates) but misses values in key2")
                    return "1-to-m with incomplete key1"
                else:
                    print("key1 and key2 have both duplicates, key1 is possibly fact table (subset of key2)")
                    return "m-to-1 with duplicate keys in both"
        else:
            


def main():
    """ Validation functions"""


if __name__ == "__main__":
    main()
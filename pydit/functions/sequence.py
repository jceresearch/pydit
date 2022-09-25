""" Module to check for numerical sequence of DataFrame column or Series
"""

import logging
from datetime import timedelta

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas import Series, DataFrame


logger = logging.getLogger(__name__)


def check_sequence(obj_in, col=None):
    """ Checks the numerical sequence of a series including dates
    
    If a text column is provided it will attempt to convert to numeric after
    extacting any non numeric chars.

    Parameters
    ----------
    obj_in : list, pandas.Series or pandas.DataFrame
        The list, series or dataframe to check
    col : str
        The column name to check, if a DataFrame is provided.


    Returns
    -------
    list
        A list of the missing values in the series

    """

    # TODO: #32 check_sequence() refactor to do better input validation and error handling and simpler flow control

    if col:
        try:
            obj = obj_in[col]
        except:
            raise ValueError("Column not found in dataframe") 
    else:
        if isinstance(obj_in, Series):
            obj = obj_in.copy()
        elif isinstance(obj_in, list):
            obj = pd.Series(obj_in)
        else:
            raise TypeError("Input needs to be a DataFrame, List or Series")
            
    typ = obj.dtype
    if "int" in str(typ):
        unique = set([i for i in obj[pd.notna(obj)]])
        fullrng = set(range(min(unique), max(unique) + 1))
        diff = fullrng.difference(unique)
        if diff:
            print(len(diff), " missing in sequence. First 10:", list(diff)[0:10])
            return list(diff)
        else:
            print("Full sequence")
            return []
    elif is_datetime(obj):
        unique = set([i.date() for i in obj[pd.notna(obj)]])
        fullrng = pd.date_range(min(unique), max(unique) + timedelta(days=1), freq="d")
        fullrng = set([i.date() for i in fullrng])
        diff = fullrng.difference(unique)
        if diff:
            print(
                len(diff), " missing, first 10:", list(diff)[0:10],
            )
            working_days = [wd for wd in diff if wd.weekday() < 5]
            print(
                len(working_days), " missing working days:", list(diff)[0:10],
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
                        len(diff), " missing in sequence")
                    print("fist 10:", list(diff)[0:10])
                    return list(diff)
                else:
                    print("Full sequence")
                    return []
            else:
                print("No sequence to check")
                return None
    return
    
    
group_gaps(gap_list):  
    try:
        def to_ranges(iterable):
            iterable = sorted(set(iterable))
            for key, group in itertools.groupby(enumerate(iterable), lambda t: t[1] - t[0]):
                group = list(group)
                yield [group[0][1], group[-1][1],group[-1][1]-group[0][1]+1]
        df_grouped = pd.DataFrame.from_records(list(to_ranges(gap_list)),columns=["start","end","count"])
    except TypeError:
        print("Grouping only works for integers for now")
        return
    return df_grouped


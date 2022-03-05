" Validation functions" ""

import logging
from datetime import timedelta

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas import Series, DataFrame


logger = logging.getLogger(__name__)


def check_sequence(obj_in, col=""):
    """ to check the numerical sequence of a series including dates
    and numbers within an text ID """
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

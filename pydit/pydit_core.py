""" core library of convenience tools"""
from datetime import datetime
import re
import pickle
import os
from zlib import DEFLATED
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime


class Tools(object):
    """
    Main class to hold parameters and core functions
    PYDIT a toolset for processing data specifically targetting internal audit
needs, which focuses on simplicity and generating audit trails of everyghing
this module is the main library
"""

    def __init__(self, temp_path="", output_path="", input_path=""):
        if temp_path == "":
            self.temp_path = "."
        else:
            self.temp_path = temp_path
        if output_path == "":
            self.output_path = "."
        else:
            self.output_path = output_path
        if input_path == "":
            self.input_path = "."
        else:
            self.intput_path = input_path

    def _hello(self):
        print("Hello World")

    def _dataframe_to_code(self, df):
        """ utility function to convert a dataframe to a piece of code
        that one can include in a test script or tutorial. May need extra tweaks
        or imports , e.g. from pandas import Timestamp to deal with dates, etc.
        """
        data = np.array2string(df.to_numpy(), separator=", ")
        data = data.replace(" nan", " float('nan')")
        data = data.replace(" NaT", " pd.NaT")
        cols = df.columns.tolist()
        return f"""df = pd.DataFrame({data}, columns={cols})"""

    def _deduplicate_list(self, list_to_deduplicate):
        "Deduplicates a list"
        if not list_to_deduplicate:
            return []
        newlist = list_to_deduplicate.copy()
        for i, el in enumerate(list_to_deduplicate):
            dupes = list_to_deduplicate.count(el)
            if dupes > 1:
                for j in range(dupes):
                    pos = [i for i, n in enumerate(list_to_deduplicate) if n == el][j]
                    if j == 0:
                        newlist[pos] = str(el)
                    else:
                        newlist[pos] = str(el) + "_" + str(j + 1)
            else:
                newlist[i] = str(el)
        return newlist

    def clean_columns_names(self, df):
        """ Cleanup the column names of a Pandas dataframe
        e.g. removes non alphanumeric chars, _ instead of space, perc instead
        of %, strips trailing spaces, converts to lowercase
        """
        df.columns = df.columns.str.replace(r"%", "perc", regex=True)
        df.columns = df.columns.str.replace(r"[^a-zA-Z0-9]", " ", regex=True)
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.replace(" +", "_", regex=True)
        df.columns = df.columns.str.lower()
        if len(df.columns) != len(set(df.columns)):
            print("Identified some duplicate columns, renaming them")
            new_cols = self._deduplicate_list(list(df.columns))
            df.columns = new_cols
        if len(df.columns) != len(set(df.columns)):
            raise ValueError("Duplicated column names remain!!! check what happened")
        return True

    def clean_string(self, t, keep_dot=False, space_to_underscore=True, case="lower"):
        """Sanitising text:
        - Keeps only [a-zA-Z0-9]
        - Optional to retain dot
        - Spaces to underscore
        - Removes multiple spaces , trims
        - Optional to lowercase
        The purpose is just for easier typing, exporting, saving to filenames.
        Args:
            t (string]): string with the text to sanitise
            keep_dot (bool, optional): Keep the dot or not. Defaults to False.
            space_to_underscore (bool, optional): False to keep spaces. Defaults to True.
            case= "lower" (default), "upper" or "keep"(unchanged)
        Returns:
            string: cleanup string
        """
        r = ""
        if case == "lower":
            r = str.lower(str(t))
        elif case == "upper":
            str.upper(str(t))
        elif case == "keep":
            r = str(t)
        if t:
            if keep_dot is True:
                r = re.sub(r"[^a-zA-Z0-9.]", " ", r)
            else:
                r = re.sub(r"[^a-zA-Z0-9]", " ", r)
            r = r.strip()
            if space_to_underscore is True:
                r = re.sub(" +", "_", r)
            else:
                r = re.sub(" +", " ", r)
        return r

    def load(self, file_name, source="auto"):
        """ load a file with extra features and assuming some standardisation
        """
        obj = None
        if source == "input":
            if os.path.isfile(self.input_path + file_name):
                full_name = self.input_path + file_name
        if source == "output":
            if os.path.isfile(self.output_path + file_name):
                full_name = self.output_path + file_name
        if source == "temp":
            if os.path.isfile(self.temp_path + file_name):
                full_name = self.temp_path + file_name
        if source == "auto":
            if os.path.isfile(self.temp_path + file_name):
                full_name = self.temp_path + file_name
            elif os.path.isfile(self.temp_path + file_name):
                full_name = self.input_path + file_name
            elif os.path.isfile(self.output_path + file_name):
                full_name = self.input_path + file_name
            else:
                print("No file found in any of the possible sources")
                return obj

        if ".pickle" in full_name:
            try:
                with open(full_name, "rb") as handle:
                    obj = pickle.load(handle)
                    print(
                        "Loaded pickle from: " + full_name,
                        " Size:",
                        round((handle.tell() / 1024) / 1024, 1),
                        " MB",
                    )
            except Exception as e:
                print(e)
        if ".xlsx" in full_name:
            try:
                obj = pd.read_excel(full_name)
                print(full_name)
            except Exception as e:
                print(e)
        if ".csv" in full_name:
            try:
                obj = pd.read_csv(full_name)
                print(full_name)
            except Exception as e:
                print(e)
        if isinstance(obj, pd.DataFrame):
            print("Shape:", obj.shape)
            print(list(obj.columns))
        else:
            try:
                print(len(obj))
            except Exception:
                pass
        print(datetime.now())
        return obj

    def check_dataframe(self, df):
        """[summary]

        Args:
            df ([type]): [description]

        Returns:
            [type]: [description]
        """

        # df=in_df.copy() # if we needed to do transformations create a copy

        if isinstance(df, pd.DataFrame):
            dtypes = df.dtypes.to_dict()
        else:
            return

        col_metrics = []
        for col, typ in dtypes.items():
            metrics = {}
            metrics["column"] = col
            metrics["dtype"] = typ
            metrics["records"] = len(df[col])
            metrics["count_unique"] = len(set(df[pd.notna(df[col])][col]))
            metrics["nans"] = len(df[pd.isnull(df[col])])
            if metrics["count_unique"] < 5:
                value_counts_series = df[col].value_counts(dropna=False)
                metrics["value_counts"] = value_counts_series.to_dict()
            else:
                metrics["value_counts"] = []
            if "float" in str(typ):
                print("float")
                metrics["max"] = max(df[col])
                metrics["min"] = min(df[col])
                metrics["sum"] = sum(df[col])
                metrics["sum_abs"] = sum(abs(df[col]))
                # TODO: possibly add hist/sparkline data to further add to the profiling
            elif "int" in str(typ):
                metrics["max"] = max(df[col])
                metrics["min"] = min(df[col])
                metrics["sum"] = sum(df[col])
                metrics["sum_abs"] = sum(abs(df[col]))
            elif is_datetime(df[col]):
                metrics["max"] = max(df[col])
                metrics["min"] = min(df[col])
            elif typ == "object":
                values = df[pd.notna(df[col])][col]
                numeric_chars = values.str.replace(
                    r"[^0-9^-^.]+", "", regex=True
                )  # TODO: refactor this regex, currently very simplistic works only for clean id sequences, e.g. double dots
                numeric_chars_no_blank = numeric_chars[numeric_chars.str.len() > 0]
                numeric = pd.to_numeric(numeric_chars_no_blank, errors="coerce")
                if len(numeric) > 0:
                    metrics["max"] = max(numeric)
                    metrics["min"] = min(numeric)
                metrics["empty_strings"] = len(df[df[col].eq("")])
            col_metrics.append(metrics)
        return pd.DataFrame(col_metrics)


def main():
    """ main routine, currently not used """


if __name__ == "__main__":
    main()

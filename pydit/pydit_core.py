""" core library of convenience tools"""
from datetime import datetime, timedelta
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

    def version(self):
        """ version information"""
        return "V.01"

    def about(self):
        """ About information"""
        about_text = "Pydit - Tools for internal auditors\n \
        Version: 1.01\n \
        Released:Jan 2022 "
        return about_text

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

    def _save_to_excel(self, df, file_name, sheet_name=None):
        """ Internal routine to save a dataframe to excel with sensible options"""
        file_name = file_name.replace(r"\.xlsx*", "", regex=True)
        if self.output_path[-1] == "/" or self.output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"

        full_file_name = self.output_path + separator + file_name + ".xlsx"
        if not sheet_name:
            sheet_name = file_name[:15]
        try:
            df.to_excel(full_file_name, sheet_name=sheet_name, index=False)
        except Exception as e:
            print(e)
            return None
        return full_file_name

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

    def save(self, obj, filename, bool_also_pickle=False):
        """Save the dataframe in excel, pickle or csv with some extra audit trails
        as well as choosing the destination based on size

        Args:
            obj ([type]): [description]
            filename ([type]): [description]
            bool_also_pickle (bool, optional): [description]. Defaults to False.
        """

        flag = False
        flag_to_csv_instead = False
        start_time = datetime.now()
        stem_name = re.sub("\.[a-zA-Z0-9_]{2,}$", "", filename)
        if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
            if ".xlsx" in filename:
                if obj.shape[0] < 300000:
                    print("Saving to an excel file:", output_path + filename)
                    obj.to_excel(
                        output_path + filename,
                        index=False,
                        sheet_name=stem_name,
                        freeze_panes=(1, 0),
                    )
                    flag = True
                else:
                    flag_to_csv_instead = True
                    print("Too big for excel!")
                if bool_also_pickle:
                    print(
                        "Saving also to a pickle file:",
                        temp_path + stem_name + ".pickle",
                    )
                    obj.to_pickle(temp_path + stem_name + ".pickle")
            if ".csv" in filename or flag_to_csv_instead == True:
                print("Saving to csv:", temp_path + stem_name + ".csv")
                obj.to_csv(
                    temp_path + filename,
                    index=False,
                    quotechar='"',
                    quoting=csv.QUOTE_ALL,
                )
                flag = True
            if ".pickle" in filename or bool_also_pickle == True:
                print("Saving to pickle format in: ", temp_path + filename)
                obj.to_pickle(temp_path + stem_name + ".pickle")
                flag = True
            if flag:
                print("(rows, columns) :", obj.shape)
                print("Saved columns:", list(obj.columns))
                print(
                    "Finished:",
                    f"{datetime.now():%Y-%m-%d %H:%M:%S}",
                    " - ",
                    round((datetime.now() - start_time).total_seconds() / 60.0, 2),
                    " mins",
                )
            else:
                print("Name not recognised, nothing saved")
        else:
            if ".pickle" in filename:
                with open(temp_path + filename, "wb") as handle:
                    pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print(
                        "Saved pickle to " + filename,
                        round((handle.tell() / 1024) / 1024, 1),
                        " MB",
                    )
                    print(datetime.now())
            else:
                print("Nothing saved, format not recognised")

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

    def check_duplicates(
        self, df, columns=None, keep="first", ascending=None, output_file=None
    ):
        """
        Bundles duplicate analysis, common steps like checking duplicates
        showing the total numbers, showing the actual duplicates, exporting
        to excel the offending duplicates
        Args:
            df (DataFrame): pandas dataframe
            columns (str, list or int, optional): column(s) to check, if more
            than one column is provided the check is combined duplicates, exactly as pandas duplicated().
            keep ('first','last' or False, optional): Argument for pandas df.duplicated() method.
            Defaults to 'first'.
            ascending (True, False or None, optional): Argument for pandas df.value_counts() Defaults to None.

        Returns:
            DataFrame or None: Returns the DataFrame with the duplicates.
            If no duplicates, returns None.
        """
        if not isinstance(df, pd.DataFrame):
            return
        if isinstance(columns, str):
            cols = [columns]
        if isinstance(cols, int):
            cols = [df.columns[columns]]
        if not columns:
            fields = "entire record"
            cols = list(df.columns)
        else:
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

        if output_file:
            self._save_to_excel(df_ret, output_file)

        return df_ret

    def check_sequence(self, df):
        """ to check the numerical sequence of a series including dates
        and numbers within an text ID """
        dtypes = df.dtypes.to_dict()
        for col, typ in dtypes.items():
            print(col, typ)
            if "int" in str(typ):
                unique = set([i for i in set(df[pd.notna(df[col])][col])])
                fullrng = range(min(unique), max(unique) + 1)
                if unique.issubset(fullrng):
                    print("Full sequence")
                else:
                    diff = unique.difference(fullrng)
                    print("Missing in sequence: ", list(diff)[0:10])
            elif is_datetime(df[col]):
                unique = set([i.date() for i in set(df[pd.notna(df[col])][col])])
                fullrng = set(
                    pd.date_range(
                        min(unique), max(unique) - timedelta(days=1), freq="d"
                    ).to_list()
                )
                if unique.issubset(fullrng):
                    print("Full sequence")
                else:
                    diff = unique.difference(fullrng)
                    print(
                        len(diff),
                        " missing in sequence, first ",
                        min(len(diff), 10),
                        ":",
                        list(diff)[0:10],
                    )
            elif typ == "object":
                values = df[pd.notna(df[col])][col]
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
                        if unique.issubset(fullrng):
                            print("Full sequence")
                        else:
                            diff = unique.difference(fullrng)
                            print(
                                len(diff),
                                " missing in sequence, fist 10:",
                                list(diff)[0:10],
                            )
                    else:
                        print("No sequence to check")
        return


def main():
    """ main routine, currently not used """


if __name__ == "__main__":
    main()

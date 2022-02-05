""" core library of convenience tools"""

from datetime import datetime, timedelta
import re
import pickle
import os
import logging
from pathlib import Path, PureWindowsPath
import csv
import numpy as np
import pandas as pd
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_string_dtype, is_numeric_dtype
from pandas import Series, DataFrame

logger = logging.getLogger(__name__)


class Tools(object):
    """
    Main class to hold parameters and core functions
    PYDIT a toolset for processing data specifically targetting internal audit
needs, which focuses on simplicity and generating audit trails of everyghing
this module is the main library
"""

    def __init__(
        self, temp_path="", output_path="", input_path="", max_rows_to_excel=200000
    ):
        """ initialise configuration"""
        # TODO: #14 check that the folders exist, see to that this check is done every time it is updated
        self.temp_path = temp_path
        self.output_path = output_path
        self.input_path = input_path
        self.max_rows_to_excel = max_rows_to_excel

    @property
    def max_rows_to_excel(self):
        """Maximum number of rows to save to Excel, past that CSV or Pickle"""
        return self._MAX_ROWS_TO_EXCEL

    @max_rows_to_excel.setter
    def max_rows_to_excel(self, n):
        """ Setter for max_rows_to_excel"""
        if n > 999999 or n < 0:
            raise Exception("Rows number must be positive and less than 1,000,000")
        self._MAX_ROWS_TO_EXCEL = n

    @property
    def temp_path(self):
        """'Where do we save the temp files, typically for large files, local cache"""
        return self._temp_path

    @temp_path.setter
    def temp_path(self, path):
        if not path:
            path = "./"
        else:
            if not path[-1] == "/":
                path = path + "/"
        self._temp_path = path

    @property
    def input_path(self):
        return self._input_path

    @input_path.setter
    def input_path(self, path):
        if not path:
            path = "./"
        else:
            if not path[-1] == "/":
                path = path + "/"
        self._input_path = path

    @property
    def output_path(self):
        return self._output_path

    @output_path.setter
    def output_path(self, path):
        if not path:
            path = "./"
        else:
            if not path[-1] == "/":
                path = path + "/"
        self._output_path = path

    @property
    def version(self):
        """ version information"""
        return "V.01"

    @property
    def about(self):
        """ About information"""
        about_text = "Pydit - Tools for internal auditors\n \
        Version: 1.01\n \
        Released:Jan 2022 "
        return about_text

    def config(self):
        """returns current configuration"""
        conf = {
            "temp_path": self.temp_path,
            "output_path": self.output_path,
            "input_path": self.input_path,
            "max_rows_to_excel": self.max_rows_to_excel,
        }
        logger.info("\n" + "\n".join("{}\t{}".format(k, v) for k, v in conf.items()))
        return conf

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

    def _stem_name(self, file_name):
        """ find the core name of a provided string with a filename and lowers case"""
        try:
            p = PureWindowsPath(file_name)
        except:
            p = Path(file_name)
        s = str.lower(p.stem)
        return s

    def _save_to_excel(self, obj, file_name, sheet_name=None):
        """ Internal routine to save a dataframe to excel with sensible options"""
        stem_name = self._stem_name(file_name)

        if self.output_path[-1] == "/" or self.output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"

        full_file_name = self.output_path + separator + stem_name + ".xlsx"
        if not sheet_name:
            sheet_name = file_name
        sheet_name = sheet_name[:30]  # truncating to meet Excel max tab lenght
        try:
            obj.to_excel(
                full_file_name, sheet_name=sheet_name, index=False, freeze_panes=(1, 0)
            )

        except Exception:
            logger.exception("Failed to save to Excel file")
            return None

        return full_file_name

    def _save_to_csv(self, df, file_name):
        """ Internal routine to save a dataframe to a csv with sensible options"""
        stem_name = self._stem_name(file_name)

        if self.output_path[-1] == "/" or self.output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"
            logger.warning(
                "Output path does not end in backslash, add it in the config for stability"
            )

        full_file_name = self.temp_path + separator + stem_name + ".csv"
        try:
            df.to_csv(
                full_file_name, index=False, quotechar='"', quoting=csv.QUOTE_ALL,
            )
        except Exception:
            logger.exception("Failed to save to csv file")
            return None
        return full_file_name

    def _save_to_pickle(self, obj, file_name):
        """ Internal routine to save a dataframe to a pickle with sensible options"""
        stem_name = self._stem_name(file_name)

        if self.output_path[-1] == "/" or self.output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"

        full_file_name = self.temp_path + separator + stem_name + ".pickle"
        try:
            with open(full_file_name, "wb") as handle:
                pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print(
                    "Saved pickle to " + full_file_name,
                    round((handle.tell() / 1024) / 1024, 1),
                    " MB",
                )
        except Exception:
            logger.exception("Failed to save to a pickle file")
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
        """Load a xlsx, csv or pickle file into a DataFrame with extra features and sensible parameters
        Assumes it is perfectly tabular and fields are in row one, assumes spreadsheets has one sheet.
        This is meant to be used for highly standard files, typically intermediate files we control
        Args:
            file_name (String): the core (stem) file name and externsion 
            source (str, optional): temp, input, output, auto, Defaults to "auto".
            Auto will look for the file in temp_path, then input_path, then output_path
        Returns:
            DataFrame with the file loaded
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
            elif os.path.isfile(self.input_path + file_name):
                full_name = self.input_path + file_name
            elif os.path.isfile(self.output_path + file_name):
                full_name = self.output_path + file_name
            else:
                logger.error("No file found in any of the possible sources")
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
                logger.debug("Object doesnt have len()")
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
        if filename is False:
            return

        flag = False
        flag_to_csv_instead = False
        filename = str.lower(str.strip(filename))
        start_time = datetime.now()
        stem_name = self._stem_name(filename)

        if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
            if ".xlsx" in filename:
                if obj.shape[0] < self._MAX_ROWS_TO_EXCEL:
                    logger.debug("Saving to an excel file")
                    output = self._save_to_excel(obj, stem_name)
                    if output:
                        logger.info("Saved to %s", output)
                        flag = True

                else:
                    flag_to_csv_instead = True
                    logger.warning("Too big for excel, saving to csv instead")
            if ".csv" in filename or flag_to_csv_instead:
                logger.debug("Saving to csv")
                output = self._save_to_csv(obj, stem_name)
                if output:
                    print("Saved to ", output)
                    flag = True
        if ".pickle" in filename or bool_also_pickle:
            logger.debug("Saving to pickle format")
            output = self._save_to_pickle(obj, stem_name)
            if output:
                logger.info("Saved to %s", output)
                flag = True
        if flag:
            try:
                # TODO #15 Look into pretty outputs for logging lists/tuples
                print("Shape :", obj.shape)
                print("Saved columns:", list(obj.columns))
            except Exception:
                pass  # should be when the object doesnt support shape or columns
            logger.info(
                "Finished in %s mins",
                str(round((datetime.now() - start_time).total_seconds() / 60.0, 2)),
            )
        else:
            logger.error("Errors found when saving")

        return flag

    def profile_dataframe(self, df):
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
                metrics["max"] = max(df[col])
                metrics["min"] = min(df[col])
                metrics["sum"] = sum(df[col])
                metrics["sum_abs"] = sum(abs(df[col]))
                metrics["std"] = df[col].std()
                # TODO: possibly add hist/sparkline data to further add to the profiling
            elif "int" in str(typ):
                metrics["max"] = max(df[col])
                metrics["min"] = min(df[col])
                metrics["sum"] = sum(df[col])
                metrics["sum_abs"] = sum(abs(df[col]))
                metrics["std"] = df[col].std()
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

    def check_blanks(
        self,
        df_in,
        columns=None,
        zeroes=True,
        null_strings_and_spaces=True,
        output_file=None,
        totals_only=False,
    ):
        """ Reports on blanks in the Dataframe and optionally saves to an excel file  """

        if not isinstance(df_in, pd.DataFrame):
            logging.error(
                "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
            )
            return
        df = df_in.copy()
        if columns and isinstance(columns, list):
            cols = columns
        elif not columns:
            cols = df.columns
        else:
            logging.error("Expecting a list, even a list of one element")
            return

        fields = ",".join(cols)
        logging.info("Checking for blanks in %s", fields)
        total_results = []
        for c in cols:
            if is_numeric_dtype(df[c]) and zeroes:
                df[c + "_blanks"] = (pd.isna(df[c])) | (df[c] == 0)
            elif is_string_dtype(df[c]) and null_strings_and_spaces:
                logging.debug("Checking for spaces and nullstring too in %s", c)
                df[c + "_blanks"] = (pd.isna(df[c])) | (df[c].str.strip() == "")
            else:
                logging.debug("Checking just for NaN or NaT in %s", c)
                df[c + "_blanks"] = pd.isna(df[c])
            total_results.append(df[c + "_blanks"].sum())
        new_cols = [c + "_blanks" for c in cols]
        df["has_blanks"] = np.any(df[new_cols])

        print("Total blanks found in each columns:", total_results)
        if output_file:
            self.save(df, output_file)
        if totals_only:
            return total_results

        return df

    def check_duplicates(
        self, df, columns=None, keep="first", ascending=None, output_file=None
    ):
        """
        Bundles duplicate analysis, common steps like checking duplicates
        showing the total numbers, showing the actual duplicates, exporting
        to excel the offending duplicates
        Args:
            df (DataFrame): pandas dataframe
            columns (str, list or int, optional): column(s) to check, if multiple columns provided 
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
            logging.error(
                "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
            )
            # TODO: #17 Add support for Series in the duplicate check
            return
        if not isinstance(columns, list):
            logging.error("Expecting a list, even a list of one element")
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

        if output_file:
            self._save_to_excel(df_ret, output_file)

        return df_ret

    def check_sequence(self, obj_in, col=""):
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
                            len(diff),
                            " missing in sequence, fist 10:",
                            list(diff)[0:10],
                        )
                        return list(diff)
                    else:
                        print("Full sequence")
                        return []
                else:
                    print("No sequence to check")
                    return None
        return

    def clean_cols(self, in_df, date_fillna="latest"):
        """Cleanup the actual values of the dataframe with sensible
        nulls handling.

        Args:
            in_df ([type]): Input DataFrame
            date_fillna ('latest','first' or datetime, optional):
            What to put in NaT values, takes the first, last or a specified
            date to fill the gaps.
            Defaults to "latest".

        Returns:
            DataFrame: Returns copy of the original dataframe with modifications
            Beware if the dataframe is large you may have memory issues.
        """

        df = in_df.copy()
        dtypes = df.dtypes.to_dict()
        for col, typ in dtypes.items():
            if ("int" in str(typ)) or ("float" in str(typ)):
                df[col].fillna(0, inplace=True)
            elif is_datetime(df[col]):
                if date_fillna == "latest":
                    val = max(df[col])
                elif date_fillna == "first":
                    val = min(df[col])
                elif isinstance(date_fillna, datetime):
                    val = date_fillna
                df[col].fillna(val, inplace=True)
            elif typ == "object":
                df[col].fillna("", inplace=True)
        return df


def main():
    """ main routine"""


if __name__ == "__main__":
    main()

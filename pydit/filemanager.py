""" class for dealing with opening and saving files within the project
"""

import logging
from datetime import datetime
import pickle
import os
from pathlib import Path, PureWindowsPath
import csv
import pandas as pd

logger = logging.getLogger(__name__)


class FileManager:
    """Singleton class to provie file management features across the library"""

    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if FileManager.__instance is None:
            FileManager()
        return FileManager.__instance

    def __init__(self,):
        """ Virtually private constructor. """
        if FileManager.__instance is not None:
            return None
            # TODO: #21 Research whether returning None in singleton __init__ is the right approach, got some errors in ipython
            # when rerruning the initialisation somehow gets called again. now seems to be working
            # raise Exception("You cannot initialise the Configuration class again")
        else:
            FileManager.__instance = self
            self._temp_path = "./"
            self._output_path = "./"
            self._input_path = "./"
            self._max_rows_to_excel = 200000

    def _fix_path(self, path=None):
        if not path:
            res = "./"
        else:
            if not (path[-1] == "/" or path[-1] == "\\"):
                logging.debug("Adding a trailing / to path")
                res = path + "/"
            else:
                res = path
                logging.debug("Setting path to %s", path)
        if Path(res).is_dir() is False:
            logger.warning(
                "Could not find the folder %s , ensure it does exist or gets created",
                res,
            )
        else:
            logger.debug("Folder %s found alright", res)

        return res

    @property
    def max_rows_to_excel(self):
        """Maximum number of rows to save to Excel, past that CSV or Pickle"""
        return self._max_rows_to_excel

    @max_rows_to_excel.setter
    def max_rows_to_excel(self, n):
        """ Setter for max_rows_to_excel"""
        if n > 999999 or n < 0:
            raise Exception("Rows number must be positive and less than 1,000,000")
        self._max_rows_to_excel = n

    @property
    def temp_path(self):
        """'Where do we save the temp files, typically for large files, local cache"""
        return self._temp_path

    @temp_path.setter
    def temp_path(self, path):
        """ Where we validate the temp_path property"""
        self._temp_path = self._fix_path(path)

    @property
    def input_path(self):
        """ input_path property"""
        return self._input_path

    @input_path.setter
    def input_path(self, path):
        """ Where we validate the input_path property"""
        self._input_path = self._fix_path(path)

    @property
    def output_path(self):
        """ Output path property"""
        return self._output_path

    @output_path.setter
    def output_path(self, path):
        """ where we validate the output_path property"""
        self._output_path = self._fix_path(path)

    def _stem_name(self, file_name):
        """ find the core name of a provided string with a filename and lowers case"""
        try:
            p = PureWindowsPath(file_name)
        except Exception:
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
            logger.debug(
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
            logger.debug(
                "Output path does not end in backslash, add it in the config for stability"
            )

        full_file_name = self.temp_path + separator + stem_name + ".pickle"
        try:
            with open(full_file_name, "wb") as handle:
                pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
                logger.info(
                    "Saved pickle to "
                    + full_file_name
                    + " "
                    + str(round((handle.tell() / 1024) / 1024, 1))
                    + " MB",
                )
        except Exception:
            logger.exception("Failed to save to a pickle file")
            return None
        return full_file_name

    def load(self, file_name, source="auto"):
        """Load a xlsx, csv or pickle file into a DataFrame with extra features
        and sensible parameters. Assumes it is perfectly tabular and fields are
        in row one, assumes spreadsheets has one sheet. This is meant to be used
        for highly standard files, typically intermediate files we control
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
                    logger.info(
                        "Loaded pickle from: "
                        + full_name
                        + "\nSize:"
                        + str(round((handle.tell() / 1024) / 1024, 1))
                        + " MB",
                    )
            except Exception as e:
                print(e)
        if ".xlsx" in full_name:
            try:
                obj = pd.read_excel(full_name)
                logger.info("Loading from: " + full_name)
            except Exception as e:
                logger.error(e)
        if ".csv" in full_name:
            try:
                obj = pd.read_csv(full_name)
                logger.info("Loading from: " + full_name)
            except Exception as e:
                logger.error(e)
        if isinstance(obj, pd.DataFrame):
            logger.info(
                "Loading into a dataframe with rows/cols: %s",
                "/".join(map(str, obj.shape)),
            )
            logger.info("Columns: ['%s']", "','".join(map(str, obj.columns)))
        else:
            try:
                logger.info("Length: %s", len(obj))
            except Exception:
                logger.debug("Object doesnt have len()")
        return obj

    def save(self, obj, filename, bool_also_pickle=False):
        """Save the dataframe in excel, pickle or csv with some extra audit trails
        as well as choosing the destination based on size

        Args:
            obj ([type]): [description]
            filename ([type]): [description]
            bool_also_pickle (bool, optional): [description]. Defaults to False.
        """
        if not filename:
            logger.warning("No filename provided")
            return False

        try:
            if len(obj) == 0:
                logger.warning("Nothing to save to %s, length zero object", filename)
                return False
            else:
                if obj.empty:
                    logger.warning("Nothing to save to %s, empty object", filename)
                    return False
                else:
                    # object not empty, we continue
                    # logger.debug("Non empty object, will proceed")
                    pass

        except Exception:
            # we failed somehow to check the len(), probably None object
            logger.warning("Nothing to save to %s, empty object", filename)
            return False

        flag = False
        flag_to_csv_instead = False
        filename = str.lower(str.strip(filename))
        start_time = datetime.now()
        stem_name = self._stem_name(filename)

        if ".pickle" in filename or bool_also_pickle:
            logger.debug("Saving to pickle format")
            output = self._save_to_pickle(obj, stem_name)
            if output:
                logger.info("Saved to %s", output)
                flag = True
        if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
            if ".xlsx" in filename:
                if obj.shape[0] < self._max_rows_to_excel:
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
                    logger.info("Saved to %s", output)
                    flag = True
        else:
            logger.info("Object is not a DataFrame or Series, can't save to Excel")

        if flag:
            try:
                logger.info("Shape: %s", " ".join(map(str, obj.shape)))
                logger.info("Columns: ['%s']", "','".join(map(str, obj.columns)))
            except Exception as e:
                pass  # should be when the object doesnt support shape or columns
            logger.info(
                "Finished in %s mins",
                str(round((datetime.now() - start_time).total_seconds() / 60.0, 2)),
            )
        else:
            logger.error("Nothing saved")
        return flag

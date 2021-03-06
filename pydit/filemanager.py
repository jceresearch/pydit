"""Class for dealing with opening and saving files within the project
"""

import logging
from datetime import datetime
import pickle
import os
from pathlib import Path, PureWindowsPath
import csv
import pandas as pd

# pylint: disable=logging-fstring-interpolation
# pylint: disable=logging-not-lazy


logger = logging.getLogger(__name__)


class FileManager:
    """Singleton class to provide file management features across the library"""

    __instance = None

    @staticmethod
    def getInstance():
        """Static access method."""
        if FileManager.__instance is None:
            FileManager()
        return FileManager.__instance

    def __init__(
        self,
    ):
        """Virtually private constructor."""
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
        """Setter for max_rows_to_excel"""
        if n > 999999 or n < 0:
            raise ValueError("Rows number must be positive and less than 1,000,000")
        self._max_rows_to_excel = n

    @property
    def temp_path(self):
        """'Where do we save the temp files, typically for large files, local cache"""
        return self._temp_path

    @temp_path.setter
    def temp_path(self, path):
        """Where we validate the temp_path property"""
        self._temp_path = self._fix_path(path)

    @property
    def input_path(self):
        """input_path property"""
        return self._input_path

    @input_path.setter
    def input_path(self, path):
        """Where we validate the input_path property"""
        self._input_path = self._fix_path(path)

    @property
    def output_path(self):
        """Output path property"""
        return self._output_path

    @output_path.setter
    def output_path(self, path):
        """where we validate the output_path property"""
        self._output_path = self._fix_path(path)

    def _stem_name(self, file_name):
        """find the core name of a provided string with a filename and lowers case"""
        try:
            p = PureWindowsPath(file_name)
        except Exception:
            p = Path(file_name)
        s = str.lower(p.stem)
        return s

    def _save_to_excel(self, obj, file_name, sheet_name=None, dest="auto"):
        """Internal routine to save a dataframe to excel with sensible options"""
        stem_name = self._stem_name(file_name)
        if dest == "auto":
            output_path = self.output_path
        elif dest == "temp":
            output_path = self.temp_path
        elif dest == "output":
            output_path = self.output_path
        elif dest == "input":
            output_path = self.input_path
        else:
            raise ValueError("dest must be auto, output, temp or input")

        if output_path[-1] == "/" or output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"

        full_file_name = output_path + separator + stem_name + ".xlsx"
        if not sheet_name:
            sheet_name = file_name
        sheet_name = sheet_name[:30]  # truncating to meet Excel max tab lenght
        try:
            obj.to_excel(
                full_file_name, sheet_name=sheet_name, index=False, freeze_panes=(1, 0)
            )

        except Exception as e:
            raise RuntimeError(
                "Failed to save to Excel file to  %s" % full_file_name
            ) from e

        return full_file_name

    def _save_to_csv(self, df, file_name, dest="auto"):
        """Internal routine to save a dataframe to a csv with sensible options"""
        stem_name = self._stem_name(file_name)

        if dest == "auto":
            output_path = self.temp_path
        elif dest == "temp":
            output_path = self.temp_path
        elif dest == "output":
            output_path = self.output_path
        elif dest == "input":
            output_path = self.input_path
        else:
            raise ValueError("dest must be auto, output, temp or input")

        if output_path[-1] == "/" or output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"

        full_file_name = output_path + separator + stem_name + ".csv"
        try:
            df.to_csv(
                full_file_name,
                index=False,
                quotechar='"',
                quoting=csv.QUOTE_ALL,
            )
        except Exception as e:
            raise RuntimeError(
                "Failed to save to CSV file to  %s" % full_file_name
            ) from e

        return full_file_name

    def _save_to_pickle(self, obj, file_name, dest="auto"):
        """Internal routine to save a dataframe to a pickle with sensible options"""
        stem_name = self._stem_name(file_name)

        if dest == "auto":
            output_path = self.temp_path
        elif dest == "temp":
            output_path = self.temp_path
        elif dest == "output":
            output_path = self.output_path
        elif dest == "input":
            output_path = self.input_path
        else:
            raise ValueError("dest must be auto, output, temp or input")

        if output_path[-1] == "/" or output_path[-1] == "\\":
            separator = ""
        else:
            separator = "\\"

        full_file_name = output_path + separator + stem_name + ".pickle"
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
        except Exception as e:
            raise RuntimeError(
                "Failed to save to pickle file to %s" % full_file_name
            ) from e
        return full_file_name

    def load(self, file_name, source="auto"):
        """Load a xlsx, csv or pickle file into a DataFrame with extra features and sensible parameters.

        Assumes it is perfectly tabular, first row has headers and loads the first sheet
        This function is meant to be used with files generated by pydit or very
        simple/standard files. For anything more complicated you should use pandas direclty.


        Parameters
        ----------
        file_name : str
            The core (stem) file name and externsion
        source : str, optional, default "auto"
            temp, input, output: as per the paths set in the config
            Auto will look for the file in temp_path, then input_path, then output_path

        Returns
        -------
        DataFrame
            If the file is not found, returns None


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
                        "Loaded pickle: "
                        + file_name
                        + "\nFull path: "
                        + full_name
                        + "\nFile Size:"
                        + str(round((handle.tell() / 1024) / 1024, 1))
                        + " MB",
                    )
            except Exception as e:
                print(e)
        if ".xlsx" in full_name:
            try:
                obj = pd.read_excel(full_name)
                logger.info("Loading excel from: " + full_name)
            except Exception as e:
                logger.error(e)
        if ".csv" in full_name:
            try:
                obj = pd.read_csv(full_name)
                logger.info("Loading csv from: " + full_name)
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

    def save(self, obj, filename, also_pickle=False, dest="auto"):
        """Save the dataframe in excel, pickle or csv with some extra audit trails
        as well as choosing the destination based on size

        Parameters
        ----------
        obj : DataFrame
            The dataframe to save
        filename : str
            The file name with extension, no path
        also_pickle : bool, optional, default False
            If true, will save the object to a pickle file too, to the temp folder
        dest : str, optional, default "auto"
            auto, temp, input, output: as per the paths set in the config
        Returns
        -------
            Path of the file saved if successfull
            None if unsuccessful or Empty data

        """

        try:
            if len(obj) == 0:
                logger.warning("Nothing to save to %s, length zero object", filename)
                return None
            else:
                if obj.empty:
                    logger.warning("Nothing to save to %s, empty object", filename)
                    return None
                else:
                    # object not empty, we continue
                    # logger.debug("Non empty object, will proceed")
                    pass

        except Exception:
            # we failed somehow to check the len(), probably None object
            logger.warning("Nothing to save to %s, empty object", filename)
            return None

        flag_to_csv_instead = False
        filename = str.lower(str.strip(filename))
        start_time = datetime.now()
        stem_name = self._stem_name(filename)
        flag_other_type = False

        if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
            if ".xlsx" in filename:
                if obj.shape[0] < self._max_rows_to_excel:
                    logger.info("Saving to excel format")
                    output = self._save_to_excel(obj, stem_name, dest=dest)
                    if output:
                        logger.info("Saved to %s", output)
                else:
                    flag_to_csv_instead = True
                    logger.warning("Too big for excel, saving to csv instead")
            if ".csv" in filename or flag_to_csv_instead:
                logger.debug("Saving to csv")
                output = self._save_to_csv(obj, stem_name, dest=dest)
                if output:
                    logger.info("Saved to %s", output)
        else:
            flag_other_type = True  # so we save as pickle

        if ".pickle" in filename or also_pickle or flag_other_type:
            logger.info("Saving to pickle format")
            output = self._save_to_pickle(obj, stem_name, dest=dest)
            if output:
                logger.info("Saved to %s", output)

        try:
            logger.info("Rows/Columns: %s", " ".join(map(str, obj.shape)))
            logger.info("Columns: ['%s']", "','".join(map(str, obj.columns)))
        except Exception:
            logger.info("Object of type: %s ", type(obj))
            try:
                logger.info("Object of len: %s ", len(obj))
            except Exception:
                logger.info("Object has no len()")

            # should happen when the object doesnt support shape or columns
            # so we show the object type so user can check if that is expected
        logger.info(
            "Finished in %s mins",
            str(round((datetime.now() - start_time).total_seconds() / 60.0, 2)),
        )

        return output

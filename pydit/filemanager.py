"""Module for dealing with opening and saving files within the project

This module is still highly experimental and unstable


Usage:


"""

import logging
from datetime import datetime
import pickle
import os
import pathlib
from pathlib import Path, PureWindowsPath
import csv
import pandas as pd
import yaml

# pylint: disable=logging-fstring-interpolation
# pylint: disable=logging-not-lazy


logger = logging.getLogger(__name__)


def _save_yaml(data, file_name):
    """Save the data to a yaml file"""
    with open(file_name, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f)


def _fix_path_name(path=None):
    """Internal routine to fix the path to a file"""
    if not path:
        res = "./"
    else:
        if not (path[-1] == "/" or path[-1] == "\\"):
            logging.debug("Adding a trailing / to path")
            res = path + "/"
        else:
            res = path
    return res


def _stem_name(file_name):
    """find the core name of a provided string with a filename and lowers case"""
    try:
        p = PureWindowsPath(file_name)
    except Exception:
        p = Path(file_name)
    s = str.lower(p.stem)
    return s


def setup_project(project_name="my_project", project_path="."):
    """Setup the project directory and log file"""
    logger.info(f"Setting up project {project_name}")
    if project_path == ".":
        _project_path = Path(os.getcwd())
    else:
        _project_path = Path(project_path)
    if not _project_path.exists():
        _project_path.mkdir()

    config = {}
    config["project_name"] = project_name
    config["project_path"] = str(_project_path)
    config["temp_path"] = config["project_path"] + "/temp"
    config["output_path"] = config["project_path"] + "/output"
    config["input_path"] = config["project_path"] + "/input"
    config["max_rows_to_excel"] = 200000
    pathlib.Path(config["temp_path"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(config["output_path"]).mkdir(parents=True, exist_ok=True)
    pathlib.Path(config["input_path"]).mkdir(parents=True, exist_ok=True)
    _save_yaml(config, config["project_path"] + "/conf.yaml")
    return config


def set_config(key, value, config=None):
    """Set a configuration value"""
    if not config:
        config = load_config()
    if isinstance(config, str):
        config = load_config(config)
        if not config:
            raise ValueError("Error loading configuration file")
    if isinstance(config, dict):
        if check_config(config):
            config[key] = value
            if check_config(config, fix=True):
                return True
            else:
                raise ValueError("Error saving back the config with key/value provided")
        else:
            raise ValueError("Error validating the configuration file")
    return False


def check_config(config, fix=False):
    """Check the configuration file is valid"""
    if not config:
        config = load_config()
        if not config:
            raise ValueError("Could not load config")
    if not config["project_name"]:
        return False
    if fix:
        config["project_path"] = _fix_path_name(config["project_path"])
        config["temp_path"] = _fix_path_name(config["temp_path"])
        config["output_path"] = _fix_path_name(config["output_path"])
        config["input_path"] = _fix_path_name(config["input_path"])
    if not config["project_path"]:
        return False
    if not config["temp_path"]:
        return False
    if not config["output_path"]:
        return False
    if not config["input_path"]:
        return False
    if not config["max_rows_to_excel"]:
        return False
    if not Path(config["input_path"]).exists():
        if fix:
            Path(config["input_path"]).mkdir()
        else:
            return False
    if not Path(config["output_path"]).exists():
        if fix:
            Path(config["output_path"]).mkdir()
        else:
            return False
    if not Path(config["temp_path"]).exists():
        if fix:
            Path(config["temp_path"]).mkdir()
        else:
            return False
    if fix:
        _save_yaml(config, config["project_path"] + "/conf.yaml")

    return True


def load_config(project_path="."):
    """Load the configuration file for the project"""
    conf_file = Path(project_path + "/conf.yaml")
    if not conf_file.exists():
        setup_project("untitled")
    config = yaml.safe_load(open(conf_file, "r", encoding="utf-8"))
    if not config:
        raise ValueError("Could not load the conf file")
    if not check_config(config, fix=True):
        raise ValueError("Config file is not valid")

    return config


def _save_to_excel(obj, file_name, sheet_name=None, dest="auto", config=None):
    """Internal routine to save a dataframe to excel with sensible options"""
    stem_name = _stem_name(file_name)
    if dest == "auto":
        output_path = config["output_path"]
    elif dest == "temp":
        output_path = config["temp_path"]
    elif dest == "output":
        output_path = config["output_path"]
    elif dest == "input":
        output_path = config["input_path"]
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


def _save_to_csv(df, file_name, dest="auto", config=None):
    """Internal routine to save a dataframe to a csv with sensible options"""
    stem_name = _stem_name(file_name)
    if dest == "auto":
        output_path = config["temp_path"]
    elif dest == "temp":
        output_path = config["temp_path"]
    elif dest == "output":
        output_path = config["output_path"]
    elif dest == "input":
        output_path = config["input_path"]
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
        raise RuntimeError("Failed to save to CSV file to  %s" % full_file_name) from e

    return full_file_name


def _save_to_pickle(obj, file_name, dest="auto", config=None):
    """Internal routine to save a dataframe to a pickle with sensible options"""
    stem_name = _stem_name(file_name)

    if dest == "auto":
        output_path = config["temp_path"]
    elif dest == "temp":
        output_path = config["temp_path"]
    elif dest == "output":
        output_path = config["output_path"]
    elif dest == "input":
        output_path = config["input_path"]
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


def load(file_name, source="auto", config=None):
    """Load a xlsx, csv or pickle file into a DataFrame with extra features and sensible parameters.

    Assumes it is perfectly tabular, first row has headers and loads the first sheet
    This function is meant to be used with very simple/standardised files.
    For anything more complicated you should use pandas direclty.


    Parameters
    ----------
    file_name : str
        The core (stem) file name and externsion
    source : str, optional, default "auto"
        temp, input, output: as per the paths set in the config
        Auto will look for the file in temp_path, then input_path, then output_path
    config : dict or path to yaml file, optional, default None (attempts to load from conf.yaml)
    Returns
    -------
    DataFrame
        If the file is not found, returns None


    """
    if not config:
        config = load_config()
        if not config:
            raise ValueError("Could not load config")
    else:
        if isinstance(config, str):
            config = load_config(config)
            if not config:
                raise ValueError("Could not load config")
        elif isinstance(config, dict):
            if not check_config(config):
                raise ValueError("Config file is not valid")
        else:
            raise ValueError("config must be a path to a yaml file or a dict")
    obj = None
    if source == "input":
        if os.path.isfile(config["input_path"] + file_name):
            full_name = config["input_path"] + file_name
    if source == "output":
        if os.path.isfile(config["output_path"] + file_name):
            full_name = config["output_path"] + file_name
    if source == "temp":
        if os.path.isfile(config["temp_path"] + file_name):
            full_name = config["temp_path"] + file_name
    if source == "auto":
        if os.path.isfile(config["temp_path"] + file_name):
            full_name = config["temp_path"] + file_name
        elif os.path.isfile(config["input_path"] + file_name):
            full_name = config["input_path"] + file_name
        elif os.path.isfile(config["output_path"] + file_name):
            full_name = config["output_path"] + file_name
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


def save(obj, filename, also_pickle=False, dest="auto", config=None):
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
    config : dict or path to yaml file, optional, default None (attempts to load from conf.yaml)

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

    if not config:
        config = load_config()
        if not config:
            raise ValueError("Could not load config")

    flag_to_csv_instead = False
    filename = str.lower(str.strip(filename))
    start_time = datetime.now()
    stem_name = _stem_name(filename)
    flag_other_type = False

    if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
        if ".xlsx" in filename:
            if obj.shape[0] < config["max_rows_to_excel"]:
                logger.info("Saving to excel format")
                output = _save_to_excel(obj, stem_name, dest=dest, config=config)
                if output:
                    logger.info("Saved to %s", output)
            else:
                flag_to_csv_instead = True
                logger.warning("Too big for excel, saving to csv instead")
        if ".csv" in filename or flag_to_csv_instead:
            logger.debug("Saving to csv")
            output = _save_to_csv(obj, stem_name, dest=dest, config=config)
            if output:
                logger.info("Saved to %s", output)
    else:
        flag_other_type = True  # so we save as pickle

    if ".pickle" in filename or also_pickle or flag_other_type:
        logger.info("Saving to pickle format")
        output = _save_to_pickle(obj, stem_name, dest=dest, config=config)
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

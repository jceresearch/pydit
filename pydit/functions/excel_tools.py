"""


"""
import openpyxl
import logging

import pandas as pd

logger = logging.getLogger(__name__)


def read_excel(
    file_name,
    sheet_name=None,
):
    """Reads an Excel file and returns a dataframe."""
    logger.info("Reading Excel file")
    df = pd.read_excel(file_name, sheet_name=sheet_name, engine="openpyxl")
    df = df.dropna(how="all")

    return df

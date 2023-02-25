""" Module with utility functions for fuzzy matching"""

import string
import pandas as pd
import numpy as np
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)


@lru_cache(
    maxsize=None
)  # we enable the caching in this small piece, maxsize is set to unlimited, but we could add a limit , apparently having an actual limit makes it marginally faster in some conditions.
def token_set_sort(s):
    s = str(s)
    s = s.translate(str.maketrans("", "", string.punctuation))
    sl = list(set(str.split(s)))
    sl.sort()
    s = "".join(sl)
    return s


def create_fuzzy_key(df, input_col, output_col="fuzzy_key"):
    """Create a fuzzy key for a dataframe
    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to create the fuzzy key for
    input_col : str
        The column to create the fuzzy key from
    output_col : str, optional
        The column to create the fuzzy key to, by default "fuzzy_key"
    Returns
    -------
        pandas.Series
            The fuzzy key

    """
    df[output_col] = (
        df[input_col]
        .str.lower()
        .replace("'", "", regex=True)
        .replace(r"\s", " ", regex=True)
        .replace("", np.nan, regex=True)
    )
    # Now we are going to deal with non standar chars
    #
    # This version directly removes accented chars and spanish enie
    # df['fuzzy'] = df['fuzzy'].str.encode('ascii', 'ignore').str.decode('ascii')

    # This will also remove accented chars
    # from string import printable
    # st = set(printable)
    # df["fuzzy"] = df["fuzzy"].apply(lambda x: ''.join([" " if  i not in  st else i for i in x]))

    # This will retain the characters but standardise for compatibility, there are various
    # libraries that do that too. I would use other versions if performance is a concern
    df["fuzzy"] = (
        df["fuzzy"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df["fuzzy"].replace("[^a-z1-9 ]", " ", regex=True, inplace=True)
    df["fuzzy"].replace(" (ltd|plc|inc|llp|limited)", " ", regex=True, inplace=True)
    df["fuzzy"].replace("(mr|mrs|miss) ", " ", regex=True, inplace=True)
    df["fuzzy"].replace(" +", " ", regex=True, inplace=True)
    df["fuzzy"] = df["fuzzy"].str.strip()
    list_token_sort = [token_sort(s) for s in df["fuzzy"]]
    s = pd.Series(list_token_sort)
    df["fuzzy"] = s.values
    df.set_index("fuzzy")
    return list(df["fuzzy"][~pd.isnull(df.fuzzy)])


print("Test of the cleaning routine, examine it to check that it does what you need")
test_data = [
    ["  New\rLine", "linenew"],
    ["Iñaqui  ", "inaqui"],
    ["Tab\tEntry", "entrytab"],
    ["Lucía", "lucia"],
    ["", "nan"],
    ["Mr. Ryan     O'Neill", "oneillryan"],
    ["Miss Ana-María", "anamaria"],
    ["John Smith 2nd", "2ndjohnsmith"],
    ["Peter\uFF3FDrücker", "druckerpeter"],
    ["Emma\u005FWatson", "emmawatson"],
    ["Jeff Bezos", "bezosjeff"],
    ["  jeff   . Bezos  ", "bezosjeff"],
    ["Amazon Ltd.", "amazon"],
    ["Bezos, Jeff", "bezosjeff"],
    ["Charlie, 2 Delta, 1 Alpha, ", "12alphacharliedelta"],
    ["Emma Emma Hermione", "emmahermione"],
]

test_df = pd.DataFrame(test_data, columns=["input", "expected"])
test_list = create_fuzzy_column(test_df, "input")
test_df["test_check"] = test_df["expected"] == test_df["fuzzy"]
test_df

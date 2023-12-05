""" Module with utility functions for fuzzy matching"""
import unicodedata
import re
import string
import logging

# pylint disable=unused-variable

logger = logging.getLogger(__name__)


def clean_string(
    t=None,
    keep_dot=False,
    keep_dash=False,
    keep_apostrophe=False,
    keep_ampersand=False,
    keep_spaces=True,
    space_to_underscore=True,
    to_case="lower",
):
    """Sanitising a string

    Cleans the strings applying the following transformations:
    - Normalises unicode to remove accents and other symbols
    - Keeps only [a-zA-Z0-9]
    - Optional to retain dot
    - Spaces to underscore
    - Removes multiple spaces, strips
    - Optional to lowercase

    This is a naive/slow implementation, useful for sanitising things like
    a filename or column headers or small datasets. If you need to cleanup
    large datasets, you need to look into pandas/numpy tools, and vectorised
    functions.


    Parameters
    ----------
    t : str
        String to clean
    keep_dot : bool, optional, default False
        Whether to keep the dot in the string
    keep_dash : bool, optional, default False
        Whether to keep the dash in the string (useful for names)
    keep_aphostrophe : bool, optional, default False
        Whether to keep the apostrophe in the string (useful for names)
    keep_ampersand : True, False, "expand", default False
        Whether to keep the & or not, or expand to "and"
    keep_spaces: bool, optional, default True
        Whether to keep the spaces in the string
        If true we still remove double spaces, and by default we replace
        spaces to underscores.
    space_to_underscore : bool, optional, default True
        Whether to replace spaces with underscores
    case : str, optional, default "lower", choices=["lower", "upper"]
        Whether to lowercase the string

    Returns
    -------
    str
        Cleaned string

    """
    if t != t or t is None:
        return ""

    try:
        t = str(t)
    except Exception:
        return ""

    # we are going to normalize using NFKD
    # this will convert characters to their closest ASCII equivalent
    # e.g. é will become e
    # https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string
    r = (
        unicodedata.normalize("NFKD", t)
        .encode("ascii", errors="ignore")
        .decode("utf-8")
    )
    if to_case == "lower":
        r = str.lower(r)
    elif to_case == "upper":
        r = str.upper(r)
    else:
        pass

    if not keep_dot:
        r = re.sub(r"[\.]", " ", r)
    if not keep_dash:
        r = re.sub(r"[-]", " ", r)
    if not keep_apostrophe:
        r = re.sub(r"[']", " ", r)
    if not keep_ampersand:
        r = re.sub(r"[&]", " ", r)
    elif keep_ampersand == "expand":
        r = re.sub(r"[&]", "and", r)
    r = re.sub(r"[^a-zA-Z0-9\.\-\&']", " ", r)
    r = r.strip()
    if keep_spaces:
        if space_to_underscore:
            r = re.sub(" +", "_", r)
        else:
            r = re.sub(" +", " ", r)
    else:
        r = re.sub(" +", "", r)
    return r


# we enable the caching in this small piece, maxsize can be set to None=unlimited,
# but we could add a limit , apparently having an actual limit makes it
# marginally faster in some conditions.


def create_fuzzy_key(
    df, input_col, output_col="fuzzy_key", inplace=False, token_sort=None
):
    """
    Create a fuzzy key for a dataframe, note that this key preserves the spaces
    after tokenisation, thing this may work better when computing the lev
    distance. If you want a more compact string you need to tweak the
    code to set the clean_string function to remove spaces.


    Parameters
    ----------
    df : pd.DataFrame
        The dataframe to create the fuzzy key for
    input_col : str
        The column to create the fuzzy key from
    output_col : str, optional
        The column to create the fuzzy key to, by default "fuzzy_key"
    token_sort : str, optional
        Whether to use a token sorting algorithm or not and rely on other libraries.
        Can be "token_set_sort", "token_sort" or None
    inplace : bool, optional
        Whether to create the fuzzy key inplace or not, by default False

    Returns
    -------
        pandas.Series
            The fuzzy key

    """
    if token_sort not in [None, "token_set_sort", "token_sort"]:
        raise ValueError(
            f"token_sort must be None, token_set_sort or token_sort, got {token_sort}"
        )

    def _token_set_sort(s):
        s = str(s)
        s = s.translate(str.maketrans("", "", string.punctuation))
        sl = list(set(str.split(s)))
        sl.sort()
        s = " ".join(sl)
        return s

    def _token_sort(s):
        s = str(s)
        s = s.translate(str.maketrans("", "", string.punctuation))
        sl = str.split(s)
        sl.sort()
        s = " ".join(sl)
        return s

    if not inplace:
        df = df.copy()

    # First we are going to deal with the new lines and tabs and empty strings
    df[output_col] = (
        df[input_col]
        .fillna("")
        .str.lower()
        .replace(" (ltd|plc|inc|llp|limited)", " ", regex=True)
        .replace(r"(mr\.?|mrs\.?|miss\.?) ", " ", regex=True)
        .replace("o'", "o", regex=True)
        .replace(" +", " ", regex=True)
        .str.strip()
        .apply(
            lambda v: clean_string(
                v, keep_spaces=True, space_to_underscore=False, keep_ampersand="expand"
            )
        )
    )

    if token_sort == "token_set_sort":
        df[output_col] = df[output_col].apply(_token_set_sort)

    if token_sort == "token_sort":
        df[output_col] = df[output_col].apply(_token_sort)

    if not inplace:
        return df
    return None

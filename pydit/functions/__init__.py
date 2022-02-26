# General Functions
"""
pyjanitor's general-purpose data cleaning functions.

NOTE: Instructions for future contributors:

1. Place the source code of the functions in a file named after the function.
2. Place utility functions in the same file.
3. If you use a utility function from another source file,
please refactor it out to `janitor.functions.utils`.
4. Import the function into this file so that it shows up in the top-level API.
5. Sort the imports in alphabetical order.
6. Try to group related functions together (e.g. see `convert_date.py`)
7. Never import utils.
"""


from .create_calendar import create_calendar
from .add_percentile import add_percentile
from .profile_dataframe import profile_dataframe
from .check_duplicates import check_duplicates
from .check_sequence import check_sequence
from .add_counts import add_counts_between_related_df
from .check_referential_integrity import check_referential_integrity
from .fillna_smart import fillna_smart
from .check_blanks import check_blanks
from .coalesce_categories import coalesce_categories
from .cleanup_column_names import cleanup_column_names
from .anonymise import anonymise_key
from .count_cumulative_unique import count_cumulative_unique


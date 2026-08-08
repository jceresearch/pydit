"""
Sub-package (./wrangling) containing the core data wrangling functionality.

The modules are also self standing, you should be able to copy any .py file
and import it in your script to use it with no dependencies on other modules.

There may be some exceptions to this principle in the logging module, but
you should be able to create your own logger object and run with it.

"""

from ..logger import setup_logging, start_logging_debug, start_logging_info
from .anonymise import anonymise_key
from .blanks import check_blanks
from .calendar_table import create_calendar
from .cleanup_dataframe_columns_names import cleanup_column_names
from .coalesce_dataframe_columns import coalesce_columns
from .coalesce_dataframe_values import coalesce_values
from .collapse_dataframe_levels import collapse_levels
from .counts import (
    count_cumulative_unique,
    count_isna,
    count_notna,
    count_related_key,
    count_values_in_col,
    has_different_values,
)
from .date_time_calculations import (
    business_calendar,
    calculate_business_hours,
    calculate_business_hours_fast,
    date_relative_in_words,
    first_and_end_of_month,
)
from .duplicates import check_duplicates
from .file_utils import get_latest_modif_file_from_dir
from .fillna import fillna_smart
from .fuzzy_matching import clean_string, create_fuzzy_key
from .groupby_text_concatenate import groupby_text
from .keyword_search_batch import keyword_search
from .lookup_values import lookup_values
from .map_common_values import map_values
from .merge import merge_outer_and_split, merge_smart
from .referential_integrity_check import check_referential_integrity
from .sequence import check_sequence, group_gaps
from .split_transactions import check_for_split_transactions
from .truncate_datetime import truncate_datetime_dataframe
from .various import (
    create_test_dataframe,
    dataframe_to_code,
    deduplicate_list,
    print_green,
    print_red,
)

# Here we import each of the functions in the functions/ directory to have them
# available in the functions namespace.
# In turn functions gets imported with * at root

__all__ = [
    "anonymise_key",
    "business_calendar",
    "calculate_business_hours",
    "calculate_business_hours_fast",
    "check_blanks",
    "check_duplicates",
    "check_for_split_transactions",
    "check_referential_integrity",
    "check_sequence",
    "clean_string",
    "cleanup_column_names",
    "coalesce_columns",
    "coalesce_values",
    "collapse_levels",
    "count_cumulative_unique",
    "count_isna",
    "count_notna",
    "count_related_key",
    "count_values_in_col",
    "create_calendar",
    "create_fuzzy_key",
    "create_test_dataframe",
    "dataframe_to_code",
    "date_relative_in_words",
    "deduplicate_list",
    "fillna_smart",
    "first_and_end_of_month",
    "get_latest_modif_file_from_dir",
    "group_gaps",
    "groupby_text",
    "has_different_values",
    "keyword_search",
    "lookup_values",
    "map_values",
    "merge_outer_and_split",
    "merge_smart",
    "print_green",
    "print_red",
    "setup_logging",
    "start_logging_debug",
    "start_logging_info",
    "truncate_datetime_dataframe",
]

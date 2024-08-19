""" 
Sub-package (./functions) containing the core functionality.

The modules are also self standing, you should be able to copy any .py file
and import it in your script to use it with no dependencies on other modules.

There are currently no exceptions to this design principle.

"""

from .calendar_table import create_calendar, fom_eom
from .duplicates import check_duplicates
from .sequence import check_sequence
from .sequence import group_gaps
from .referential_integrity_check import check_referential_integrity
from .fillna import fillna_smart
from .blanks import check_blanks
from .coalesce_dataframe_values import coalesce_values
from .cleanup_dataframe_columns_names import cleanup_column_names
from .anonymise import anonymise_key
from .coalesce_dataframe_columns import coalesce_columns
from .collapse_dataframe_levels import collapse_levels
from .groupby_text_concatenate import groupby_text
from .keyword_search_batch import keyword_search
from .truncate_datetime import truncate_datetime_dataframe
from .counts import count_cumulative_unique
from .counts import count_related_key
from .counts import count_values_in_col
from .counts import count_isna
from .counts import count_notna
from .counts import has_different_values
from .date_time_calculations import business_calendar
from .date_time_calculations import calculate_business_hours_fast
from .date_time_calculations import calculate_business_hours
from .map_common_values import map_values
from .fuzzy_matching import create_fuzzy_key, clean_string
from .merge import merge_outer_and_split
from .merge import merge_smart
from .lookup_values import lookup_values
from .split_transactions import check_for_split_transactions
from .various import print_red
from .various import print_green
from .various import deduplicate_list
from .various import dataframe_to_code
from .various import create_test_dataframe
from ..logger import setup_logging, start_logging_debug, start_logging_info


# Here we import each of the functions in the functions/ directory to have them
# available in the functions namespace.
# In turn functions gets imported with * at root

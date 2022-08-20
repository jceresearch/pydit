""" 
Sub-package (./functions) containing the core functionality.

The modules are also self standing, you should be able to copy any .py file
and import it in your script to use it with no dependencies on other modules.

There are currently no exceptions to this design principle.

"""

from .calendar_table import create_calendar
from .percentile import add_percentile
from .profile_dataframe_statistics import profile_dataframe
from .duplicates import check_duplicates
from .sequence import check_sequence
from .referential_integrity_check import check_referential_integrity
from .fillna import fillna_smart
from .blanks import check_blanks
from .coalesce_dataframe_values import coalesce_values
from .cleanup_dataframe_columns_names import cleanup_column_names
from .anonymise import anonymise_key
from .counts import count_cumulative_unique
from .coalesce_dataframe_columns import coalesce_columns
from .benford import benford_to_dataframe
from .benford import benford_to_plot
from .benford import benford_list_anomalies
from .collapse_dataframe_levels import collapse_levels
from .groupby_text_concatenate import groupby_text
from .keyword_search_batch import keyword_search
from .truncate_datetime import truncate_datetime_dataframe
from .merge import merge_force_suffix
from .counts import count_related_key
from .counts import count_values_in_col
from .charts import chart_bar


# Here we import each of the functions in the functions/ directory to have them
# available in the functions namespace.
# In turn functions gets imported with * at root

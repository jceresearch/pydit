""" General Functions"""

from .create_calendar import create_calendar
from .add_percentile import add_percentile
from .profile_dataframe import profile_dataframe
from .check_duplicates import check_duplicates
from .check_sequence import check_sequence
from .add_counts import add_counts_between_related_df
from .check_referential_integrity import check_referential_integrity
from .fillna_smart import fillna_smart
from .check_blanks import check_blanks
from .coalesce_values import coalesce_values
from .cleanup_column_names import cleanup_column_names
from .anonymise import anonymise_key
from .count_cumulative_unique import count_cumulative_unique
from .coalesce_columns import coalesce_columns
from .check_benford import benford_to_dataframe
from .check_benford import benford_to_plot
from .check_benford import benford_list_anomalies
from .collapse_levels import collapse_levels
from .groupby_text import groupby_text

# Here we import each of the functions in the functions/ directory to have them
# available in the functions namespace.
# In turn functions gets imported with * at root

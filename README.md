# pydit
Library of useful data munging tools that a typical internal auditor may need to apply.  

(this library is for my own use, and it my first time creating a proper package, so if you wish to use/collaborate pls get in touch, or use at your own peril)  

It is inspired in Pyjanitor (awesome library!) but taking a different approach to cater for the IA use cases:
- dropping the method chaining
- making each function self standing, minimising imports. The auditor should be able to just pick a few of these modules and import them directly to assist in the test scripts without having the full blown functionality.
- adding significant amount of logging to explain what is going on under the hood
- aspirationally, lots of documentation, tests, and ease of interpretation/audit, and less focus on performance, typically audit tests dont have that many data, normally do not need to run "in production" or have to be operationalised.
It is more important to ensure accuracy and audit trails than raw performance/cleverness.


Quick start:
```
import pydit
logger = pydit.setup_logging()
logger.info("Started")
```


The logger feature is used extensively to create a human readable audit log to be included in workpapers.


The functions are typically used on a pandas DataFrame or Series object, 
returning a new object with the output of the processing. The default is 
not to mutate the calling object.



The list of functions available are:

create_calendar

add_percentile

profile_dataframe

check_duplicates

check_sequence

add_counts_between_related_df

check_referential_integrity

fillna_smart

check_blanks

coalesce_values()

cleanup_column_names()

anonymise_key()

count_cumulative_unique()

coalesce_columns()

benford_to_dataframe()

benford_to_plot()

benford_list_anomalies()

collapse_levels()

groupby_text()







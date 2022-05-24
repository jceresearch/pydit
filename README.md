# pydit
Library of useful data munging tools that a typical internal auditor may need to apply.  

(this library is for my own use, and it my first time creating a proper package, so if you wish to use/collaborate pls get in touch, or use at your own peril)  

It is inspired in Pyjanitor (awesome library!) but taking a different approach to cater for the IA use cases:
- dropping the method chaining approach from pyjanitor in interest of source code
readability. Pyjanitor is great and the chaining approach is super elegant. definitely a tool to have in the chest. However, to cater for auditors less skilled in python and to encourage simple and step by step documented code in the test and the simplest modular codebase in pydit itself, I made the hard choice of dropping the chaining.
- making each function self standing, minimising imports. The auditor should be able to cherry pick modules from pydit and import (or tweak) them directly to assist in the test scripts without having to understand or rely on the full blown functionality of pydit.
- adding significant amount of logging to explain what is going on under the hood
- aspirationally, lots of documentation, tests, and ease of interpretation/audit, and less focus on performance and more in accuracy/readability, typically audit tests dont have that many data, normally do not need to run "in production" or have to be operationalised. I will insist: in an audit use case it is more important to ensure accuracy and audit trails than raw performance/cleverness.


Quick start:
```
import pydit
logger = pydit.setup_logging()
logger.info("Started")
```

The logger feature is used extensively to create a human readable audit log to be included in workpapers.


<<<<<<< HEAD
The functions are typically used on a pandas DataFrame or Series object, 
returning a new object with the output of the processing. The default is 
not to mutate the calling object.



   pydit.benford_to_dataframe
   pydit.create_calendar
   pydit.add_percentile
   pydit.profile_dataframe
   pydit.check_duplicates
   pydit.check_sequence
   pydit.add_counts_between_related_df
   pydit.check_referential_integrity
   pydit.fillna_smart
   pydit.check_blanks
   pydit.coalesce_values
   pydit.cleanup_column_names
   pydit.anonymise_key
   pydit.count_cumulative_unique
   pydit.coalesce_columns
   pydit.benford_to_dataframe
   pydit.benford_to_plot
   pydit.benford_list_anomalies
   pydit.collapse_levels
   pydit.groupby_text

=======
The functions perform common transformations and checks on data -typically 
a pandas DataFrame or Series object- such as checking for blanks, or adding 
counters to check if two tables are plausibly in a 1:n or a n:n or a 1:1 
relationship. Typically these can be done with a short snippet of code in
pandas, but those can be fairly complex and obscure and you would also need to 
build some print() or logging feature to show the result and various exceptions
When stitching together many files, we often need to check for those many times
along the process. 
The default behaviour is to return a new or a transformed copy of the object and
not to mutate the input object(s). The "inplace-True" option may be available.
>>>>>>> 31401312537102e8b1f2f42a22c818443e167952





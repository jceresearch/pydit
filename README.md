
Pydit is a library of useful data munging tools that a typical internal auditor may need to apply.  

Note: this library is for my own use, and it my first time creating a proper package, so if you wish to use/collaborate pls get in touch, or use at your own peril

## Introduction 

Typically the features in pydit could be done with a short snippet of code using
pandas, numpy or standard python libraries. 
E.g. to cleanup data or to do some duplicates checks, Benford, etc.
But, those accumulate in the code. Either we need to put it in reusable functions or we start to
see them everywhere, possibly with slightly different code and bugs. 
Plus we need to keep evidence of the tests done and results, so we end up adding print() statements
everywhere, with intermediate .to_excel() exports.
All that gets messy. 

Pydit attempts to standardise several checks and cleanup routines with the specific
internal audit test use case in mind. 
Btw, Pydit takes a lot of inspiration (and code) from Pyjanitor, an awesome library!

These are the main design principles that differentiates pydit from other tools:
- dropping pyjanitor method chaining approach from pyjanitor in interest of source code
readability. Pyjanitor is great and its chaining approach is super elegant. Definitely one to have in the toolbox. However, auditors are typically less skilled in python than data scientists, work is tends to be one off and we have high turnover. To encourage simple and step by step documented code in the audit test and the simplest modular codebase in pydit itself, I made the hard choice of dropping the chaining.
-  functions are self standing, minimising imports/dependencies. The auditor should be able to import a individual modules from pydit to use that functionatliy directly in the audit test, making it easier to undertand it, document the test and peer review. 
- functions include verbose logging to explain what is going on under the hood.
- a focus on robust documentation, tests, and ease of read, and less on performance/smarts. 
Auditors most of the time work on relatively small datasets and we can afford some performance penalty if the code is trasparent and easy to follow. Most of the time we don't have a large teams or the time to develop extensive test suites on the audit tests themselves, so the code needs to be low complexity across the board and pydit needs to be almost as readable as snippets from stackoverflow.
- The default behaviour is to return a new or a transformed copy of the object and not to mutate the input object(s). The "inplace=True" option may be available.


## Quick start:
```
import pydit
logger = pydit.start_logging_info()
logger.info("Started")

```

The logger feature is used extensively by default, aiming to generate a human readable audit log to be included in workpapers that will satisfy QA. 


The functions perform common transformations and checks on data -typically 
a pandas DataFrame or Series object- such as checking for blanks, or adding 
counters to check if two tables are plausibly in a 1:n or a n:n or a 1:1 
relationship. 

```
import pandas as pd
df_profile=pydit.profile_dataframe(df) #will return a df with summary statistics
```


## Requires
- Python >= 3.8
- Pandas >= 1.2.1
- Numpy >= 1.21.1
- openpyxl
- Matplotlib (for the ocassional plot, e.g. Benford)


## Installation
```bash
pip install pydit
```
(not available in anaconda yet)

## Documentation
Documentation can be found [here](https://pydit.readthedocs.io/en/latest/index.html)

## Dev Install
```bash
git clone https://github.com/jceresearch/pydit.git
pip install -e .
```
This project uses:
- ```pylint```and  ```black``` for linting/style
- ```pytest``` for testing.
- ```sphinx``` and RTD for documentation 
- ```poetry``` for packaging.




Pydit is a library of useful data munging tools that a typical internal auditor may need to apply.  

Note: I am building this library as learning exercise on how to create a package, build documentation and tests and publish it, the code quality is low, marginally better than pasting from SO as I add tests and use it in real life ocassionally, but be warned that it has not been peer reviewed and I keep finding bugs :), use it at your own peril.

If you wish to contribute pls get in touch

## Introduction 

Pydit packages data cleansing and integrity checks tasks that typically could be done with a short snippet of code using pandas, numpy or standard python libraries.
E.g. to cleanup field names or to do some duplicates checks, Benford, etc.

These snippets tend to accumulate in the code making things difficutl to read and often may have some limitations/bugs that never get to retrofix.

On top, the scripts we run for audit tests need a lot of "audit trails" in line
to allow reviewers to follow the logic and actual execution outcomes, leading
to loads of print() everywhere.

All that gets messy. 

Pydit attempts to standardise several checks and cleanup routines with the specific internal audit test use case in mind. 
Btw, Pydit takes a lot of inspiration (and code) from Pyjanitor, an awesome library!

These are the main design principles:

- no method chaining, in interest of source code readability. 

Pyjanitor is great and its chaining approach is super elegant. Definitely one to have in the toolbox. However, auditors are typically less skilled in python than data scientists, and the code tends to be ad hoc/one of, with little time for deep review. Therefore, code readability is top priority. 
Method chaining does pack a lot but I find very simple step by step is easier
to peer review.

-  functions should be self standing, minimising imports/dependencies. 

The auditor should be able to import an individual module from pydit to use only that functionatliy directly in the audit test, making it easier to undertand it, document the test and peer review. 

- functions include verbose logging to explain what is going on under the hood.


- focus on documentation, tests, and simple code, less on performance

Auditors most of the time work on relatively small datasets (or one off runs)
and we can afford some performance penalty if the code is very easy to follow. Most of the time we don't have a large teams or the time to do extensive peer review or develop test suites on the audit tests themselves, so the code needs to be low complexity across the board.

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
- Numpy >= 1.22
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



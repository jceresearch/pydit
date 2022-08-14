
## Introduction to Pydit 

Pydit is a library of useful data munging tools that a typical internal auditor may need to apply.  

I am building this library as learning exercise on how to create a package, build documentation and tests and publish it, the code quality is still low, marginally better than pasting from SO.

Use it at your own peril.

If you wish to contribute pls get in touch.


Pydit is a collection of functions for data cleansing and integrity checks tasks.
Most can be done with a short snippet of code using pandas, numpy or standard python libraries, or using one of the many libraries out there.
E.g. cleanup field names or to do some duplicates checks, Benford, etc.
Btw, Pydit takes a lot of inspiration (and code) from Pyjanitor, an awesome library!


The problem I am tackling is:
- These snippets tend to accumulate in the code making it difficult to review 
and often may have some limitations/bugs that I never get to retrofix.
- While most implementations go for speed and elegance, in an Audit context the 
most important points are accuracy, legibility, reproducibility and generating lots of audit trails of what is going on.

These are the main design principles and highlights:

-  functions are self standing, minimising imports/dependencies. 

The auditor should be able to import an individual module from pydit to use only those functions directly in the audit test, making it easier to undertand it, document the test and peer review. No dependencies on future versions of the library breaking the code (which happens a lot)

- functions include verbose logging to explain what is going on.

Another feature specifically useful for Internal Audit, lots of logging entries.


- focus on documentation, tests, and simple code, less concern on performance

Auditors mostly work on relatively small datasets and/or one-off processing.
We can afford some performance penalty if the code is very easy to follow. Most of the time we don't have a large teams or the time to do extensive peer review or develop test suites for the audit tests themselves, so the code needs to be low complexity across the board.

- no method chaining, in interest of source code readability. 

Pyjanitor is great and its chaining approach is super elegant. Definitely one to have in the toolbox. However, auditors are typically less skilled in python than data scientists, and the code tends to be ad hoc/one-off, with little time for deep review. Therefore, code readability is top priority and I prefer more step by step 
approach to coding with no method chaining.

In any case the default behaviour is to return a new or a transformed copy of the object and not mutate the input object(s). The "inplace=True" option may be available.



## Quick start:
```
import pydit
logger = pydit.start_logging_info()
logger.info("Started")

```

The logger feature is used extensively by default, aiming to generate a human readable audit log to be included in workpapers.

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




## Introduction to Pydit 

Pydit is a library of common data munging tools that an internal auditor may need to apply. 

I am building this library as learning exercise on how to create a package, build documentation and tests and publish it, the code quality is still low, marginally better than pasting from SO.

Use it at your own peril :) . If you wish to contribute pls get in touch.



Most of these functions boil down to short(ish) snippet of code using some more or less obscure existing feature in pandas, numpy or standard python libraries). E.g. cleanup field names or to do some duplicates checks, Benford, etc.
Btw, Pydit takes a lot of inspiration (and code) from Pyjanitor, an awesome library!


The problem Pydit tries to solve is that all these cleanup and checks snippets start to crop up everywhere, pasted from recent ones (may or may not be buggy) with no great consistency, with the most laconic use of 
print() to explain what was going on. 
Libraries like pyjanitor do a great job but tend to be compact and non verbose, for audit tests we want super 
verbose and very easy to understand, code and read. 

So for pydit I follow the following principles:

1.  functions are self standing, minimising imports/dependencies. The auditor should be able to pluck and import an individual module from pydit to use only those functions directly in the audit test, making it easier to undertand it, document the test and peer review. Also, that means no dependencies on future versions of the library breaking the code (which happens a lot).

2. functions include verbose logging to explain what is going on. Another feature specifically useful for Internal Audit, lots of logging entries.

3. focus on documentation, tests, and simple code, less concern on performance

4. no method chaining, in interest of source code readability. Pyjanitor is great and its chaining approach is super elegant and compact. Definitely one to have in the toolbox. However, I have found I always need to split the steps to do/evidence data integrity checks on the intermediate results, and I find it easier to have it all step by step split, with comments, for easier peer review. In any case the default behaviour is to return a new or a transformed copy of the object and not mutate the input object(s). The "inplace=True" option may be available.



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
- Python >= 3.9
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
- ```sphinx``` for documentation in RTD
- ```myst_parser``` is a requirement for RTD too 
- ```poetry``` for packaging.




# Introduction to Pydit  

Pydit is a library of data wrangling tools aimed to internal auditors  
specifically for our use cases.

This library is also a learning exercise for me on how to create a package, build documentation & tests, and publish it.  
Code quality varies, and I don't commit to keep backward compatibility (see below how I use it) So, use it at your own peril!  
If, despite all that, you wish to contribute, feel free to get in touch.

Shout out: Pydit takes ideas (and some code) from Pyjanitor, an awesome library.  
Check it out!

## Why a dedicated library for auditors?

The problem Pydit solves is that a big part of our audit tests have to do with basic data quality checks (e.g. find duplicates or blanks) as they may flag potential fraud or systemic errors.

But to do those check I often end up pasting snippets from internet or reusing code from previous audits with no consistency or tests done.

Libraries like pyjanitor do a great job, however:  

  a) require installation that often is not allowed in your environment  

  b) tend to be very compact and non verbose (e.g. use method chaining), and 

  c) are difficult to review/verify.  


What I really need is:
  a) easy to review code, both code and execution (even for non-programmers)  

  b) portable, minimal dependencies, pure python, drop-in module ideally.  

  c) performance is ultimately secondary to readability and repeatability.  
  

Pydit follows these principles:

1. Functions should be self-standing with minimal imports/dependencies.  

The auditor should be able to import or copy paste only a specfic module into the project to perform a particular the audit test. That makes it easier to undertand, customise, review. Plus, it removes dependencies of future versions of pydit. Note that anyway, we need to file the actual code exactly as it was used during the audit.

2. Functions should include verbose logging, short of debug level.  

3. Focus on documentation, tests and simple code, less concerns on performance.

4. No method chaining, in interest of source code readability.

While Pyjanitor is great and its method chaining approach is elegant, I've found the good old "step by step" works better for documenting the test, and explaining to reviewers or newbies.  

5. Returns a new transformed copy of the object, code does not mutate the input object(s). Any previous inplace=True parameter is deprecated and I will remove in future versions.

## Quick start

```python
import pandas as pd
from pydit import start_logging_info # sets up nice logging params with rotation
from pydit import profile_dataframe  # runs a few descriptive analysis on a df
from pydit import cleanup_column_names # opinionated cleanup of column names


logger = start_logging_info()
logger.info("Started")

```

The logger feature is used extensively by default, aiming to generate a human readable audit log to be included in workpapers.

I recommend importing individual functions so you can copy them locally to your project folder and just change the import command to point to the local module, that way you freeze the version and reduce dependencies.

```python
df=pd.read_excel("mydata.xlsx")

df_profile= profile_dataframe(df) # will return a df with summary statistics

# you may realise the columns from excel are all over the place with cases and
# special chars

df_clean= cleanup_column_names(df) 

df_deduped=check_duplicates(df_clean, columns=["customer_id","last_update_date"],ascending=[True,False],keep="first",indicator=True, also_return_non_duplicates=True)

# you will get a nice output with the report on duplicates, retaining the last
# modification entry (via the pre-sort descending by date) and returning 
# the non-duplicates,  
# It also brings a boolean column flagging those that had a duplication removed.


```

## Requires

- python >=3.13 (Should work by and large in 3.10 onwards, but I test in 3.13)
- pandas
- numpy
- openpyxl
- matplotlib (for the ocassional plot, e.g. Benford)

## Installation

```bash
pip install pydit-jceresearch
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

- ```pylint``` for linting  
- ```black``` for style  
- ```pytest``` for testing  
- ```sphinx``` for documentation in RTD  
- ```myst_parser``` is a requirement for RTD too  
- ```poetry``` for packaging  

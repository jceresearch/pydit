
## Introduction to Pydit 

Pydit is a library of data wrangling tools for use by internal auditors 
specifically for our typical use cases, see below explanation.

This library is also a learning exercise for me on how to create a package, build documentation & tests, and publish it. 
Code quality varies, and due to its main use case I don't commit to keep backward 
compatibility (see below) So, use it at your own peril! 
If, despite all that, you wish to contribute, feel free to get in touch.

Shout out: Pydit takes ideas (and some code) from Pyjanitor, an awesome library.  
Check it out!

### Why a dedicated library for auditors?

The problem Pydit tries to solve is that all these cleanup and checks (e.g. extract 
duplicates) snippets are quite important for our work and start to crop up everywhere, 
often pasted from internet or from recent version used in another script with no 
consistency or tests.

On the other hand, libraries like pyjanitor do a great job but 
  a) require installation that often is not allowed in your environment 
  b) tend to be compact and non verbose (and use method chaining) and 
  c) are difficult to verify given the high complexity of the library overall. 

For internal audit tests, what we really need is very verbose and easy to 
understand code and outputs, so it is almost self explanatory and easy 
to review. 
Most of the time, performance is secondary. We just need it to run a 
few times for the duration of the audit.

This leads to Pydit following these principles:

1.  Functions should be self-standing with minimal imports/dependencies. 

The auditor should be able to import any individual module to use only those 
functions in the audit test. That makes it easier to undertand, document and 
peer-review. Also, it reduces dependencies of future versions of pydit. 
Typically, we need file the code used as it was ran during the audit.

2. Functions include verbose logging to explain what is going on. Another feature specifically useful for the Internal Audit use case.

3. Focus on documentation, tests, and simple code, less concern on performance.

4. No method chaining, in interest of source code readability. 

Pyjanitor is great and its chaining approach is elegant and compact. Definitely one to have in the toolbox. However, I have found it better for documenting the audit test, to check and show all the intermediate steps/results. 

5. The default behaviour is to return a new or a transformed copy of the object and not mutate the input object(s). The "inplace=True" option should be available if feasible.



## Quick start
```
import pandas as pd
from pydit import start_logging_info # sets up nice logging params with rotation
from pydit import profile_dataframe  # runs a few descriptive analysis on a df
from pydit import cleanup_column_names # opinionated cleanup of column names


logger = start_logging_info()
logger.info("Started")

```

The logger feature is used extensively by default, aiming to generate a human 
readable audit log to be included in workpapers.

I recommend importing individual functions so you can copy them locally to your
project folder and just change the import command to point to the local module,
that way you freeze the version and reduce dependencies.

```
df=pd.read_excel("mydata.xlsx")

df_profile= profile_dataframe(df) # will return a df with summary statistics

# you may realise the columns from excel are all over the place with cases and
# special chars

cleanup_column_names(df,inplace=True) # use of inplace, otherwise it returns a new copy

df_deduped=check_duplicates(df, columns=["customer_id","last_update_date"],ascending=[True,False],keep="first",indicator=True, also_return_non_duplicates=True)

# you will get a nice output with the report on duplicates, retaining the last
# modification entry (via the pre-sort descending by date) and returning 
# the non-duplicates,  
# It also brings a boolean column flagging those that had a duplication removed.


```

## Requires
- Python >= 3.10
- Pandas >= 1.5.0
- Numpy >= 1.24
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
- ```pylint``` for linting 
- ```black``` for style 
- ```pytest``` for testing 
- ```sphinx``` for documentation in RTD 
- ```myst_parser``` is a requirement for RTD too 
- ```poetry``` for packaging. 



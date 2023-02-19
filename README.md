
## Introduction to Pydit 

Pydit is a library of common data munging tools that an internal auditor may need to apply. 

This library is (also) a learning exercise for me on how to create a package, build documentation & tests, and publish it

The code quality is still low, marginally better than pasting from SO.
Use it at your own peril :) 

If you wish to contribute pls get in touch.


Most of these functions boil down to short(ish) snippet of code using existing feature in pandas, numpy or standard python libraries. 
E.g. cleanup field names or to do some duplicates checks, Benford, etc. 

Btw, Pydit takes a lot of inspiration (and code) from Pyjanitor, an awesome library!


The problem Pydit tries to solve is that all these cleanup and checks snippets start to crop up everywhere, often pasted from internet or from recent version used in another script with no consistency or tests.

Libraries like pyjanitor do a great job but tend to be compact and non verbose, for interal audit tests, we really want super-verbose and very easy to understand code and outputs. 

So for pydit I follow the following principles:

1.  functions are self standing, minimising imports/dependencies. 

The auditor should be able to pluck and import an individual module from pydit to use only those functions directly in the audit test, making it easier to undertand it, document the test done and peer-review the whole thing.
Also, that means no dependencies on future versions of the pydit library breaking the code (an audit test may be only revisited one or two years from now).

2. functions include verbose logging to explain what is going on. Another feature specifically useful for the Internal Audit use case.

3. focus on documentation, tests, and simple code, less concern on performance.

4. no method chaining, in interest of source code readability.  

Pyjanitor is great and its chaining approach is elegant and compact. Definitely one to have in the toolbox. 

However, I have found it better for documenting the audit test, to check and show all the intermediate steps/results. 

5. Default behaviour is to return a new or a transformed copy of the object and not mutate the input object(s). The "inplace=True" option should be available if feasible.



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



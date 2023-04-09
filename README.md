
## Introduction to Pydit 

Pydit is a library of data wrangling tools for use by internal auditors 
specifically for our typical use cases, see below explanation.

This library is also a learning exercise for me on how to create a package, build documentation & tests, and publish it. The code quality is marginally better than pasting from Stack Overflow.
So, use it at your own peril! :) 
If you wish to contribute, get in touch.

Most of these tools could be done as short/obscure code snippets using existing feature in pandas, numpy or standard python libraries. 
E.g. cleanup field names or to do some duplicates checks, or apply Benford law.

Btw, Pydit takes inspiration (and some code) from Pyjanitor, an awesome library, check it out!

Why a dedicated library for auditors?

The problem Pydit tries to solve is that all these cleanup and checks (e.g. extract duplicates) snippets are quite important for our work and start to crop up everywhere, often pasted from internet or from recent version used in another script with no consistency or tests.

On the other hand, libraries like pyjanitor do a great job but a) require installation that often is not allowed in your environment b) tend to be compact and non verbose (and use method chaining) and c) are difficult to verify given the high complexity of the library overall.

For interal audit tests, what we really need is super-verbose and very easy to understand/verify code and outputs, to follow step by step. 
Most of the time, for a one/few time/s use and performance is secondary.

So, Pydit follows the following principles:

1.  Functions are self-standing, minimal imports/dependencies. 

The auditor should be able to import any pydit's individual module and use only those functions in the audit test. That makes it easier to undertand, document the test done and peer-review.
Also, reduces dependencies of future versions of pydit. For better or 
worse, you file the code used as it was ran during the audit.

2. Functions include verbose logging to explain what is going on. Another feature specifically useful for the Internal Audit use case.

3. Focus on documentation, tests, and simple code, less concern on performance.

4. No method chaining, in interest of source code readability. 

Pyjanitor is great and its chaining approach is elegant and compact. Definitely one to have in the toolbox. However, I have found it better for documenting the audit test, to check and show all the intermediate steps/results. 

5. The default behaviour is to return a new or a transformed copy of the object and not mutate the input object(s). The "inplace=True" option should be available if feasible.



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



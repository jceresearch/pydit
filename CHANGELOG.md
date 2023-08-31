# Changelog

## V0.1.02

### Features

- Added lookup_values() , a sort of xlookup() for odd use cases e.g. Airtables  
which includes linked tables as list with one (or more) elements

## V0.1.01

- Changed requirements to the latest version of everything (pandas etc). 
This is due to Github actions not passing the test there while it is passing 
locally, so I will try to run in latest version and fix whatever GH doesn't like.
As soon as I sort out why I will pin a particular version.

## V0.0.18
### Fixes

- Fixed check_blanks() and coalesce_values(), some small refactoring and enhancing there too


## V0.0.17

### Features

- Added count_notna, count_isna, and has_different_values to apply to several columns in a dataframe

## V0.0.16

### Features

- added merge_smart() replacing merge_force_suffix , offering more functionality, such as prefix and optionally renaming keys or preserving them
  
## V0.0.15

### Features

- adding merge_outer_and_split to the library, which generates inner join and
    extractions for the nans and non matches.

### Fixes

- fix bug in clean string
- fixed percertage count option in count function

## V0.0.14

### Tweaks

- added silent=False option in the cleanup, groupby and coalesce functions
    to reduce the logging when used within other functions
- improved clean_string function to do unicode decoding and preserve dashes
  
### Fixes

- refactored coalesce columns to add more input validation but also accept
    columns that may not be in the dataframe, for cases where we are looping
    disparate dataframes

## V0.0.13

### Features

- Added get_latest_modif_file_from() to the filemanager.py

### Tweaks

- Duplicates returns a log warning if there are no duplicates so it is visible

## V0.0.12

### Fixes

- Fixed duplicates to return all values if there are no duplicates and
  to have clearer logging of various cases with nan.
  BREAKING CHANGES: New parameter dropna=True introduced and
  add_indicator_column=False replaces indicator=False
- keyword_search_batch() fixed to work better when limiting the output
  to hits.

### Features

- Added map_values() function to map common values to numbers and the  
  other way around. e.g. 1,2,3 to "red","amber","green" and so on.

## V0.0.11

### Fixes

- Improving tests and dosctrings
- cleanup_dataframe_columns_names now replaces $ £ € with usd, gbp and eur respectively
- requirements.txt has lifted specific version requirement for sphinx (for the documentation), otherwise it doesnt install in gitpod, no impact on main library

## V0.0.10

### Features

- Added business hours calculator module
- Upgraded filemanager, now it uses a json file to store config check the docs

### Tweaks

- Refactored sequence checks and added grouping in output

### Fixes

- profile_dataframe() fixes

## V0.0.9 (20/08/2022)

### Features

- filemanager now has yaml instead of singleton object, full rewrite

### Tweaks

- cleanup_column_names() now accepts a list in addition to a dataframe and cleans unicode accents
- keyword_search accepts labels including rollup columns
- logger now in colour and to stdout
- count_values_in_col() has percentage option

### Fixes

- keyword_search() refactoring and some bug fixes

## V0.0.8 (16/07/2022)

### Features

- keyword_search allows columns with labels and rollups for multiple patterns for variations of a single conceptual keyword
- keyword_search can bring individual hits as a "thin and long" table

### Tweaks

- coalesce_dataframe_columns supports "last" value to keep
- group_by_text concatenates better, and also added option unique=True to restrieve only unique instances
- save() now can direct to one of the channels

### Fixes

- Lots

## v0.0.7 (3/07/2022)

### Features

- Fillna_smart() improved
- Implemented a count_values_in_col(), can do combined columns
- Implemented merge_smart() to improve handling of suffixes

### Fix

- Many fixes and refactoring, most notably logging when saving and load files
- renamed count_related()

## v0.0.6 (19/06/2022)

### Fix

- Refactoring check_blanks() to be cleaner how it does the summary, better tests and a change in the default behaviour (by default is restricted to just nans)

## v0.0.5 (4/06/2022)

## Fix

- Lots of refactoring. Generally ensuring that using inplace=True returns True to avoid confusion.
- Also working on test suite to improve it

### Documentation

- working on documentation across the board, thanks Autopilot for the help, couldn't have done it without you

### Feature

- Expanding the function to create test datasets to play and to put in examples, these are not used in the core test suite

## v0.0.4 (4/06/2022)

### Fix

- Loads and loads

### Feature

- profile_dataframe() : Added an option to return a dictionary

### Documentation

- Now hosting documentation on Read the Docs
- Working through all the doctrings to make them useable

### Test suite

- Improving test suite, currently at 70%, but 3 out of 41 pending development.

## v0.0.2-3

- Various improvements

## v0.0.1 (14/05/2022)

- First release of `pydit`

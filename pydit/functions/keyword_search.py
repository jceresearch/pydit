""" 
functions to sweep a dataframe for keywords and return a matrix of matches
or a sparse matrix if the keyword list is large
"""

import logging
import re

import pandas as pd
import numpy as np
from pandas import Series, DataFrame


logger = logging.getLogger(__name__)


def keyword_search(obj_in, keywords, columns=None):
    """
    Searches the keywords in a dataframe or series and returns a matrix of matches
    """
    if not keywords:
        raise ValueError("keywords must be a list of strings or a string")
    
    if columns:
        try:
            df = obj_in[columns].copy()
        except:
            raise ValueError("Columns not found in dataframe")

    else:
        if isinstance(obj_in, Series):
            df = obj_in.to_frame()

        elif isinstance(obj_in, DataFrame):
            df = obj_in.copy()
        elif isinstance(obj_in, list):
            df = pd.DataFrame(obj_in, columns="text_data")

        else:
            raise ValueError("Type not recognised")

    if isinstance(keywords, str):
        keywords=[keywords]
    
    '''Creates a boolean column in the dataframe, one per keyword
    and a combined column that is True if any of the other columns is True.
    For simplicity we name columns sequentially as pushing keywords straight 
    as columns may yield error with special characters or duplicated/banned names
    '''
    n=1
    for re_text in keywords:
        pattern= re.compile(re_text,re.IGNORECASE)
        regmatch = np.vectorize(lambda x: bool(pattern.match(x)))
        df["kw_match"+str.zfill(str(n),2)]=regmatch(df[columns].values)
        n=n+1
    match_columns=[m for m in df.columns if "kw_match" in m]
    df["kw_match_all"]=df.apply(lambda row: any(row[match_columns]),axis=1)
    return df
    
    
    
    
    
def keyword_search_str(keyword_list,df_in, field_name):
    ''' Simpler version with no regular expressions, which is less powerful but
    could be faster if we wish to do lots of keywords on a large file, normally
    regexp are fine and can take normal keywords too, use this as an exception'''
    df=df_in.copy()
    keyword_list=[x.lower() for x in keyword_list]
    listed = df[field_name].str.lower().tolist()
    for i, kw in enumerate(keyword_list):
        df["kw_match"+str.zfill(str(i+1),2)] = [kw in n for n in listed]
    match_columns=[m for m in df.columns if "kw_match" in m]
    df["kw_match_all"]=df.apply(lambda row: any(row[match_columns]),axis=1)
    return df

#Run this for regular expression search (regexp), more powerful but could be slower
# in large datasets and a bit more prone to error as regepx can be complex
df_result=keyword_search_re(keywords,df,text_field)

#Run this for simpler keyword search instead of the regexp one
#df_result =keyword_search_str(keywords,df,'article_sentences')

#we pick only rows with hits, you could change this to bring all the dataset instead.
df_output=df_result[df_result['kw_match_all']==True]
print(f"Found: {df_output.shape[0]} rows out of {df.shape[0]} with one or more hits")
df_output.head()
    
    return

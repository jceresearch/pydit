import pandas as pd
import numpy as np
from datetime import datetime,date

def lookup_values(df,key,df_ref, key_ref,return_column, flatten_list=True, fillna=None):
    """
    Lookup values from a reference dataframe and return a list of values.
    If the key is a list, it will return a list of values


    Parameters
    ----------
    df : pandas.DataFrame
        Dataframe to lookup values from
    key : str
        Column name of the key to lookup
    df_ref : pandas.DataFrame
        External Reference Dataframe to lookup values  
    key_ref : str
        Column name of the key to lookup
    return_column : str
        Column name of the value to return
    flatten_list : bool, optional
        If True, it will return a string with the values separated by a comma. 
        The default is True.
    fillna : str, optional
        If not None, it will replace the NaN values with the value provided. 
        The default is None.

    Returns
    -------
    res_series : pandas.Series
        Series with the values looked up


    """

    if not isinstance(df_ref, pd.DataFrame):
        raise TypeError("df_ref must be a pandas.DataFrame")
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas.DataFrame")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if not isinstance(key_ref, str):
        raise TypeError("key_ref must be a string")
    if not isinstance(return_column, str):
        raise TypeError("return_column must be a string")
    if return_column not in df_ref.columns:
        raise ValueError("return_column must be a column in df_ref")
    if key_ref not in df_ref.columns:
        raise ValueError("key_ref must be a column in df_ref")
    if key not in df.columns:
        raise ValueError("key must be a column in df")
    

    def aux_lookup(keys):
        res_list=[]
        if isinstance(keys,(int,str,float,date)):
            if pd.notna(keys):
                try:
                    res_list= [df_ref.loc[df_ref[key_ref] == keys, return_column].values[0]]
                except:
                    res_list=[np.nan]
            else:
                res_list=[np.nan]
        elif isinstance(keys,(list,tuple)): 
            for element in keys:
                try:
                    res_list.append(df_ref.loc[df_ref[key_ref] == element, return_column].values[0])
                except IndexError:
                    pass
            if res_list==[]:
                res_list=[np.nan]

        else:
            res_list=[np.nan]


        if fillna is not None:
            res_list= [fillna if pd.isna(e) else e for e in res_list]

        if flatten_list:
            res_list= ", ".join([str(e) for e in res_list]) 
        
        return res_list


    res_series= df[key].apply(aux_lookup)

    return res_series


if __name__ == "__main__":
    df=pd.DataFrame(
        {'a':[[1,2],2,3,np.nan,5,6,7,8,9,10,11,[1,11],[12,13],[1,2,3,22]]})
    df_ref=pd.DataFrame(
        {'ref':[1,1,2,3,4,5,6,7,8,9,10],
        'val_1':[1,2,3,4,5,6,7,8,9,10,11],
        'val_2':["a","b","c","d","e","f","g","h","i","j","k"],
        }
    )    
    print(lookup_values (df,'a',df_ref,'ref',"val_1",flatten_list=True,fillna="NA"))


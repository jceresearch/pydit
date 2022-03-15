""" Validation functions"""

import logging

import pandas as pd
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


from pandas.api.types import is_string_dtype, is_numeric_dtype
import numpy as np


logger = logging.getLogger(__name__)


def check_benford(
    df, column=None, zeroes=True):
    """ 

    Args:
        

    Returns:
        
    """

    if not isinstance(df, pd.DataFrame):
        logger.error(
            "Expecting a dataframe, a single column dataframe is a Series and not yet supported"
        )
        return
    df = df_in.copy()
    
    thres=10
anomalies=set(dfres.sort_values("bf_diffperc", ascending=False)[0:thres]['bf_digit'])
print(anomalies)
df['bf_digit']=df[field_to_analyse].fillna(0)
df["bf_digit"]=df.apply(lambda r: int(str(abs(r['bf_digit']*100000))[0:digit])  , axis=1)
dfmerged=pd.merge(df,dfres,on='bf_digit',how='left',suffixes=(None,"_bf"+str(digit)))
dfmerged['flag_bf_anomaly']=df.apply(lambda r: True if r['bf_digit'] in anomalies else False , axis=1)
dfmerged.head()
    
    
    
    
    
    def benford_x_digit(rawdata,digit):
        data_nonzero=filter(lambda n: n !=0. , rawdata)
        data=list(data_nonzero)
        BFD= [math.log10(1.0+1.0/n) for n in range (10**(digit-1),10**digit)]
        data_count={}
        for i in range(10**(digit-1),10**digit):
            data_count[i]=0      
        data_xdigits=[int(str(abs(x*1000))[0:digit]) for x in data]
        for i in range(len(data_xdigits)):
                data_count[data_xdigits[i]]=data_count[data_xdigits[i]]+1
        list_tuples=sorted(data_count.items())
        data_count=[i[1] for i in list_tuples]
        total_count=sum(data_count)
         
        expected_count=[p * total_count for p in BFD]
        #We are not rounding/flooring here because it may be useful to have the 
        #fractions even if it doesnt make sense in real life, just to reconcile totals
        #in the dataframe wrapper I am rounding it anyway.    
        return  data_count, expected_count, BFD
    def benford_x_digit_to_dataframe(rawdata,digit):
        c,e,p = benford_x_digit(data,digit)
        ct=sum(c)
        df=pd.DataFrame(
        tuple(zip(range(10**(digit-1),10**digit),np.around(e),c,p)),
        columns=['bf_digit','bf_exp_count','bf_act_count','bf_exp_freq'])
        df['bf_act_freq']= df['bf_act_count']/ct
        df['bf_diff'] =     abs(df['bf_exp_count']-df['bf_act_count'])
        df['bf_diffperc'] = abs(df['bf_diff']/df['bf_exp_count'])        
        return df
    def plot_benford(data,digit):   
        data_count, expected_count, p =benford_x_digit(data,digit)
        y1 = expected_count
        y2 = data_count
        x= np.arange(10**(digit-1),10**digit)
        bins = np.linspace(1, 10)
        width=.35
        plt.figure(figsize=(20, 8), dpi=80)
        plt.bar(x, y2, width, label="Actual")
        plt.bar(x+width, y1, width, label="Benford")
        plt.xticks(x+width/2 , x)
        plt.legend(loc='upper right')  
        plt.show()
    
    
    
    
    return df

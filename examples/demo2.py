
#%%


from sklearn import datasets
import pandas as pd

# load iris dataset
ds = datasets.load_boston()
# Since this is a bunch, create a dataframe
df=pd.DataFrame(ds.data)
df
#%%
import pydit
pydit.profile_dataframe(df)

#%%


iris_df['class']=iris.target

iris_df.columns=['sepal_len', 'sepal_wid', 'petal_len', 'petal_wid', 'class']
iris_df.dropna(how="all", inplace=True) # remove any empty lines
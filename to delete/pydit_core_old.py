import csv
import pickle
from datetime import datetime
import pandas as pd
import re
import zipfile
import glob

def hello_world():
    print("Hello World!!!")
    return "Hello World"


def unzip_files(in_path="",out_path=""):
    files = glob.glob(in_path)
    for f in files:
        with zipfile.ZipFile(f, "r") as zip_ref:
            zip_ref.extractall(out_path)
    return True

temp_path = "c:/temp/"
output_path = "./output/"

def dedupe_list(list=[]):
    newlist = list.copy()
    for e in list:
        dupes = list.count(e)
        if dupes > 1:
            for j in range(dupes):
                pos = [i for i, n in enumerate(list) if n == e][j]
                if j == 0:
                    pass
                else:
                    newlist[pos] = e+"_"+str(j+1)
        else:
            pass
    return newlist


def clean_cols(df):
    df.columns = df.columns.str.replace(r'%', 'perc', regex=True)
    df.columns = df.columns.str.replace(r'[^a-zA-Z0-9]', ' ', regex=True)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' +', '_', regex=True)
    df.columns = df.columns.str.lower()
    if len(df.columns) != len(set(df.columns)):
        print("Identified some duplicate columns, renaming them")
        new_cols = dedupe_list(list(df.columns))
        df.columns = new_cols
    if len(df.columns) != len(set(df.columns)):
        print("Duplicated column names remain!!! check what happened!!")
        return
    return True  # returns true meaning that it is going to modify the calling dataframe "by reference"


def clean_text(t, keep_dot=False, space_to_underscore=True):
    """Sanitising text for various uses within Pandas. Excludes characters not 
    [a-zA-Z0-9] with nuances for the dot and multiple spaces.
    The purpose is just for easier typing, exporting, saving to filenames.
    Args:
        t (string]): string with the text to sanitise
        keep_dot (bool, optional): Keep the dot or not. Defaults to False.
        space_to_underscore (bool, optional): Spaces will be replaced by one underscore, False to keep spaces. Defaults to True.
    Returns:
        string: cleanup string restricted to a-
    """
    r = ""
    if t:
        r = str.lower(str(t))
        if keep_dot == True:
            r = re.sub(r'[^a-zA-Z0-9.]', " ", r)
        else:
            r = re.sub(r'[^a-zA-Z0-9]', " ", r)
        r = r.strip()
        if space_to_underscore == True:
            r = re.sub(" +", "_", r)
    return r


def save(obj, filename, bool_also_pickle=False):
    flag = False
    flag_to_csv_instead = False
    start_time = datetime.now()
    stem_name = re.sub("\.[a-zA-Z0-9_]{2,}$", "", filename)
    if isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series):
        if ".xlsx" in filename:
            if obj.shape[0] < 300000:
                print("Saving to an excel file:", output_path+filename)
                obj.to_excel(output_path+filename, index=False,
                    sheet_name=stem_name, freeze_panes=(1, 0))
                flag = True
            else:
                flag_to_csv_instead = True
                print("Too big for excel!")
            if bool_also_pickle:
                print("Saving also to a pickle file:",
                    temp_path+stem_name+".pickle")
                obj.to_pickle(temp_path+stem_name+".pickle")
        if ".csv" in filename or flag_to_csv_instead == True:
            print("Saving to csv:", temp_path+stem_name+".csv")
            obj.to_csv(temp_path+filename, index=False,
                quotechar='"', quoting=csv.QUOTE_ALL)
            flag = True
        if ".pickle" in filename or bool_also_pickle == True:
            print("Saving to pickle format in: ", temp_path+filename)
            obj.to_pickle(temp_path+stem_name+".pickle")
            flag = True
        if flag:
            print("(rows, columns) :", obj.shape)
            print("Saved columns:", list(obj.columns))
            print("Finished:", f'{datetime.now():%Y-%m-%d %H:%M:%S}', " - ", round(
                (datetime.now()-start_time).total_seconds() / 60.0, 2), " mins")
        else:
            print("Name not recognised, nothing saved")
    else:
        if ".pickle" in filename:
            with open(temp_path+filename, 'wb') as handle:
                pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Saved pickle to "+filename,
                    round((handle.tell()/1024)/1024, 1), " MB")
                print(datetime.now())
        else:
            print("Nothing saved, format not recognised")


def load(filename):
    stem_name = re.sub("\.[a-zA-Z0-9_]{2,}$", "", filename)
    if ".pickle" in filename:
        # df=pd.read_pickle(temp_path+filename)
        with open(temp_path+filename, 'rb') as handle:
            obj = pickle.load(handle)
            print("Loaded pickle from: "+temp_path+filename, " Size:",
                round((handle.tell()/1024)/1024, 1), " MB")
    if ".xlsx" in filename:
        try:
            obj = pd.read_excel(output_path+filename)
            print(output_path+filename)
        except:
            obj = pd.read_excel(temp_path+filename)
            print(temp_path+filename)
    if ".csv" in filename:
        try:
            obj = pd.read_csv(output_path+filename)
            print(output_path+filename)
        except:
            obj = pd.read_csv(temp_path+filename)
            print(temp_path+filename)
    print(datetime.now())
    if isinstance(obj, pd.DataFrame):
        print(obj.shape)
        print(list(obj.columns))
    else:
        try:
            print(len(obj))
        except:
            pass
    print(datetime.now())
    return obj


def main():
    '''
    '''
    print("aux functions")


if __name__ == '__main__':
    main()

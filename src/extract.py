import pandas as pd

## 從csv提取資料
## list[0] = col(欄位) , list[1] = row(前10筆資料)
def extract_by_csv(file_name:str)->list:
    mData = list()
    df = pd.read_csv(f"data/{file_name}.csv")
    mData.append(df.columns.to_list())
    mData.append(df.head(10).values.tolist())
    return mData

## 從DataFrame提取資料
## list[0] = col(欄位) , list[1] = row(前10筆資料)
def extract_by_DF(df:pd.DataFrame)->list:
    mData = list()
    mData.append(df.columns.to_list())
    mData.append(df.head(10).values.tolist())
    return mData
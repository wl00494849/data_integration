import pandas as pd

## 在向量表中新增資料下載網址url
## df1詞向量表csv
df1 = pd.read_csv("dataset/dataset_dimension_large.csv")
## df2資料集清單csv
df2 = pd.read_csv("dataset/OpenDataSet_2025_3_24.csv")

merged = pd.merge(
    df1, df2[["資料集名稱", "資料下載網址"]],
    left_on="dataset_Name", right_on="資料集名稱", how="left"
)
result = merged[["dataset_Name", "dimension", "資料下載網址"]]
result = result.rename(columns={"資料下載網址": "url"})

result.to_csv('dataset/Datalist_VectorTable')

print(result[['dataset_Name','url']])
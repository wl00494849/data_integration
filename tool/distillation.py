import requests
from src.chat import Chat
from dotenv import load_dotenv
import logging
from datetime import datetime
import pandas as pd
import numpy as np

## 把資料集名稱分批傳入Text Embedding API取得詞向量
def distillation():
    gpt = Chat()
    ## df取資料集清單metadata
    df = pd.read_csv("dataset/OpenDataSet_2025_2_24.csv")
    dataName = df['資料集名稱'].values
    ## dataName len = 52201
    ## MAX_TOKENS = 8192
    li = []
    max = 52201
    slide = 150
    x = 0
    while 1:
        if max - x > slide:
            target = dataName[x:x+slide]
            res = gpt.get_vector(target,1)
            for i in range(len(res)):
                li.append([target[i],res[i].embedding])
            x = x + slide
        else:
            target = dataName[x:max]
            res = gpt.get_vector(target,1)
            for i in range(len(res)):
                li.append([target[i],res[i].embedding])
            break

    new_df = pd.DataFrame(li, columns=['dataset_Name','dimension'])
    new_df.to_csv('dataset/dataset_dimension_large.csv', index=False)

distillation()
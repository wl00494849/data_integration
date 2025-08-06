from src.chat import Chat
from src.heap import max_heap,kv
from sklearn.metrics.pairwise import cosine_similarity
from src.integration import Data_Integration
import pandas as pd
import numpy as np
import requests

print("Loading Model.....")
df = pd.read_csv('dataset/DataList_VectorTable.csv')
print("Compelet.....")

## 用餘弦相似度搜尋資料
def search_file(keyword:str,top:int=15):
    gpt = Chat()
    heap = max_heap()
    exist = df['dimension'][df['dataset_Name'].isin([keyword])]
    if len(exist) == 0:
        target = gpt.get_vector(keyword,1)[0].embedding
        target = np.array(target).reshape(1, -1)
    else:
        target = np.array([float(x) for x in exist.values[0].strip('[]').split(',')]).reshape(1, -1)
    
    for item in df.values:
        di = np.array([float(x) for x in item[1].strip('[]').split(',')]).reshape(1, -1)
        cos = cosine_similarity(target,di)
        heap.push(kv(item[0],cos))

    li = list()

    for i in range(top):
        p = heap.pop()
        li.append(p.k)
        print(f"{i}.{p.k}:{p.v[0]}")

    return li

## 下載資料
def downloadSearchFile(fileName1:str,fileName2):
    url1 = df[df['dataset_Name'] == fileName1]['url'].iloc[0]
    url2 = df[df['dataset_Name'] == fileName2]['url'].iloc[0]

    csv_url1 = None
    csv_url2 = None

    ##只取CSV檔
    csv_url1 = [u.strip() for u in url1.split(";")           
                       if u.strip().lower().endswith(".csv")]  

    csv_url2 = [u.strip() for u in url2.split(";")           
                       if u.strip().lower().endswith(".csv")]  
        
    print(fileName1)
    print(csv_url1)
    print(fileName2)
    print(csv_url2)

    response1 = requests.get(csv_url1[0])
    response2 = requests.get(csv_url2[0])

    with open(f"temp/{fileName1}.csv",'wb') as f:
        f.write(response1.content)
    with open(f"temp/{fileName2}.csv",'wb') as f:
        f.write(response2.content)

    
    



import pandas as pd
import requests
import os
from datetime import datetime

##下載政府開放資料集清單

time = datetime.now()
fileName = f"dataset/OpenDataSet_{time.year}_{time.month}_{time.day}.csv"
domain_Url = 'https://data.gov.tw/api/front/dataset/export?format=csv'

def get_dataset():
    if not os.path.exists(fileName):
        response = requests.get(domain_Url)
        with open(fileName, 'wb') as f:
            f.write(response.content)
    
get_dataset()
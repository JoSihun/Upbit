import numpy as np
import pandas as pd
import requests

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

url = 'https://api.upbit.com/v1/market/all'
response = requests.get(url).json()



df = pd.DataFrame(columns=['MARKET_CODE', 'NAME_ENG', 'NAME_KOR'])
for market in response:
    if market['market'].startswith('KRW') == True:
        df['MARKET_CODE'] = market['market']
        df['NAME_ENG'] = market['english_name']
        df['NAME_KOR'] = market['korean_name']
print(df)
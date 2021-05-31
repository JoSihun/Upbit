import numpy as np
import pandas as pd
import requests, pyupbit

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

url = 'https://api.upbit.com/v1/market/all'
response = requests.get(url).json()

columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'MAX_PRICE',
           'BUY_PRICE', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_KOR']
dfMarket = pd.DataFrame(columns=columns)

# SECRET_KEY = 'iSCwJ7YAkU4sait93qhrMdYqlyi3FxzWAkP3Ct1q'
# ACCESS_KEY = 'G0PsoHONIqtJbUXLeMSvbpbYv0bk0eOtxcqkWXGF'
SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY= 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)
for balance in upbit.get_balances()[1:]:
    dfNew = pd.DataFrame({'BUY_PRICE': [balance['avg_buy_price']]})
    dfMarket = pd.concat([dfMarket, dfNew], axis=0, ignore_index=True)
    print(balance)


print(dfMarket)



# df = pd.DataFrame(columns=['MARKET_CODE', 'NAME_ENG', 'NAME_KOR'])
# for market in response:
#     if market['market'].startswith('KRW') == True:
#         df['MARKET_CODE'] = market['market']
#         df['NAME_ENG'] = market['english_name']
#         df['NAME_KOR'] = market['korean_name']
# print(df)
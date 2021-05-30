# -*- coding: utf-8 -*-

# Pandas 정렬: https://appia.tistory.com/196
# Pandas 인덱스 활용 및 정렬: https://yganalyst.github.io/data_handling/Pd_2/
# Pnadas DataFrame 병합: https://yganalyst.github.io/data_handling/Pd_12/

import os, sys, shutil, time
import numpy as np
import pandas as pd
import requests, pyupbit

def get_time_header():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]

    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    header = f'[{date}, {now} GMT{timezone}]'

    return header

PERCHASE_PRICE = 100000     # 종목당 실거래금액
SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    upbit = pyupbit.Upbit(SECRET_KEY, ACCESS_KEY)


    urlMarket = 'https://api.upbit.com/v1/market/all'
    resMarket = requests.get(urlMarket).json()

    dfMarket = pd.DataFrame(columns=['market', 'english_name', 'korean_name'])

    for market in resMarket:
        if market['market'].startswith('KRW') == True:
            urlCoin = 'https://api.upbit.com/v1/ticker?markets=' + market['market']
            resCoin = requests.get(urlCoin).json()
            dfNew2 = pd.DataFrame(resCoin)[['trade_price', 'high_price', 'low_price', 'acc_trade_volume', 'signed_change_rate']]
            dfNew1 = pd.DataFrame([market])
            dfNew = pd.concat([dfNew1, dfNew2], axis=1, ignore_index=False)
            time.sleep(0.07)

            if (dfMarket['market'] == market['market']).any():
                dfMarket[dfMarket['market'] == market['market']] = dfNew
                print('True')
            else:
                dfMarket = pd.concat([dfMarket, dfNew], axis=0, ignore_index=True)
        dfMarket = dfMarket.sort_values(by=['signed_change_rate'], ascending=False)  # 내림차순 정렬
        #dfMarket['signed_change_rate'] = (dfMarket['signed_change_rate'] * 100)  # 전일대비 %표기
        dfMarket = dfMarket[['market', 'english_name', 'trade_price', 'signed_change_rate', 'acc_trade_volume', 'korean_name']]
        #dfMarket.columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'VOLUME', 'NAME_KOR']
        dfMarket.reset_index(drop=True, inplace=True)  # drop: 기존 인덱스 재배열, inplace: 새 변수에 넣을 필요 없음


        os.system('cls')
        print(dfMarket[:20])

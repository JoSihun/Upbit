# -*- coding: utf-8 -*-

# Pandas 정렬: https://appia.tistory.com/196
# Pandas 인덱스 활용 및 정렬: https://yganalyst.github.io/data_handling/Pd_2/
# Pnadas DataFrame 병합: https://yganalyst.github.io/data_handling/Pd_12/

import os, sys, shutil, time
import numpy as np
import pandas as pd
import requests, pyupbit

def get_time_str():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]

    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    str_now = f'[{date}, {now} GMT{timezone}]'

    return str_now

def get_prices_all():
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url).json()

    dataframe = pd.DataFrame()
    for item in response:
        if item['market'].startswith('KRW'):
            url = 'https://api.upbit.com/v1/ticker?markets=' + item['market']
            response = requests.get(url).json()
            print(f'{get_time_str()} {url}')

            new_dataframe1 = pd.DataFrame([item])
            new_dataframe2 = pd.DataFrame(response)[['trade_price', 'high_price', 'low_price', 'acc_trade_volume', 'signed_change_rate']]
            new_dataframe = pd.concat([new_dataframe1, new_dataframe2], axis=1, ignore_index=False)

            dataframe = pd.concat([dataframe, new_dataframe], axis=0, ignore_index=True)
            time.sleep(0.07)
    dataframe = dataframe.sort_values(by=['signed_change_rate'], ascending=False)   # 전일대비기준 내림차순 정렬
    dataframe['signed_change_rate'] = (dataframe['signed_change_rate'] * 100)       # 전일대비 %표기
    dataframe = dataframe[['market', 'english_name', 'high_price', 'low_price', 'trade_price', 'signed_change_rate', 'acc_trade_volume', 'korean_name']]
    dataframe.columns = ['MARKET_CODE', 'NAME_ENG', 'MAX_PRICE', 'MIN_PRICE', 'PRICE_NOW', 'RATE', 'VOLUME', 'NAME_KOR']
    dataframe.reset_index(drop=True, inplace=True)      # drop: 기존 인덱스 재배열, inplace: 새 변수에 넣을 필요 없음

    return dataframe

class Coin:
    num_coins = 0
    prices_all = pd.DataFrame()

    def buy(self):
        Coin.num_coins += 1
    def sell(self):
        Coin.num_coins -= 1





SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
PERCHASE_PRICE = 100000     # 종목당 실거래금액
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    upbit = pyupbit.Upbit(SECRET_KEY, ACCESS_KEY)

    while True:
        prices = get_prices_all()
        Coin.prices_all = prices

        if Coin.num_coins < 20:
            Coin.buy()

        print(prices[:20])
        os.system('cls')




    exit(0)





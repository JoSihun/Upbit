# -*- coding: utf-8 -*-

# Pandas 정렬: https://appia.tistory.com/196
# Pandas 인덱스 활용 및 정렬: https://yganalyst.github.io/data_handling/Pd_2/
# Pnadas DataFrame 병합: https://yganalyst.github.io/data_handling/Pd_12/

import os, sys, shutil, time
import numpy as np
import pandas as pd
import requests, pyupbit

def get_time_header():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]
    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    header = f'[{date}, {now} GMT{timezone}]'

    return header

def get_coin_names():
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url).json()

    markets = []
    for market in response:
        if market['market'].startswith('KRW'):
            data = dict()
            data['MARKET_CODE'] = market.pop('market')
            data['NAME_ENG'] = market.pop('english_name')
            data['NAME_KOR'] = market.pop('korean_name')
            markets.append(data)
    return markets

def get_coin_information(market_code='KRW-BTC'):
    url = 'https://api.upbit.com/v1/ticker?markets=' + market_code
    response = requests.get(url).json()[0]
    data = dict()

    data['MARKET_CODE'] = response['market']
    data['MIN_PRICE'] = response['low_price']
    data['MAX_PRICE'] = response['high_price']
    data['PRICE_NOW'] = response['trade_price']
    data['RATE'] = response['signed_change_rate']
    data['VOLUME'] = response['acc_trade_volume']
    return [data]



PERCHASE_PRICE = 100000     # 종목당 실거래금액
SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
# SECRET_KEY = 'iSCwJ7YAkU4sait93qhrMdYqlyi3FxzWAkP3Ct1q'
# ACCESS_KEY = 'G0PsoHONIqtJbUXLeMSvbpbYv0bk0eOtxcqkWXGF'
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.unicode.east_asian_width', True)
    upbit = pyupbit.Upbit(SECRET_KEY, ACCESS_KEY)

    # KRW MARKET BASE DATAFRAME 만들기
    columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'MAX_PRICE',
               'BUY_PRICE', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_KOR']
    dfMarket = pd.DataFrame(columns=columns)
    dfNames = pd.DataFrame(get_coin_names())
    dfMarket = pd.concat([dfMarket, dfNames], axis=0, ignore_index=True)

    # RealTime KRW MARKET Information 갱신, While문 추가할 것
    while True:
        start_time = time.time()
        for idx, row in dfMarket.iterrows():
            dfCoin = pd.DataFrame(get_coin_information(row['MARKET_CODE']))
            dfCoin.set_index('MARKET_CODE', inplace=True)
            dfMarket.set_index('MARKET_CODE', inplace=True)
            dfMarket.update(dfCoin)

            dfMarket.reset_index(drop=False, inplace=True)  # drop: 기존 인덱스 삭제여부, inplace: 새 변수에 넣을 필요 없음
            dfMarket = dfMarket.sort_values(by=['RATE'], ascending=False)  # 내림차순 정렬
            time.sleep(0.07)

            os.system('cls')
            print(dfMarket[:20])
            print(f'경과시간: {time.time() - start_time}')






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
    data['RATE'] = str(round(response['signed_change_rate'] * 100, 2)) + ' %'
    data['VOLUME'] = response['acc_trade_volume']
    return data


# 일단은 DataFrame 형태로 return, 추후 리스트던 데이터프레임이던 획일화 진행해야함
def get_holdings():
    columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'MAX_PRICE',
               'BUY_PRICE', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_KOR']
    dfHoldings = pd.DataFrame(columns=columns)

    data = dict()
    for balance in upbit.get_balances()[1:]:
        market_code = balance['unit_currency'] + '-' + balance['currency']
        if market_code == 'KRW-VTHO': continue

        data['MARKET_CODE'] = market_code
        data['BUY_PRICE'] = balance['avg_buy_price']

        dfMCODE = pd.DataFrame([{'MARKET_CODE': market_code}])
        dfHoldings = pd.concat([dfHoldings, dfMCODE], axis=0, ignore_index=True)

        dfCoin1 = pd.DataFrame(get_coin_information(market_code))
        profit = round(float(dfCoin1['PRICE_NOW'].values[0]) / float(balance['avg_buy_price']) * 100 - 100, 2)
        profit = str(profit) + ' %'
        dfCoin2 = pd.DataFrame([{'MARKET_CODE': market_code,
                                 'BUY_PRICE': balance['avg_buy_price'],
                                 'PROFIT': profit}])

        dfCoin1.set_index('MARKET_CODE', inplace=True)
        dfCoin2.set_index('MARKET_CODE', inplace=True)
        dfHoldings.set_index('MARKET_CODE', inplace=True)
        dfHoldings.update(dfCoin1)
        dfHoldings.update(dfCoin2)

        dfHoldings = dfHoldings.sort_values(by=['RATE'], ascending=False)  # 내림차순 정렬
        dfHoldings.reset_index(drop=False, inplace=True)  # drop: 기존 인덱스컬럼 삭제여부, inplace: 새 변수에 넣을 필요 없음

        time.sleep(0.07)

    # dfHoldingsList = dfHoldings.to_dict('records')
    return dfHoldings


PERCHASE_PRICE = 100000  # 종목당 실거래금액
SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)
# SECRET_KEY = 'iSCwJ7YAkU4sait93qhrMdYqlyi3FxzWAkP3Ct1q'
# ACCESS_KEY = 'G0PsoHONIqtJbUXLeMSvbpbYv0bk0eOtxcqkWXGF'
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.unicode.east_asian_width', True)

    for balance in upbit.get_balances():
        print(balance)

    exit(0)

    # KRW MARKET BASE DATAFRAME 만들기
    columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'MAX_PRICE',
               'BUY_PRICE', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_KOR']
    markets = get_coin_names()
    for market in markets:
        coinInformation = get_coin_information(market['MARKET_CODE'])
        market.update(coinInformation)
        time.sleep(0.07)
    dfMarket = pd.DataFrame(columns=columns, data=markets)










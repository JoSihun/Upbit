import time
import numpy as np
import pandas as pd
import requests, pyupbit

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
    return [data]


# SECRET_KEY = 'iSCwJ7YAkU4sait93qhrMdYqlyi3FxzWAkP3Ct1q'
# ACCESS_KEY = 'G0PsoHONIqtJbUXLeMSvbpbYv0bk0eOtxcqkWXGF'
SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY= 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

url = 'https://api.upbit.com/v1/market/all'
response = requests.get(url).json()


# dict형태로 리턴 or DataFrame형태로 리턴
# return 데이터 형태를 결정해야함, 아직 결정하지 못함
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
    print(dfHoldings)
    print(dfHoldings.to_dict('records'))

get_holdings()




# df = pd.DataFrame(columns=['MARKET_CODE', 'NAME_ENG', 'NAME_KOR'])
# for market in response:
#     if market['market'].startswith('KRW') == True:
#         df['MARKET_CODE'] = market['market']
#         df['NAME_ENG'] = market['english_name']
#         df['NAME_KOR'] = market['korean_name']
# print(df)
# -*- coding: utf-8 -*-

# Pandas 정렬: https://appia.tistory.com/196
# Pandas 인덱스 활용 및 정렬: https://yganalyst.github.io/data_handling/Pd_2/
# Pnadas DataFrame 병합: https://yganalyst.github.io/data_handling/Pd_12/

import os, sys, shutil, time
import numpy as np
import pandas as pd
import requests, pyupbit


class Coin:
    num_coins = 0
    market_dataframe = pd.DataFrame()       # Market 전체 데이터 프레임

    # df.loc[(df['MARKET_CODE'] == 'KRW-EOS')]                      # Dataframe 단일조건
    # df.loc[(df['MARKET_CODE'] == 'KRW-EOS') | (df['RATE'] > 0)]   # Dataframe 다중조건

    def __init__(self, market_code, name_kor, name_eng):
        self.market_code = market_code      # 종목코드
        self.name_kor = name_kor            # 한글이름
        self.name_eng = name_eng            # 영어이름

        url = f'https://api.upbit.com/v1/ticker?markets={self.market_code}'
        response = requests.get(url).json()[0]
        self.price_now = response['trade_price']    # 현재가
        self.max_price = response['trade_price']    # 최고가
        self.min_price = response['trade_price']    # 최저가
        self.price_buy = response['trade_price']    # 매수가

        self.rate = response['signed_change_rate']  # 전일대비
        self.volume = response['acc_trade_volume']  # 거래량
        self.profit = 0                             # 평가손익
        Coin.num_coins += 1

    def update(self):
        url = f'https://api.upbit.com/v1/ticker?markets={self.market_code}'
        response = requests.get(url).json()[0]
        self.rate = response['signed_change_rate']  # 전일대비
        self.volume = response['acc_trade_volume']  # 거래량

        self.price_now = response['trade_price']    # 현재가
        if self.max_price < self.price_now:
            self.max_price = self.price_now
        if self.min_price > self.price_now:
            self.min_price = self.price_now
        self.profit = self.price_now / self.price_buy - 1

    def buy(self):
        if self.price_now > self.min_price * 1.05:
            pass

    def sell(self):
        if self.price_now < self.max_price * 0.95:
            pass

    def view(self):
        values = [[self.market_code, self.name_eng, self.price_now, self.rate, self.max_price,
                   self.price_buy, self.min_price, self.profit, self.volume, self.name_kor]]
        index = ['BUY', 'HOLD', 'SELL']
        columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'MAX_PRICE',
                   'PRICE_BUY', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_KOR']
        df = pd.DataFrame(values, index, columns)
        print(df)

    def __del__(self):
        Coin.num_coins -= 1

def get_time_str():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]

    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    str_now = f'[{date}, {now} GMT{timezone}]'

    return str_now

def get_tickers(option='KRW'):
    timeHeader = get_time_str()
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url)
    markets_all = response.json()
    print(f'{timeHeader} Obtaining All Market Informations...')

    TICKERS_BTC = []
    TICKERS_KRW = []
    TICKERS_USDT = []
    print(f'{timeHeader} {url}\n')
    for item in markets_all:
        if item['market'].startswith('BTC'):
            TICKERS_BTC.append(item)
        if item['market'].startswith('KRW'):
            TICKERS_KRW.append(item)
        if item['market'].startswith('USDT'):
            TICKERS_USDT.append(item)

    if option == 'BTC':
        return TICKERS_BTC
    if option == 'KRW':
        return TICKERS_KRW
    if option == 'USDT':
        return TICKERS_USDT
    if option == 'ALL':
        return TICKERS_BTC, TICKERS_KRW, TICKERS_USDT

def get_prices(TICKERS):
    timeHeader = get_time_str()
    url = 'https://api.upbit.com/v1/ticker?markets='
    print(f'{get_time_str()} Obtaining Trade Informations...')

    PRICES = []
    for TICKER in TICKERS:
        print(f'{timeHeader} {url}' + TICKER['market'])
        response = requests.get(url + TICKER['market'])
        TICK = response.json()
        time.sleep(0.1)

        coin_code = TICKER['market']  # 종목코드
        coin_name = TICKER['korean_name']  # 코인이름
        trade_price = TICK[0]['trade_price']  # 현재가
        trade_volume = TICK[0]['acc_trade_volume'] # 거래량, 거래량이 아니라 체결량인듯
        change_rate = TICK[0]['signed_change_rate']  # 전일대비(-%포함)
        PRICES.append({'종목코드': coin_code,
                       '코인이름': coin_name,
                       '현재가': trade_price,
                       '전일대비': change_rate,
                       '거래량': trade_volume})

    print(f'{timeHeader} Sorting Trade Informations...')
    return sorted(PRICES, key=lambda PRICE: PRICE['전일대비'], reverse=True)

SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
PERCHASE_PRICE = 100000     # 종목당 실거래금액

# 실시간 관측정보
# 1) 상위 20개 종목정보
# ㄴ 모든 정보 120개를 상시 관찰하여 상위 20개 종목을 갱신해야함
# ㄴ 0.1s * 120 = 12s
# 2) 보유 20개 종목정보
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
    dataframe = dataframe.sort_values(by=['signed_change_rate'], ascending=False)   # 내림차순 정렬
    dataframe['signed_change_rate'] = (dataframe['signed_change_rate'] * 100)       # 전일대비 %표기
    dataframe = dataframe[['market', 'english_name', 'trade_price', 'signed_change_rate', 'acc_trade_volume', 'korean_name']]
    dataframe.columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'VOLUME', 'NAME_KOR']
    dataframe.reset_index(drop=True, inplace=True)      # drop: 기존 인덱스 재배열, inplace: 새 변수에 넣을 필요 없음

    return dataframe





if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    upbit = pyupbit.Upbit(SECRET_KEY, ACCESS_KEY)
    test_coin = Coin("KRW-ETC", "이더리움클래식", "EtheriumClassic")

    PRICES_ALL = get_prices_all()       # Coin Class변수에 넣는게 나을 것 같음
    print(PRICES_ALL)
    exit(0)

    TOP20 = []
    MYCOINS = []
    while True:
        # 전일대비 상승률 TOP 20개 종목


        # 보유중인 종목
        test_coin.update()
        test_coin.view()
        print(f'Number of Holding Coins = {Coin.num_coins}')
        time.sleep(0.1)
        os.system('cls')


# -*- coding: utf-8 -*-

import os, sys, shutil, time
import numpy as np
import pandas as pd
import requests, pyupbit


class Coin:
    num_coins = 0

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

SECRET_KEY = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
ACCESS_KEY = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
PERCHASE_PRICE = 100000     # 종목당 실거래금액

# 실시간 관측정보
# 1) 상위 20개 종목정보
# ㄴ 모든 정보 120개를 상시 관찰하여 상위 20개 종목을 갱신해야함
# ㄴ 0.1s * 120 = 12s
# 2) 보유 20개 종목정보

if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    upbit = pyupbit.Upbit(SECRET_KEY, ACCESS_KEY)
    test_coin = Coin("KRW-ETC", "이더리움클래식", "EtheriumClassic")

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


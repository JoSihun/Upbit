import os, shutil, time
import requests, pyupbit

class Coin:
    num_coins = 0

    def __init__(self, market_code, name_kor, name_eng, ):
        self.market_code = market_code  # 종목코드
        self.name_kor = name_kor            # 한글이름
        self.name_eng = name_eng            # 영어이름

        url = 'https://api.upbit.com/v1/ticker?markets=' + self.market_code
        response = requests.get(url).json()
        self.purchase_price = response[0]['trade_price']
        self.change_rate = response[0]['signed_change_rate']
        self.trade_volume = response[0]['acc_trade_volume']

        self.max_price = response[0]['trade_price']
        self.min_price = response[0]['trade_price']
        self.current_price = response[0]['trade_price']
        self.increase_rate = 0
        Coin.num_coins += 1

    def update(self):
        url = 'https://api.upbit.com/v1/ticker?markets=' + self.market_code
        response = requests.get(url).json()
        self.change_rate = response[0]['signed_change_rate']
        self.trade_volume = response[0]['acc_trade_volume']

        self.current_price = response[0]['trade_price']
        if self.max_price < self.current_price:
            self.max_price = self.current_price
        if self.min_price > self.current_price:
            self.min_price = self.current_price
        self.increase_rate = self.current_price / self.purchase_price - 1

    def buy(self):
        if self.current_price > self.min_price * 1.05:
            pass

    def sell(self):
        if self.current_price < self.max_price * 0.95:
            pass

    def view(self):
        print('[보유정보]', end=' ')
        print('{}: {:<12}'.format('종목코드', self.market_code), end='')
        print('{}: {:>6.2f}'.format('전일대비', self.change_rate * 100), end='%   ')
        print('{}: {:>8,}'.format('최고가', self.max_price), end='원   ')
        print('{}: {:>8,}'.format('최저가', self.min_price), end='원   ')
        print('{}: {:>8,}'.format('매수가', self.purchase_price), end='원   ')
        print('{}: {:>8,}'.format('현재가', self.current_price), end='원   ')
        print('{}: {:>6.2f}'.format('평가손익', self.increase_rate * 100), end='%   ')
        #print('{}: {:>18,.2f}'.format('거래량', self.trade_volume), end='건   ')
        print('{}: {!r:15s}'.format('한글코인명', self.name_kor))
        #print('{}: {!r:15s}'.format('영문코인명', self.name_eng))

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
    upbit = pyupbit.Upbit(SECRET_KEY, ACCESS_KEY)

    test_coin = Coin("KRW-ETC", "이더리움클래식", "EtheriumClassic")

    while True:
        print(f'Number of Coins = {Coin.num_coins}')
        test_coin.update()
        test_coin.view()
        time.sleep(0.07)
        print(f'===============================================')

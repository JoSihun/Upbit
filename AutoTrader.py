import os, shutil, time
import requests, pyupbit
from pyupbit import WebSocketManager

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

def buyingTop20():
    # 매수주문(매수가, 수량): 수량=매수금액/현재가 소수점아래 8자리 => .8f
    tickers = get_tickers('KRW')
    prices = get_prices(tickers)
    for price in prices[:20]:
        print('[매수주문]', end=' ')
        print('{}: {:<12}'.format('종목코드', price['종목코드']), end='')
        print('{}: {:>6.2f}'.format('전일대비', price['전일대비'] * 100), end='%   ')
        print('{}: {:>8,}'.format('매수가', int(price['현재가'])), end='원   ')
        print('{}: {:>18,.2f}'.format('거래량', price['거래량']), end='건   ')
        print('{}: {!r:15s}'.format('한글코인명', price['코인이름']))
        #################################### 실제로 매수체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매수체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매수체결되는 코드이므로 각별한 주의요구 ####################################
        upbit.buy_market_order(price['종목코드'], PERCHASE_PRICE)   # 실제로 매수체결되는 코드 ###############################
        #################################### 실제로 매수체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매수체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매수체결되는 코드이므로 각별한 주의요구 ####################################

def sellingTop20():
    sell_list = []
    # 현재보유종목 전량매도
    for balance in upbit.get_balances():
        if balance['currency'] == 'KRW': continue
        sell_list.append({'종목코드': 'KRW-'+balance['currency']})
        #################################### 실제로 매도체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매도체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매도체결되는 코드이므로 각별한 주의요구 ####################################
        upbit.sell_market_order('KRW-' + balance['currency'], balance['balance'])   # 실제로 매도체결되는 코드 #############
        #################################### 실제로 매도체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매도체결되는 코드이므로 각별한 주의요구 ####################################
        #################################### 실제로 매도체결되는 코드이므로 각별한 주의요구 ####################################

    sold_list = []
    PRICES = get_prices(get_tickers())
    for price in PRICES:
        for sell in sell_list:
            if price['종목코드'] == sell['종목코드']:
                sold_list.append({'종목코드': price['종목코드'],
                                  '코인이름': price['코인이름'],
                                  '현재가': price['현재가'],
                                  '전일대비': price['전일대비'],
                                  '거래량': price['거래량']})

    for price in sold_list[:20]:
        print('[매도주문]', end=' ')
        print('{}: {:<12}'.format('종목코드', price['종목코드']), end='')
        print('{}: {:>6.2f}'.format('전일대비', price['전일대비'] * 100), end='%   ')
        print('{}: {:>8,}'.format('매도가', int(price['현재가'])), end='원   ')
        print('{}: {:>18,.2f}'.format('거래량', price['거래량']), end='건   ')
        print('{}: {!r:15s}'.format('한글코인명', price['코인이름']))
        # upbit.buy_market_order(price['종목코드'], PERCHASE_PRICE)

secret_key = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
access_key = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
upbit = pyupbit.Upbit(access_key, secret_key)

PERCHASE_PRICE = 150000
if __name__ == "__main__":
    option = input('옵션입력(매수: buy, 매도: sell): ')
    if option == 'buy':
        buyingTop20()         # 매수주문
    elif option == 'sell':
        sellingTop20()        # 매도주문

    print(f'보유 KRW {int(upbit.get_balance("KRW")):,}원')
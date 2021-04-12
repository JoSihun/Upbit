import pyupbit
import requests

def get_current_prices(coins):
    if len(coins) > 100:
        prices1 = pyupbit.get_current_price(coins[:100])
        prices2 = pyupbit.get_current_price(coins[100:])
        return {**prices1, **prices2}
    else:
        prices = pyupbit.get_current_price(coins)
        return prices

def get_coin_name(fiat=''):
    # Get Market Information
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url)
    markets_all = response.json()
    print(f'[' + response.headers['Date'] + f'] {url}')

    markets_btc = []
    markets_krw = []
    markets_usdt = []
    for item in markets_all:
        if item['market'].startswith('BTC'):
            markets_btc.append(item)
        if item['market'].startswith('KRW'):
            markets_krw.append(item)
        if item['market'].startswith('USDT'):
            markets_usdt.append(item)
    return  markets_btc, markets_krw, markets_usdt



COINS_BTC = pyupbit.get_tickers(fiat='BTC')
COINS_KRW = pyupbit.get_tickers(fiat='KRW')
COINS_USDT = pyupbit.get_tickers(fiat='USDT')

PRICES_BTC = get_current_prices(COINS_BTC)
PRICES_KRW = get_current_prices(COINS_KRW)
PRICES_USDT = get_current_prices(COINS_USDT)

# PRICES_BTC = pyupbit.get_current_price(COINS_BTC)
# PRICES_KRW = pyupbit.get_current_price(COINS_KRW)
# PRICES_USDT = pyupbit.get_current_price(COINS_USDT)


if __name__ == '__main__':
    get_coin_name()


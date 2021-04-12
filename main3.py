import pyupbit

def get_current_prices(coins):
    if len(coins) > 100:
        prices1 = pyupbit.get_current_price(coins[:100])
        prices2 = pyupbit.get_current_price(coins[100:])
        return {**prices1, **prices2}
    else:
        prices = pyupbit.get_current_price(coins)
        return prices

COINS_BTC = pyupbit.get_tickers(fiat='BTC')
COINS_KRW = pyupbit.get_tickers(fiat='KRW')
COINS_USDT = pyupbit.get_tickers(fiat='USDT')

PRICES_BTC = get_current_prices(COINS_BTC)
PRICES_KRW = get_current_prices(COINS_KRW)
PRICES_USDT = get_current_prices(COINS_USDT)

# PRICES_BTC = pyupbit.get_current_price(COINS_BTC)
# PRICES_KRW = pyupbit.get_current_price(COINS_KRW)
# PRICES_USDT = pyupbit.get_current_price(COINS_USDT)
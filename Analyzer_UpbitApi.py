from Analyzer_Print import *

import requests


def get_market_codes(option='KRW', details='false'):
    print(f'{get_time_header()} Get All Market Code Information...')
    url = f'https://api.upbit.com/v1/market/all?isDetails={details}'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    response = sorted(response.json(), key=lambda x: x['market'])
    result = [res for res in response if res['market'].startswith(option)]
    return result


def get_market_tickers(markets):
    print(f'{get_time_header()} Get All Market Ticker Information...')
    tickers = []
    for market in markets:
        ticker = get_market_ticker(market)
        tickers.append(ticker)
    return tickers


def get_market_ticker(market):
    market_code = market['market']  # 종목 코드
    market_name_ko = market['korean_name']  # 한글 이름
    market_name_en = market['english_name']  # 영문 이름

    url = f'https://api.upbit.com/v1/ticker?markets={market_code}'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    time.sleep(0.1)

    print(f'{get_time_header()} {url}')
    trade_price = response.json()[0]['trade_price']  # 현재가
    trade_volume = response.json()[0]['acc_trade_volume']  # 누적 거래량 (UTC 00시 기준)
    change_rate = response.json()[0]['signed_change_rate']  # 전일 대비 (-% 포함)
    ticker = {
        '종목코드': market_code,
        '코인이름': market_name_ko,
        '현재가': trade_price,
        '전일대비': change_rate,
        '거래량': trade_volume
    }
    return ticker


def get_tickers():
    print(f'\n{get_time_header()} Get All Market Information...')
    market_codes = get_market_codes()
    market_tickers = get_market_tickers(market_codes)
    print(f'{get_time_header()} Sorting All Market Ticker Information...')
    return sorted(market_tickers, key=lambda x: x['전일대비'], reverse=True)
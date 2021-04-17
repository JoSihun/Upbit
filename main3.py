# [VBA] 업비트 Open API > 시세 종목 조회 > 마켓 코드 조회
# https://xlmaster.tistory.com/15
#
# [VBA] 업비트 Open API > 시세 Ticker 조회 > 현재가 정보
# https://xlmaster.tistory.com/21

# xlwings workbook 사용법
# 1) workbook = xlwings.Book()
# 2) workbook = xlwings.Book('파일명')
#
# xlwings worksheet 사용법
# 1) worksheet.range('A1').value = '문자열'
# 2) worksheet.range('A1:D4').value = 값
# 3) worksheet.range('A1').formula = '식'
# 4) worksheet.range('A1:D4').clear()

import os, time
import requests
import pyupbit, xlwings

def get_time_str():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]

    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    str_now = f'[{date}, {now} GMT{timezone}]'

    # year = time.localtime().tm_year
    # month = time.localtime().tm_mon
    # day = time.localtime().tm_mday

    return str_now

def get_tickers(option='KRW'):
    now = get_time_str()
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url)
    markets_all = response.json()
    print(f'Obtaining All Market Informations...')

    TICKERS_BTC = []
    TICKERS_KRW = []
    TICKERS_USDT = []
    print(f'{now} {url}\n')
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
    now = get_time_str()
    url = 'https://api.upbit.com/v1/ticker?markets='
    print(f'Obtaining Trade Informations...')

    PRICES = []
    for TICKER in TICKERS:
        print(f'{now} {url}' + TICKER['market'])
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

    return sorted(PRICES, key=lambda PRICE: PRICE['전일대비'], reverse=True)

def excel_edit(PRICES):
    # Excel File Load
    workbook = xlwings.Book(FILENAME)
    worksheet1 = workbook.sheets['현재가테이블']  # 현재가테이블 시트읽기
    worksheet2 = workbook.sheets['종목선정']  # 현재오늘날짜 시트읽기

    try:
        workbook.sheets[time.strftime('%Y.%m.%d')]
    except:
        worksheet3 = workbook.sheets['투자전략'].copy()
        worksheet3.name = time.strftime('%Y.%m.%d')

    # Present Price Information Update
    worksheet1.range('A2:D200').value = ''      # 데이터값 초기화
    for row, item in enumerate(PRICES):
        for col, data in enumerate(item.values()):
            worksheet1.range(row + 2, col + 1).value = data

    worksheet2.range('A2:D200').value = ''      # 데이터값 초기화
    for row, item in enumerate(PRICES):
        for col, data in enumerate(item.values()):
            worksheet2.range(row + 2, col + 1).value = data

    # # Excel File Edit
    # today = time.strftime('%Y.%m.%d', time.localtime())
    # time_now = '오전' if time.localtime().tm_hour < 12 else '오후'
    # time_now += ' ' + time.strftime('%H:%M', time.localtime())

    # # Current Time Update
    # worksheet1.range('L4').value = time_now
    # worksheet1.range('P4').value = time_now
    # worksheet1.range('H19').value = time_now
    # worksheet1.range('L19').value = time_now
    # worksheet1.range('P19').value = time_now
    #
    # # Search Selected Items and Update
    # worksheet1.range('K6:K15').value = ''       # 데이터값 초기화
    # worksheet1.range('O6:O15').value = ''       # 데이터값 초기화
    # worksheet1.range('K21:K30').value = ''      # 데이터값 초기화
    # worksheet1.range('O21:O30').value = ''      # 데이터값 초기화
    # worksheet1.range('G21:G30').value = ''      # 데이터값 초기화
    #
    # analysisMarkets = []
    # activateAppend = False
    # coin_names_temp = worksheet2.range('A1:A200').value
    # coin_names_temp = list(filter(None, coin_names_temp))
    # for data in coin_names_temp:
    #     if data == '매수금액':
    #         analysisMarkets.append(coin_names)
    #         activateAppend = False
    #
    #     if activateAppend == True:
    #         coin_names.append(data)
    #
    #     if data == '코인명':
    #         coin_names = []
    #         activateAppend = True
    # analysisMarkets = analysisMarkets[1:]
    #
    # market_num = 1
    # cols = ['K', 'O', 'K', 'O', 'G']
    # for col, market in zip(cols, analysisMarkets):
    #     for row, coin_name in enumerate(market):
    #         if market_num < 3:
    #             worksheet1.range(f'{col}{row+6}').value = coin_name
    #         else:
    #             worksheet1.range(f'{col}{row+21}').value = coin_name
    #     market_num += 1
    #
    # # Save Excel File
    # workbook.save(FILENAME)




# FILENAME = '업비트투자전략.xlsm'
FILENAME = '업비트투자전략TEST.xlsm'

if __name__ == '__main__':
    if FILENAME in os.listdir():
        TICKERS_KRW = get_tickers('KRW')
        PRICES_KRW = get_prices(TICKERS_KRW)
        excel_edit(PRICES_KRW)
    else:
        print(f'FileNotFoundError: {FILENAME}이 존재하지 않습니다!')
        print(f'프로그램을 종료합니다.')

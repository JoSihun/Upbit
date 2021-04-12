# [VBA] 업비트 Open API > 시세 종목 조회 > 마켓 코드 조회
# https://xlmaster.tistory.com/15
#
# [VBA] 업비트 Open API > 시세 Ticker 조회 > 현재가 정보
# https://xlmaster.tistory.com/15

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
import xlwings

FILENAME = '업비트투자전략1.xlsm'
# FILENAME = '업비트투자전략TEST.xlsm'


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


# Get Present Price Information
present_prices = []
for item in markets_krw:
    url = 'https://api.upbit.com/v1/ticker?markets=' + item['market']
    response = requests.get(url)
    ticker = response.json()
    time.sleep(0.1)
    print(f'[' + response.headers['Date'] + f'] {url}')

    coin_code = item['market']  # 종목코드
    coin_name = item['korean_name']  # 코인이름
    trade_price = ticker[0]['trade_price']  # 현재가
    change_rate = ticker[0]['signed_change_rate']  # 전일대비(-%포함)
    present_prices.append([coin_code, coin_name, trade_price, change_rate])


# Excel File Edit
today = time.strftime('%Y.%m.%d', time.localtime())
time_now = '오전' if time.localtime().tm_hour < 12 else '오후'
time_now += ' ' + time.strftime('%H:%M', time.localtime())
if FILENAME in os.listdir():
    # Excel File Load
    workbook = xlwings.Book(FILENAME)
    worksheet1 = workbook.sheets['현재가테이블']  # 현재가테이블 시트읽기
    worksheet2 = workbook.sheets[today]         # 현재오늘날짜 시트읽기

    # Present Price Information Update
    worksheet1.range('A1:D200').value = ''      # 데이터값 초기화
    for row, item in enumerate(present_prices):
        for col, data in enumerate(item):
            worksheet1.range(row + 1, col + 1).value = data

    # Current Time Update
    worksheet1.range('L4').value = time_now
    worksheet1.range('P4').value = time_now
    worksheet1.range('H19').value = time_now
    worksheet1.range('L19').value = time_now
    worksheet1.range('P19').value = time_now

    # Search Selected Items and Update
    worksheet1.range('K6:K15').value = ''       # 데이터값 초기화
    worksheet1.range('O6:O15').value = ''       # 데이터값 초기화
    worksheet1.range('K21:K30').value = ''      # 데이터값 초기화
    worksheet1.range('O21:O30').value = ''      # 데이터값 초기화
    worksheet1.range('G21:G30').value = ''      # 데이터값 초기화

    analysisMarkets = []
    activateAppend = False
    coin_names_temp = worksheet2.range('A1:A200').value
    coin_names_temp = list(filter(None, coin_names_temp))
    for data in coin_names_temp:
        if data == '매수금액':
            analysisMarkets.append(coin_names)
            activateAppend = False

        if activateAppend == True:
            coin_names.append(data)

        if data == '코인명':
            coin_names = []
            activateAppend = True
    analysisMarkets = analysisMarkets[1:]

    market_num = 1
    cols = ['K', 'O', 'K', 'O', 'G']
    for col, market in zip(cols, analysisMarkets):
        for row, coin_name in enumerate(market):
            if market_num < 3:
                worksheet1.range(f'{col}{row+6}').value = coin_name
            else:
                worksheet1.range(f'{col}{row+21}').value = coin_name
        market_num += 1

    # Save Excel File
    workbook.save(FILENAME)

# else:
#     workbook = xlwings.Book()
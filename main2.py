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

import os, shutil, time
import requests
import pyupbit, xlwings

def get_time_str():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]

    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    str_now = f'[{date}, {now} GMT{timezone}]'

    return str_now

def get_tickers(option='KRW'):
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url)
    markets_all = response.json()
    print(f'Obtaining All Market Informations...')

    TICKERS_BTC = []
    TICKERS_KRW = []
    TICKERS_USDT = []
    print(f'{get_time_str()} {url}\n')
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
    url = 'https://api.upbit.com/v1/ticker?markets='
    print(f'Obtaining Trade Informations...')

    PRICES = []
    for TICKER in TICKERS:
        print(f'{get_time_str()} {url}' + TICKER['market'])
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

    print(f'Sorting Trade Informations...')
    return sorted(PRICES, key=lambda PRICE: PRICE['전일대비'], reverse=True)

def excel_edit(PRICES):
    # Dataset for Excel Input
    print(f'Resorting Trade Informations for Inputting Excel...\n')
    under100 = []
    under1000 = []
    for item in PRICES:
        if item['현재가'] < 100:
            under100.append(item)
        if 100 <= item['현재가'] < 1000:
            under1000.append(item)

    # Excel File Load
    print(f'Loading WorkBook \'{FILENAME}\'...')
    workbook = xlwings.Book(FILENAME)           # Excel 파일읽기
    print(f'Loading WorkSheet \'종목선정\'...')
    worksheet1 = workbook.sheets['종목선정']     # 종목선정 시트읽기
    print(f'Loading WorkSheet \'현재가테이블\'...')
    worksheet2 = workbook.sheets['현재가테이블']  # 현재가테이블 시트읽기
    try:
        UPDATE_TODAY = False
        print(f'Loading WorkSheet \'' + time.strftime('%Y.%m.%d') + f'\'...')
        worksheet3 = workbook.sheets[time.strftime('%Y.%m.%d')]
    except:
        UPDATE_TODAY = True
        print(f'WorkSheet \'' + time.strftime('%Y.%m.%d') + f'\'Does Not Exists!')
        print(f'Creating WorkSheet \'' + time.strftime('%Y.%m.%d') + f'\'...\n')
        worksheet3 = workbook.sheets['투자전략'].copy()
        worksheet3.name = time.strftime('%Y.%m.%d')

    # Recommend Marcket Information Update
    print(f'Initialize Date Information...')
    worksheet1.range('H3').value = time.strftime('%Y.%m.%d')
    worksheet2.range('H3').value = time.strftime('%Y.%m.%d')
    worksheet3.range('G1').value = time.strftime('%Y-%m-%d')

    print(f'Initialize Data Information...\n')
    worksheet1.range('O6:O25').value = ''  # 데이터값 초기화
    worksheet1.range('G31:G50').value = ''  # 데이터값 초기화
    worksheet1.range('K31:K50').value = ''  # 데이터값 초기화
    worksheet1.range('O31:O50').value = ''  # 데이터값 초기화

    worksheet1.range('G56:G75').value = ''  # 데이터값 초기화
    worksheet1.range('K56:K75').value = ''  # 데이터값 초기화
    worksheet1.range('O56:O75').value = ''  # 데이터값 초기화

    print(f'Updating WorkSheet 종목선정...')
    worksheet1.range('A2:E200').value = ''      # 데이터값 초기화
    for row, item in enumerate(PRICES):
        for col, data in enumerate(item.values()):
            worksheet1.range(row + 2, col + 1).value = data

    # Present Price Information Update
    print(f'Updating WorkSheet 현재가테이블...')
    worksheet2.range('A2:E200').value = ''      # 데이터값 초기화
    for row, item in enumerate(PRICES):
        for col, data in enumerate(item.values()):
            worksheet2.range(row + 2, col + 1).value = data

    print(f'Updating WorkSheet ' + time.strftime('%Y.%m.%d') + f'...')
    # Total Top20
    for row, item in enumerate(PRICES[0:20]):
        worksheet1.range(f'O{6+row}').value = item['코인이름']
        worksheet1.range(f'G{31+row}').value = item['코인이름']
        if UPDATE_TODAY == True:
            worksheet3.range(f'A{98+row}').value = item['코인이름']
            worksheet3.range(f'B{98+row}').value = item['현재가']
            worksheet3.range(f'C{98+row}').value = item['전일대비']

    # YeopJeon Top20
    for row, item in enumerate(under100[0:20]):
        worksheet1.range(f'K{31+row}').value = item['코인이름']
        if UPDATE_TODAY == True:
            worksheet3.range(f'A{44+row}').value = item['코인이름']
            worksheet3.range(f'B{44+row}').value = item['현재가']
            worksheet3.range(f'C{44+row}').value = item['전일대비']

    # DongJeon Top20
    for row, item in enumerate(under1000[0:20]):
        worksheet1.range(f'O{31+row}').value = item['코인이름']
        if UPDATE_TODAY == True:
            worksheet3.range(f'A{71+row}').value = item['코인이름']
            worksheet3.range(f'B{71+row}').value = item['현재가']
            worksheet3.range(f'C{71+row}').value = item['전일대비']

    # Total Bottom20
    for row, item in enumerate(PRICES[-20:]):
        worksheet1.range(f'G{56+row}').value = item['코인이름']
        if UPDATE_TODAY == True:
            worksheet3.range(f'A{179+row}').value = item['코인이름']
            worksheet3.range(f'B{179+row}').value = item['현재가']
            worksheet3.range(f'C{179+row}').value = item['전일대비']

    # YeopJeon Bottom20
    for row, item in enumerate(under100[-20:]):
        worksheet1.range(f'K{56+row}').value = item['코인이름']
        if UPDATE_TODAY == True:
            worksheet3.range(f'A{125+row}').value = item['코인이름']
            worksheet3.range(f'B{125+row}').value = item['현재가']
            worksheet3.range(f'C{125+row}').value = item['전일대비']

    # DongJeon Bottom20
    for row, item in enumerate(under1000[-20:]):
        worksheet1.range(f'O{56+row}').value = item['코인이름']
        if UPDATE_TODAY == True:
            worksheet3.range(f'A{152+row}').value = item['코인이름']
            worksheet3.range(f'B{152+row}').value = item['현재가']
            worksheet3.range(f'C{152+row}').value = item['전일대비']

    # Save Excel File
    workbook.save(FILENAME)


MAJOR_COIN = {'비트코인':'KRW-BTC', '이더리움':'KRW-ETH', '리플':'KRW-XRP',
              '에이다':'KRW-ADA', '스텔라루멘':'KRW-XLM'}
KIMCHI_COIN = {'아이콘':'KRW-ICX', '페이코인':'KRW-PCI', '밀크':'KRW-MLK', '보라':'KRW-BORA',
               '디카르고':'KRW-DKA', '썸씽':'KRW-SSX', '알파쿼크':'KRW-AQT', '메디블록':'KRW-MED'}
CHINA_COIN = {'트론':'KRW-TRX', '네오':'KRW-NEO', '퀀텀':'KRW-QTUM', '시아':'KRW-SC',
              '비트토렌트':'KRW-BTT', '이오스':'KRW-EOS', '온톨로지':'KRW-ONT', '온톨로지가스':'KRW-ONG', '비체인':'KRW-VET'}
NFT_COIN = {'쎄타토큰':'KRW-THETA', '엔진코인':'KRW-ENJ', '플로우':'KRW-FLOW', '칠리즈':'KRW-CHZ',
            '디센트럴랜드':'KRW-MANA', '왁스':'KRW-WAXP', '샌드박스':'KRW-SAND'}
DEPHI_COIN = {'트론':'KRW-TRX', '폴카닷':'KRW-DOT', '체인링크':'KRW-LINK',
              '스와이프':'KRW-SXP', '저스트':'KRW-JST', '제로엑스':'KRW-ZRX'}

STANDARD = 'Upbit투자분석 '+time.strftime('%Y')+'년 XX월.xlsm'
FILENAME = 'Upbit투자분석 '+time.strftime('%Y')+'년 '+time.strftime('%m')+'월.xlsm'

if __name__ == '__main__':
    start = time.time()
    if not FILENAME in os.listdir():                        # 파일이 없으면
        shutil.copy(STANDARD, FILENAME)    # 양식 파일 복사

    TICKERS_KRW = get_tickers('KRW')
    PRICES_KRW = get_prices(TICKERS_KRW)

    excel_edit(PRICES_KRW)

    end = time.time()
    print(f'처리시간: {end-start:.3f}sec')
    # 처리시간이 너무 김, 최적화 필요, 적절한 print문 필요
    # 월말정산필요
    # VBA n차 현재가 초기화 MsgBox 추가필요
    # 상단 종합 평균 상승률 조건부서식 수정필요
    # 데이터 상승률 0일때 조건부서식 처리방법 필요

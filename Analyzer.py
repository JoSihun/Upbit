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
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
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

def excel_edit(PRICES):
    timeHeader = get_time_str()

    # Dataset for Excel Input
    print(f'{timeHeader} Resorting Trade Informations for Inputting Excel...\n')
    under100 = []
    under1000 = []
    for item in PRICES:
        if item['현재가'] < 100:
            under100.append(item)
        if 100 <= item['현재가'] < 1000:
            under1000.append(item)

    # Excel File Load
    print(f'{timeHeader} Loading WorkBook \'{FILENAME}\'...')
    workbook = xlwings.Book(FILENAME)           # Excel 파일읽기
    print(f'{timeHeader} Loading WorkSheet \'종목선정\'...')
    worksheet1 = workbook.sheets['종목선정']     # 종목선정 시트읽기
    print(f'{timeHeader} Loading WorkSheet \'현재가테이블\'...')
    worksheet2 = workbook.sheets['현재가테이블']  # 현재가테이블 시트읽기
    try:
        UPDATE_TODAY = False
        print(f'{timeHeader} Loading WorkSheet \'' + time.strftime('%Y.%m.%d') + f'\'...\n')
        worksheet3 = workbook.sheets[time.strftime('%Y.%m.%d')]
    except:
        UPDATE_TODAY = True
        print(f'{timeHeader} WorkSheet \'' + time.strftime('%Y.%m.%d') + f'\'Does Not Exists!')
        print(f'{timeHeader} Creating WorkSheet \'' + time.strftime('%Y.%m.%d') + f'\'...\n')
        worksheet3 = workbook.sheets['투자전략'].copy()
        worksheet3.name = time.strftime('%Y.%m.%d')

    # Date Information Update
    print(f'{timeHeader} Initialize Date Information...')
    worksheet1.range('H3').value = time.strftime('%Y.%m.%d')
    worksheet2.range('H3').value = time.strftime('%Y.%m.%d')
    worksheet3.range('G1').value = time.strftime('%Y-%m-%d')

    # Data Information Initialize
    print(f'{timeHeader} Initialize Data Information...\n')
    worksheet1.range('O6:O25').value = ''                       # 종목선정 시트, 종목추천 셀 값 초기화
    worksheet1.range('G31:G50').value = ''                      # 종목선정 시트, 전체코인 Top20 셀 값 초기화
    worksheet1.range('K31:K50').value = ''                      # 종목선정 시트, 엽전코인 Top20 셀 값 초기화
    worksheet1.range('O31:O50').value = ''                      # 종목선정 시트, 동전코인 Top20 셀 값 초기화
    worksheet1.range('G56:G75').value = ''                      # 종목선정 시트, 전체코인 Bottom20 셀 값 초기화
    worksheet1.range('K56:K75').value = ''                      # 종목선정 시트, 엽전코인 Bottom20 셀 값 초기화
    worksheet1.range('O56:O75').value = ''                      # 종목선정 시트, 동전코인 Bottom20 셀 값 초기화

    # Recommend Marcket Information Update
    print(f'{timeHeader} Updating Total Data In WorkSheet 종목선정...')
    datas = [list(data.values()) for data in PRICES]            # 종목선정 시트, 전체코인 데이터 전처리
    worksheet1.range('A2:E200').value = ''                      # 종목선정 시트, 전체코인 셀 값 초기화
    worksheet1.range('A2:E200').value = datas                   # 종목선정 시트, 전체코인 데이터 삽입

    # Present Price Information Update
    print(f'{timeHeader} Updating Total Data In  WorkSheet 현재가테이블...')
    datas = [list(data.values()) for data in PRICES]            # 현재가테이블 시트, 전체코인 데이터 전처리
    worksheet2.range('A2:E200').value = ''                      # 현재가테이블 시트, 전체코인 셀 값 초기화
    worksheet2.range('A2:E200').value = datas                   # 현재가테이블 시트, 전체코인 데이터 삽입

    # print(f'{timeHeader} Updating WorkSheet ' + time.strftime('%Y.%m.%d') + f'...')

    # Total Top20
    print(f'{timeHeader} Updating Total Coin Top20 Data In WorkSheets...')
    datas_names = [[data['코인이름']] for data in PRICES[:20]]          # 전체코인 Top20, 코인이름 데이터 전처리
    datas_price = [[data['현재가']] for data in PRICES[:20]]            # 전체코인 Top20, 현재가 데이터 전처리
    datas_percent = [[data['전일대비']] for data in PRICES[:20]]        # 전체코인 Top20, 전일대비 데이터 전처리
    worksheet1.range('O6').value = datas_names                      # 전체코인 Top20, 종목선정 시트 코인명 업데이트
    worksheet1.range('G31').value = datas_names                     # 전체코인 Top20, 종목선정 시트 코인명 업데이트
    if UPDATE_TODAY == True:                                        # 날짜변경으로 새 시트 생성 시
        worksheet3.range(f'A98').value = datas_names                # 전체코인 Top20, 새 시트 코인명 업데이트
        worksheet3.range(f'B98').value = datas_price                # 전체코인 Top20, 새 시트 현재가 업데이트
        worksheet3.range(f'C98').value = datas_percent              # 전체코인 Top20, 새 시트 전일대비 업데이트

    # YeopJeon Top20
    print(f'{timeHeader} Updating YeopJeon Coin Top20 Data In WorkSheets...')
    datas_names = [[data['코인이름']] for data in under100[:20]]        # 엽전코인 Top20, 코인이름 데이터 전처리
    datas_price = [[data['현재가']] for data in under100[:20]]         # 엽전코인 Top20, 현재가 데이터 전처리
    datas_percent = [[data['전일대비']] for data in under100[:20]]      # 엽전코인 Top20, 전일대비 데이터 전처리
    worksheet1.range(f'K31').value = datas_names                    # 엽전코인 Top20, 종목선정 시트 코인명 업데이트
    if UPDATE_TODAY == True:                                        # 날짜변경으로 새 시트 생성 시
        worksheet3.range(f'A44').value = datas_names                # 엽전코인 Top20, 새 시트 코인명 업데이트
        worksheet3.range(f'B44').value = datas_price                # 엽전코인 Top20, 새 시트 현재가 업데이트
        worksheet3.range(f'C44').value = datas_percent              # 엽전코인 Top20, 새 시트 전일대비 업데이트

    # DongJeon Top20
    print(f'{timeHeader} Updating DongJeon Coin Top20 Data In WorkSheets...')
    datas_names = [[data['코인이름']] for data in under1000[:20]]       # 동전코인 Top20, 코인이름 데이터 전처리
    datas_price = [[data['현재가']] for data in under1000[:20]]        # 동전코인 Top20, 현재가 데이터 전처리
    datas_percent = [[data['전일대비']] for data in under1000[:20]]     # 동전코인 Top20, 전일대비 데이터 전처리
    worksheet1.range(f'O31').value = datas_names                    # 동전코인 Top20, 종목선정 시트 코인명 업데이트
    if UPDATE_TODAY == True:                                        # 날짜변경으로 새 시트 생성 시
        worksheet3.range(f'A71').value = datas_names                # 동전코인 Top20, 새 시트 코인명 업데이트
        worksheet3.range(f'B71').value = datas_price                # 동전코인 Top20, 새 시트 현재가 업데이트
        worksheet3.range(f'C71').value = datas_percent              # 동전코인 Top20, 새 시트 전일대비 업데이트

    # Total Bottom20
    print(f'{timeHeader} Updating Total Coin Bottom20 Data In WorkSheets...')
    datas_names = [[data['코인이름']] for data in PRICES[-20:]]         # 전체코인 Bottom20, 코인이름 데이터 전처리
    datas_price = [[data['현재가']] for data in PRICES[-20:]]          # 전체코인 Bottom20, 현재가 데이터 전처리
    datas_percent = [[data['전일대비']] for data in PRICES[-20:]]       # 전체코인 Bottom20, 전일대비 데이터 전처리
    worksheet1.range(f'G56').value = datas_names                    # 전체코인 Bottom20, 종목선정 시트 코인명 업데이트
    if UPDATE_TODAY == True:                                        # 날짜변경으로 새 시트 생성 시
        worksheet3.range(f'A179').value = datas_names               # 전체코인 Bottom20, 새 시트 코인명 업데이트
        worksheet3.range(f'B179').value = datas_price               # 전체코인 Bottom20, 새 시트 현재가 업데이트
        worksheet3.range(f'C179').value = datas_percent             # 전체코인 Bottom20, 새 시트 전일대비 업데이트

    # YeopJeon Bottom20
    print(f'{timeHeader} Updating YeopJeon Coin Bottom20 Data In WorkSheets...')
    datas_names = [[data['코인이름']] for data in under100[-20:]]       # 엽전코인 Bottom20, 코인이름 데이터 전처리
    datas_price = [[data['현재가']] for data in under100[-20:]]        # 엽전코인 Bottom20, 현재가 데이터 전처리
    datas_percent = [[data['전일대비']] for data in under100[-20:]]     # 엽전코인 Bottom20, 전일대비 데이터 전처리
    worksheet1.range(f'K56').value = datas_names                    # 엽전코인 Bottom20, 종목선정 시트 코인명 업데이트
    if UPDATE_TODAY == True:                                        # 날짜변경으로 새 시트 생성 시
        worksheet3.range(f'A125').value = datas_names               # 엽전코인 Bottom20, 새 시트 코인명 업데이트
        worksheet3.range(f'B125').value = datas_price               # 엽전코인 Bottom20, 새 시트 현재가 업데이트
        worksheet3.range(f'C125').value = datas_percent             # 엽전코인 Bottom20, 새 시트 전일대비 업데이트

    # DongJeon Bottom20
    print(f'{timeHeader} Updating DongJeon Coin Bottom20 Data In WorkSheets...')
    datas_names = [[data['코인이름']] for data in under1000[-20:]]      # 동전코인 Bottom20, 코인이름 데이터 전처리
    datas_price = [[data['현재가']] for data in under1000[-20:]]       # 동전코인 Bottom20, 현재가 데이터 전처리
    datas_percent = [[data['전일대비']] for data in under1000[-20:]]    # 동전코인 Bottom20, 전일대비 데이터 전처리
    worksheet1.range(f'O56').value = datas_names                    # 동전코인 Bottom20, 종목선정 시트 코인명 업데이트
    if UPDATE_TODAY == True:                                        # 날짜변경으로 새 시트 생성 시
        worksheet3.range(f'A152').value = datas_names               # 동전코인 Bottom20, 새 시트 코인명 업데이트
        worksheet3.range(f'B152').value = datas_price               # 동전코인 Bottom20, 새 시트 현재가 업데이트
        worksheet3.range(f'C152').value = datas_percent             # 동전코인 Bottom20, 새 시트 전일대비 업데이트

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
    if not FILENAME in os.listdir():                # 이번 달에 해당하는 파일이 없으면
        shutil.copy(STANDARD, FILENAME)             # 양식 파일 복사, 파일 이름 변경
        workbook = xlwings.Book(FILENAME)                                           # Excel 파일읽기
        workbook.sheets['투자전략'].range('G1').value = time.strftime('%Y-%m-%d')    # 날짜변경

    TICKERS_KRW = get_tickers('KRW')
    PRICES_KRW = get_prices(TICKERS_KRW)

    excel_edit(PRICES_KRW)

    end = time.time()
    print(f'Analyze Complete! 처리시간: {end-start:.3f}sec')

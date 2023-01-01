import os
import shutil
import time

import xlwings

from Analyzer_Print import *

DATA_PATH = f'./data/'
FORM_NAME = f'Upbit투자분석 20XX년 XX월.xlsm'
FILE_NAME = f'Upbit투자분석 yyyy년 mm월.xlsm'

STRATEGY_SHEET = '투자전략'
SELECTION_SHEET = '종목선정'
CUR_PRICE_SHEET = '현재가테이블'


def get_form_path():
    return DATA_PATH + FORM_NAME


def get_data_path():
    if time.strftime('%Y') not in os.listdir(DATA_PATH):
        print(f'''{get_time_header()} Not Exists Data Path '{DATA_PATH + time.strftime('%Y')}'...''')
        print(f'''{get_time_header()} Create New Data Path '{DATA_PATH + time.strftime('%Y')}'...''')
        os.mkdir(DATA_PATH + time.strftime('%Y'))
    return DATA_PATH + time.strftime('%Y/')


def get_file_name():
    year = time.strftime('%Y')
    month = time.strftime('%m')
    return f'Upbit투자분석 {year}년 {month}월.xlsm'


def get_file_path():
    data_path = get_data_path()
    file_name = get_file_name()
    return data_path + file_name


###################################################################################################



###################################################################################################


def create_workbook():
    form_path = get_form_path()
    file_path = get_file_path()
    shutil.copy(form_path, file_path)  # 양식 파일 복사, 파일 이름 변경


def init_worksheet(file_path):
    workbook = xlwings.Book(file_path)  # Excel 파일 읽기
    worksheet = workbook.sheets[STRATEGY_SHEET]  # Excel 시트 읽기
    worksheet.range('G1').value = time.strftime('%Y-%m-%d')  # 날짜 변경


# 여기에 전월 데이터 삽입 조건 추가해야 할 듯
def load_workbook():
    file_name = get_file_name()
    file_path = get_file_path()
    data_path = get_data_path()

    print(f'''{get_time_header()} Load WorkBook '{file_name}'...''')
    if file_name not in os.listdir(data_path):
        print(f'''{get_time_header()} Not Exists WorkBook Name '{file_name}'...''')
        print(f'''{get_time_header()} Create New WorkBook Name '{file_name}'...''')
        create_workbook()
        init_worksheet(file_path)
    return xlwings.Book(file_path)  # Excel 파일 읽기


###################################################################################################


def preprocess_tickers_split_under(tickers):
    print(f'{get_time_header()} Preprocess Total Coin Under100 Data...')
    print(f'{get_time_header()} Preprocess Total Coin Under1000 Data...')
    under100, under1000 = list(), list()
    for ticker in tickers:
        if ticker['현재가'] < 100:
            under100.append(ticker)
        elif ticker['현재가'] < 1000:
            under1000.append(ticker)
    return under100, under1000


def preprocess_tickers_total_top20(tickers):
    print(f'{get_time_header()} Preprocess Total Coin Top20 Data...')
    total_top20_names = [[ticker['코인이름']] for ticker in tickers[:20]]  # 전체코인 Top20, 코인이름 데이터 전처리
    total_top20_price = [[ticker['현재가']] for ticker in tickers[:20]]  # 전체코인 Top20, 현재가 데이터 전처리
    total_top20_rates = [[ticker['전일대비']] for ticker in tickers[:20]]  # 전체코인 Top20, 전일대비 데이터 전처리
    return total_top20_names, total_top20_price, total_top20_rates


def preprocess_tickers_yeopjeon_top20(under100):
    print(f'{get_time_header()} Preprocess YeopJeon Coin Top20 Data...')
    yeopjeon_top20_names = [[ticker['코인이름']] for ticker in under100[:20]]  # 엽전코인 Top20, 코인이름 데이터 전처리
    yeopjeon_top20_price = [[ticker['현재가']] for ticker in under100[:20]]  # 엽전코인 Top20, 현재가 데이터 전처리
    yeopjeon_top20_rates = [[ticker['전일대비']] for ticker in under100[:20]]  # 엽전코인 Top20, 전일대비 데이터 전처리
    return yeopjeon_top20_names, yeopjeon_top20_price, yeopjeon_top20_rates


def preprocess_tickers_dongjeon_top20(under1000):
    print(f'{get_time_header()} Preprocess DongJeon Coin Top20 Data...')
    dongjeon_top20_names = [[ticker['코인이름']] for ticker in under1000[:20]]  # 동전코인 Top20, 코인이름 데이터 전처리
    dongjeon_top20_price = [[ticker['현재가']] for ticker in under1000[:20]]  # 동전코인 Top20, 현재가 데이터 전처리
    dongjeon_top20_rates = [[ticker['전일대비']] for ticker in under1000[:20]]  # 동전코인 Top20, 전일대비 데이터 전처리
    return dongjeon_top20_names, dongjeon_top20_price, dongjeon_top20_rates


def preprocess_tickers_total_bottom20(tickers):
    print(f'{get_time_header()} Preprocess Total Coin Bottom20 Data...')
    total_bottom20_names = [[ticker['코인이름']] for ticker in tickers[-20:]]  # 전체코인 Bottom20, 코인이름 데이터 전처리
    total_bottom20_price = [[ticker['현재가']] for ticker in tickers[-20:]]  # 전체코인 Bottom20, 현재가 데이터 전처리
    total_bottom20_rates = [[ticker['전일대비']] for ticker in tickers[-20:]]  # 전체코인 Bottom20, 전일대비 데이터 전처리
    return total_bottom20_names, total_bottom20_price, total_bottom20_rates


def preprocess_tickers_yeopjeon_bottom20(under100):
    print(f'{get_time_header()} Preprocess YeopJeon Coin Bottom20 Data...')
    yeopjeon_bottom20_names = [[ticker['코인이름']] for ticker in under100[-20:]]  # 엽전코인 Bottom20, 코인이름 데이터 전처리
    yeopjeon_bottom20_price = [[ticker['현재가']] for ticker in under100[-20:]]  # 엽전코인 Bottom20, 현재가 데이터 전처리
    yeopjeon_bottom20_rates = [[ticker['전일대비']] for ticker in under100[-20:]]  # 엽전코인 Bottom20, 전일대비 데이터 전처리
    return yeopjeon_bottom20_names, yeopjeon_bottom20_price, yeopjeon_bottom20_rates


def preprocess_tickers_dongjeon_bottom20(under1000):
    print(f'{get_time_header()} Preprocess DongJeon Coin Bottom20 Data...')
    dongjeon_bottom20_names = [[ticker['코인이름']] for ticker in under1000[-20:]]  # 동전코인 Bottom20, 코인이름 데이터 전처리
    dongjeon_bottom20_price = [[ticker['현재가']] for ticker in under1000[-20:]]  # 동전코인 Bottom20, 현재가 데이터 전처리
    dongjeon_bottom20_rates = [[ticker['전일대비']] for ticker in under1000[-20:]]  # 동전코인 Bottom20, 전일대비 데이터 전처리
    return dongjeon_bottom20_names, dongjeon_bottom20_price, dongjeon_bottom20_rates


def update_workbook(workbook, tickers):
    # Data Preprocessing Tickers Under
    print(f'\n{get_time_header()} Preprocess Total Coin Data Splitting...')
    under100, under1000 = preprocess_tickers_split_under(tickers)

    # Data Preprocessing Tickers Top20
    print(f'\n{get_time_header()} Preprocess Top20 Data...')
    total_top20_data = preprocess_tickers_total_top20(tickers)  # 전체코인 Top20, 데이터 전처리
    yeopjeon_top20_data = preprocess_tickers_yeopjeon_top20(under100)  # 엽전코인 Top20, 데이터 전처리
    dongjeon_top20_data = preprocess_tickers_dongjeon_top20(under1000)  # 동전코인 Top20, 데이터 전처리

    # Data Preprocessing Tickers Bottom20
    print(f'\n{get_time_header()} Preprocess Bottom20 Data...')
    total_bottom20_data = preprocess_tickers_total_bottom20(tickers)  # 전체코인 Bottom20, 데이터 전처리
    yeopjeon_bottom20_data = preprocess_tickers_yeopjeon_bottom20(under100)  # 엽전코인 Bottom20, 데이터 전처리
    dongjeon_bottom20_data = preprocess_tickers_dongjeon_bottom20(under1000)  # 동전코인 Bottom20, 데이터 전처리

    # Data Preprocessing Tickers Unpack
    print(f'\n{get_time_header()} Preprocess Total Coin Data Unpacking...\n')
    total_top20_names, total_top20_price, total_top20_rates = total_top20_data  # unpack
    yeopjeon_top20_names, yeopjeon_top20_price, yeopjeon_top20_rates = yeopjeon_top20_data  # unpack
    dongjeon_top20_names, dongjeon_top20_price, dongjeon_top20_rates = dongjeon_top20_data  # unpack
    total_bottom20_names, total_bottom20_price, total_bottom20_rates = total_bottom20_data  # unpack
    yeopjeon_bottom20_names, yeopjeon_bottom20_price, yeopjeon_bottom20_rates = yeopjeon_bottom20_data  # unpack
    dongjeon_bottom20_names, dongjeon_bottom20_price, dongjeon_bottom20_rates = dongjeon_bottom20_data  # unpack

    # Read WorkSheets 종목선정 & 현재가테이블
    print(f'{get_time_header()} Read WorkSheet Name \'종목선정\'...')
    print(f'{get_time_header()} Read WorkSheet Name \'현재가테이블\'...')
    worksheet1 = workbook.sheets['종목선정']
    worksheet2 = workbook.sheets['현재가테이블']

    # Initialize WorkSheet 1 & 2
    markets = [list(ticker.values()) for ticker in tickers]  # 전체코인 데이터 전처리
    print(f'''\n{get_time_header()} Update All Tickers In WorkSheet '종목선정'...''')
    worksheet1.range('A2:E200').value = ''  # 종목선정 시트, 전체코인 셀 값 초기화
    worksheet1.range('A2:E200').value = markets  # 종목선정 시트, 전체코인 데이터 삽입
    print(f'''{get_time_header()} Update All Tickers In WorkSheet '현재가테이블'...''')
    worksheet2.range('A2:E200').value = ''  # 현재가테이블 시트, 전체코인 셀 값 초기화
    worksheet2.range('A2:E200').value = markets  # 현재가테이블 시트, 전체코인 데이터 삽입

    # Initialize All Recommended Coin Names In WorkSheet 종목선정
    print(f'''\n{get_time_header()} Initialize All Recommended Coin Names In WorkSheet '종목선정'...''')
    worksheet1.range('O6:O25').value = ''  # 종목선정 시트, 종목추천 셀 값 초기화
    worksheet1.range('G31:G50').value = ''  # 종목선정 시트, 전체코인 Top20 셀 값 초기화
    worksheet1.range('K31:K50').value = ''  # 종목선정 시트, 엽전코인 Top20 셀 값 초기화
    worksheet1.range('O31:O50').value = ''  # 종목선정 시트, 동전코인 Top20 셀 값 초기화
    worksheet1.range('G56:G75').value = ''  # 종목선정 시트, 전체코인 Bottom20 셀 값 초기화
    worksheet1.range('K56:K75').value = ''  # 종목선정 시트, 엽전코인 Bottom20 셀 값 초기화
    worksheet1.range('O56:O75').value = ''  # 종목선정 시트, 동전코인 Bottom20 셀 값 초기화

    # Update All Recommended Coin Names In WorkSheet 종목선정
    print(f'''{get_time_header()} Update All Recommended Coin Names In WorkSheet '종목선정'...''')
    worksheet1.range('O6').value = total_top20_names  # 전체코인 Top20, 종목선정 시트 코인명 업데이트
    worksheet1.range('G31').value = total_top20_names  # 전체코인 Top20, 종목선정 시트 코인명 업데이트
    worksheet1.range(f'K31').value = yeopjeon_top20_names  # 엽전코인 Top20, 종목선정 시트 코인명 업데이트
    worksheet1.range(f'O31').value = dongjeon_top20_names  # 동전코인 Top20, 종목선정 시트 코인명 업데이트
    worksheet1.range(f'G56').value = total_bottom20_names  # 전체코인 Bottom20, 종목선정 시트 코인명 업데이트
    worksheet1.range(f'K56').value = yeopjeon_bottom20_names  # 엽전코인 Bottom20, 종목선정 시트 코인명 업데이트
    worksheet1.range(f'O56').value = dongjeon_bottom20_names  # 동전코인 Bottom20, 종목선정 시트 코인명 업데이트

    # Validate WorkSheet Today
    print(f'''\n{get_time_header()} Validate WorkSheet Name '{time.strftime('%Y.%m.%d')}'...''')
    worksheets = [worksheet.name for worksheet in workbook.sheets]
    if time.strftime('%Y.%m.%d') not in worksheets:
        print(f'''{get_time_header()} Not Exists WorkSheet Name '{time.strftime('%Y.%m.%d')}'!''')
        print(f'''{get_time_header()} Create New WorkSheet Name '{time.strftime('%Y.%m.%d')}'...''')
        worksheet3 = workbook.sheets['투자전략'].copy()
        worksheet3.name = time.strftime('%Y.%m.%d')

        print(f'''\n{get_time_header()} Initialize All Recommended Coin Data In WorkSheet {time.strftime('%Y.%m.%d')}...''')
        worksheet3.range(f'A98').value = total_top20_names  # 전체코인 Top20, 새 시트 코인명 업데이트
        worksheet3.range(f'B98').value = total_top20_price  # 전체코인 Top20, 새 시트 현재가 업데이트
        worksheet3.range(f'C98').value = total_top20_rates  # 전체코인 Top20, 새 시트 전일대비 업데이트
        worksheet3.range(f'A44').value = yeopjeon_top20_names  # 엽전코인 Top20, 새 시트 코인명 업데이트
        worksheet3.range(f'B44').value = yeopjeon_top20_price  # 엽전코인 Top20, 새 시트 현재가 업데이트
        worksheet3.range(f'C44').value = yeopjeon_top20_rates  # 엽전코인 Top20, 새 시트 전일대비 업데이트
        worksheet3.range(f'A71').value = dongjeon_top20_names  # 동전코인 Top20, 새 시트 코인명 업데이트
        worksheet3.range(f'B71').value = dongjeon_top20_price  # 동전코인 Top20, 새 시트 현재가 업데이트
        worksheet3.range(f'C71').value = dongjeon_top20_rates  # 동전코인 Top20, 새 시트 전일대비 업데이트
        worksheet3.range(f'A179').value = total_bottom20_names  # 전체코인 Bottom20, 새 시트 코인명 업데이트
        worksheet3.range(f'B179').value = total_bottom20_price  # 전체코인 Bottom20, 새 시트 현재가 업데이트
        worksheet3.range(f'C179').value = total_bottom20_rates  # 전체코인 Bottom20, 새 시트 전일대비 업데이트
        worksheet3.range(f'A125').value = yeopjeon_bottom20_names  # 엽전코인 Bottom20, 새 시트 코인명 업데이트
        worksheet3.range(f'B125').value = yeopjeon_bottom20_price  # 엽전코인 Bottom20, 새 시트 현재가 업데이트
        worksheet3.range(f'C125').value = yeopjeon_bottom20_rates  # 엽전코인 Bottom20, 새 시트 전일대비 업데이트
        worksheet3.range(f'A152').value = dongjeon_bottom20_names  # 동전코인 Bottom20, 새 시트 코인명 업데이트
        worksheet3.range(f'B152').value = dongjeon_bottom20_price  # 동전코인 Bottom20, 새 시트 현재가 업데이트
        worksheet3.range(f'C152').value = dongjeon_bottom20_rates  # 동전코인 Bottom20, 새 시트 전일대비 업데이트

        print(f'''{get_time_header()} Initialize Date Information In WorkSheet '종목선정'...''')
        print(f'''{get_time_header()} Initialize Date Information In WorkSheet '현재가테이블'...''')
        print(f'''{get_time_header()} Initialize Date Information In WorkSheet '{time.strftime('%Y.%m.%d')}'...''')
        worksheet1.range('H3').value = time.strftime('%Y.%m.%d')
        worksheet2.range('H3').value = time.strftime('%Y.%m.%d')
        worksheet3.range('G1').value = time.strftime('%Y-%m-%d')

    # Save Excel File
    print(f'{get_time_header()} Save WorkBook in {get_file_path()}...')
    workbook.save(get_file_path())

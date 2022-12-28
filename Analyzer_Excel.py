import os, shutil, time
import datetime, schedule
import xlwings

DATA_PATH = f'./data/'
FORM_NAME = f'Upbit투자분석 20XX년 XX월.xlsm'
FILE_NAME = f'Upbit투자분석 yyyy년 mm월.xlsm'

STRATEGY_SHEET = '투자전략'


def get_form_path():
    return DATA_PATH + FORM_NAME


def get_excel_path():
    return DATA_PATH + time.strftime('%Y/')


def get_file_name():
    year = time.strftime('%Y')
    month = time.strftime('%m')
    return f'Upbit투자분석 {year}년 {month}월.xlsm'


def get_file_path():
    filename = get_file_name()
    excel_path = get_excel_path()
    return excel_path + filename


def create_new_file():
    form_path = get_form_path()
    file_path = get_file_path()
    shutil.copy(form_path, file_path)  # 양식 파일 복사, 파일 이름 변경
    change_date_strategy_sheet(file_path)


def change_date_strategy_sheet(filename):
    workbook = xlwings.Book(filename)  # Excel 파일 읽기
    worksheet = workbook.sheets[STRATEGY_SHEET]  # Excel 시트 읽기
    worksheet.range('G1').value = time.strftime('%Y-%m-%d')  # 날짜 변경


def open_excel_file():
    file_name = get_file_name()
    file_path = get_file_path()
    excel_path = get_excel_path()
    if file_name not in os.listdir(excel_path):
        create_new_file()
    return xlwings.Book(file_path)  # Excel 파일 읽기

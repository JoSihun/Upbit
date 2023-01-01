from Analyzer_Excel import *
from Analyzer_Macro import *
from Analyzer_Print import *
from Analyzer_UpbitApi import *

import os, shutil, time
import datetime, schedule
import requests, pyupbit, xlwings


DATA_PATH = f'./data/'
FORM_NAME = f'Upbit투자분석 20XX년 XX월.xlsm'
FILE_NAME = f'Upbit투자분석 yyyy년 mm월.xlsm'


def init_routine():
    return get_tickers()


def main_routine(tickers):
    workbook = load_workbook()
    update_workbook(workbook, tickers)


def exit_routine():
    macro_window_activate(get_file_name())
    macro_click_paste_btn()


def run():
    start = time.time()
    tickers = init_routine()
    main_routine(tickers)
    exit_routine()
    end = time.time()
    print(f'\n{get_time_header()} Analyze Complete! 처리시간: {end-start:.3f}sec')


if __name__ == '__main__':
    # run()
    scheduller(run)
from Analyzer_Excel import *
from Analyzer_Macro import *
from Analyzer_Print import *
from Analyzer_UpbitApi import *

import os, shutil, time
import datetime, schedule
import requests, pyupbit, xlwings

import pyautogui
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

DATA_PATH = f'./data/'
FORM_NAME = f'Upbit투자분석 20XX년 XX월.xlsm'
FILE_NAME = f'Upbit투자분석 yyyy년 mm월.xlsm'


def init_routine():
    workbook = load_workbook()
    switch_window_activate(get_file_name())
    return workbook


def main_routine(workbook):
    tickers = get_tickers()
    update_workbook(workbook, tickers)


def exit_routine():
    pass


def run():
    start = time.time()
    workbook = init_routine()
    main_routine(workbook)
    exit_routine()
    end = time.time()
    print(f'\n{get_time_header()} Analyze Complete! 처리시간: {end-start:.3f}sec')


if __name__ == '__main__':
    # run()
    schedule.every().day.at("14:00").do(run)
    schedule.every().day.at("19:00").do(run)
    schedule.every().day.at("21:00").do(run)
    schedule.every().day.at("00:00").do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
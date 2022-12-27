import os, shutil, time
import datetime, schedule
import requests, pyupbit, xlwings

from Analyzer_Macro import *

import pyautogui
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def is_exist(filename, filepath):
    if filename in os.listdir(filepath):
        return True
    return False


def update_filename():
    year = time.strftime('%Y')
    month = time.strftime('%m')
    return f'Upbit투자분석 {year}년 {month}월.xlsm'


def create_new_file():
    shutil.copy(STANDARD, FILENAME)  # 양식 파일 복사, 파일 이름 변경
    workbook = xlwings.Book(FILENAME)  # Excel 파일읽기
    workbook.sheets['투자전략'].range('G1').value = time.strftime('%Y-%m-%d')  # 날짜변경


def paste_btn_click():
    switch_window_activate(FILENAME)
    if datetime.datetime.now().hour == 14:
        macro_mouse_click_by_image(BTN_PASTE_PATH1)
    elif datetime.datetime.now().hour == 19:
        macro_mouse_click_by_image(BTN_PASTE_PATH2)
    elif datetime.datetime.now().hour == 21:
        macro_mouse_click_by_image(BTN_PASTE_PATH3)
    elif datetime.datetime.now().hour == 0:
        pyautogui.hotkey('ctrl', 'pageup')
        macro_mouse_click_by_image(BTN_PASTE_PATH4)
        pyautogui.hotkey('ctrl', 'pagedown')


DATA_PATH = f'./data/'
EXCEL_PATH = DATA_PATH + time.strftime('%Y/')
STANDARD = EXCEL_PATH + 'Upbit투자분석 20XX년 XX월.xlsm'
FILENAME = update_filename()


def run():
    pass

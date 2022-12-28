from Analyzer_Excel import *
from Analyzer_Macro import *
from Analyzer_Print import *

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
    print_open_excel_message()
    workbook = open_excel_file()
    switch_window_activate(get_file_name())
    return workbook


def main_routine(workbook):
    pass


def exit_routine():
    pass


def run():
    workbook = init_routine()
    main_routine(workbook)
    exit_routine()


if __name__ == '__main__':
    run()
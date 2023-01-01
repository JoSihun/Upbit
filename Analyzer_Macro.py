from Analyzer_Print import *

import time
import datetime
import schedule

import pyautogui
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

IMG_SRC_PATH = './data/images/'
BTN_PASTE_PATH1 = IMG_SRC_PATH + 'button_paste1.png'
BTN_PASTE_PATH2 = IMG_SRC_PATH + 'button_paste2.png'
BTN_PASTE_PATH3 = IMG_SRC_PATH + 'button_paste3.png'
BTN_PASTE_PATH4 = IMG_SRC_PATH + 'button_paste4.png'


def macro_window_activate(file_name):
    win = pyautogui.getWindowsWithTitle(file_name)[0]
    if not win.isActive:
        win.activate()
    if not win.isMaximized:
        win.maximize()


def macro_click_by_image(img):
    btn_location = pyautogui.locateOnScreen(img)
    btn_position = pyautogui.center(btn_location)
    pyautogui.moveTo(btn_position)
    pyautogui.click()
    pyautogui.hotkey('enter')


def macro_click_curr_page(img):
    macro_click_by_image(img)


def macro_click_prev_page(img):
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'pageup')
    time.sleep(1)
    macro_click_by_image(img)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'pagedown')


def macro_click_paste_btn():
    if datetime.datetime.now().hour == 14:
        macro_click_curr_page(BTN_PASTE_PATH1)
    elif datetime.datetime.now().hour == 19:
        macro_click_curr_page(BTN_PASTE_PATH2)
    elif datetime.datetime.now().hour == 21:
        macro_click_curr_page(BTN_PASTE_PATH3)
    elif datetime.datetime.now().hour == 0:
        macro_click_prev_page(BTN_PASTE_PATH4)


def scheduller(run):
    print_waiting_schedule()
    schedule.every().hour.do(print_waiting_schedule)
    schedule.every().day.at("14:00").do(run)
    schedule.every().day.at("19:00").do(run)
    schedule.every().day.at("21:00").do(run)
    schedule.every().day.at("00:00").do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
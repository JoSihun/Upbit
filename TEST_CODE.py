import datetime
import pyautogui
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

SRC_PATH = './data/images'
BTN_PASTE_PATH1 = SRC_PATH + '/button_paste1.png'
BTN_PASTE_PATH2 = SRC_PATH + '/button_paste2.png'
BTN_PASTE_PATH3 = SRC_PATH + '/button_paste3.png'
BTN_PASTE_PATH4 = SRC_PATH + '/button_paste4.png'

win = pyautogui.getWindowsWithTitle('Upbit투자분석')[0]
if not win.isMaximized:
    win.maximize()
if not win.isActive:
    win.activate()

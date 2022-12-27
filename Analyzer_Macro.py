import pyautogui, datetime
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

IMG_SRC_PATH = './data/images/'
BTN_PASTE_PATH1 = IMG_SRC_PATH + 'button_paste1.png'
BTN_PASTE_PATH2 = IMG_SRC_PATH + 'button_paste2.png'
BTN_PASTE_PATH3 = IMG_SRC_PATH + 'button_paste3.png'
BTN_PASTE_PATH4 = IMG_SRC_PATH + 'button_paste4.png'


def switch_window_activate(filename):
    win = pyautogui.getWindowsWithTitle(filename)[0]
    if not win.isActive:
        win.activate()
    if not win.isMaximized:
        win.maximize()


def macro_mouse_click_by_image(img):
    btn_location = pyautogui.locateOnScreen(img)
    btn_position = pyautogui.center(btn_location)
    pyautogui.moveTo(btn_position)
    pyautogui.click()
    pyautogui.hotkey('enter')


def macro_paste_btn_click():
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
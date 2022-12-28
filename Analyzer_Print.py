from Analyzer_Excel import *

import time


def get_time_header():
    date_info = time.strftime("%a, %b %d %Y")
    time_info = time.strftime('%H:%M:%S')
    time_zone = time.strftime('GMT%z')
    return f'[{date_info}, {time_info} {time_zone}]'


def print_open_excel_message():
    time_header = get_time_header()
    main_message = 'Opening Excel File in'
    file_path = get_file_path()
    print(f'{time_header} {main_message} {file_path}')
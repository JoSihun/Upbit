from Analyzer_Excel import *

import time


def get_time_header():
    date_info = time.strftime("%a, %b %d %Y")
    time_info = time.strftime('%H:%M:%S')
    time_zone = time.strftime('GMT%z')
    return f'[{date_info}, {time_info} {time_zone}]'


def print_obtain_all_market_message():
    time_header = get_time_header()
    main_message = 'Obtaining All Market Information...'
    print(f'{time_header} {main_message}')


def print_get_all_market_ticker_message():
    time_header = get_time_header()
    main_message = 'Obtaining All Market Ticker Information...'
    print(f'{time_header} {main_message}')


def print_get_market_ticker_message(url):
    time_header = get_time_header()
    print(f'{time_header} {url}')


def print_sort_all_market_ticker_message():
    time_header = get_time_header()
    main_message = 'Sorting All Market Ticker Information...'
    print(f'{time_header} {main_message}')


def print_resort_dataset_for_excel_input_message():
    time_header = get_time_header()
    main_message = 'Resorting Trade Informations for Inputting Excel...\n'
    print(f'{time_header} {main_message}')
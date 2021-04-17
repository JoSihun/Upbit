import time
import xlwings


FILENAME = '업비트투자전략TEST.xlsm'
if __name__ == '__main__':
    workbook = xlwings.Book(FILENAME)
    worksheet1 = workbook.sheets['현재가테이블']  # 현재가테이블 시트읽기
    worksheet2 = workbook.sheets['종목선정']  # 현재오늘날짜 시트읽기


    worksheet3 = workbook.sheets['투자전략'].copy()
    worksheet3.name = time.strftime('%Y.%m.%d')

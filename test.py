import time
import xlwings

# year = time.localtime().tm_year
# month = time.localtime().tm_mon
# day = time.localtime().tm_mday

FILENAME = '업비트투자전략TEST.xlsm'
if __name__ == '__main__':
    dictA = {'a':1, 'b':2, 'c':3}
    values = list(dictA.values())
    print(values)
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
index = ['BUY', 'HOLD', 'SELL']
columns = ['NAME_KOR', 'CODE', 'PRICE_BUY', 'RATE_YESTERDAY', 'MAX_PRICE', 'PRICE_NOW', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_ENG']
df = pd.DataFrame(values, index, columns)
print(df)
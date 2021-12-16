import os, shutil, time
import pandas as pd
import pyupbit, fbprophet

# 현재시간 String
def get_time_str():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month = months[time.localtime().tm_mon - 1]

    date = time.strftime(f'%a, %d {month} %Y')
    now = time.strftime('%H:%M:%S')
    timezone = time.strftime('%z')
    return f'[{date}, {now} GMT{timezone}]'



if __name__ == '__main__':
    # Pandas 출력옵션
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.options.display.float_format = '{:.4f}'.format

    # 특정시장 암호화폐 목록
    df_CODE_BTC = pd.DataFrame(pyupbit.get_tickers(fiat='BTC'), columns=['MARKET_CODE'])      # 비트시장
    df_CODE_KRW = pd.DataFrame(pyupbit.get_tickers(fiat='KRW'), columns=['MARKET_CODE'])      # 한국시장
    df_CODE_USDT = pd.DataFrame(pyupbit.get_tickers(fiat='USDT'), columns=['MARKET_CODE'])    # 미국시장

    list_CODE_BTC = pyupbit.get_tickers(fiat='BTC')
    list_CODE_KRW = pyupbit.get_tickers(fiat='KRW')
    list_CODE_USDT = pyupbit.get_tickers(fiat='USDT')


    # DataFrame 생성
    columns = ['MARKET_CODE', 'NAME_ENG', 'PRICE_NOW', 'RATE', 'MAX_PRICE',
               'BUY_PRICE', 'MIN_PRICE', 'PROFIT', 'VOLUME', 'NAME_KOR']
    df_TRADING = pd.DataFrame(columns=columns)
    df_TRADING = pd.concat([df_TRADING, df_CODE_KRW], axis=0, ignore_index=True)
    print(df_TRADING)


    # Pandas DataFrame Index 재정렬, 1부터 시작작
    df_CODE_BTC.index = df_CODE_BTC.index + 1
    df_CODE_KRW.index = df_CODE_KRW.index + 1
    df_CODE_USDT.index = df_CODE_USDT.index + 1

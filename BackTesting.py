import pyupbit
import numpy as np

# OHLCV(Open, High, Low, Close, Volume): 시가, 고가, 저가, 종가, 거래량
df = pyupbit.get_ohlcv("KRW-BTC", count=7)                      # 7일간의 원화시장 BTC정보
df['range'] = (df['high'] - df['low']) * 0.5
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.05
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")
import time
import pyupbit
import datetime
import schedule
from fbprophet import Prophet

# OHLCV(OPEN, HIGH, LOW, CLOSE, VOLUME: 시가, 고가, 저가, 종가, 거래량)

def get_target_price(ticker, k):
    ''' 변동성 돌파 전략으로 매수 목표가 조회 '''
    ''' 최근 2일간의 데이터'''
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

predicted_close_price = 0
def predict_price(ticker):
    """Prophet으로 당일 종가 가격 예측"""
    global predicted_close_price
    df = pyupbit.get_ohlcv(ticker, interval="minute60") # 시간봉기준, 최근 200시간의 데이터
    df = df.reset_index()
    df['ds'] = df['index']                              # 시간
    df['y'] = df['close']                               # 종가
    data = df[['ds','y']]                               # [INDEX, 시간, 종가] COLUMN을 갖는 데이터프레임

    model = Prophet()                                           # MODEL LOAD
    model.fit(data)                                             # DATA LEARNING
    future = model.make_future_dataframe(periods=24, freq='H')  # 24HOURS FOR FUTURE
    forecast = model.predict(future)                            # PREDICT FUTURE

    fig1 = model.plot(forecast)             # 최근 200시간 가격변화 및 예측가격
    fig2 = model.plot_components(forecast)  # TREND, DAILY 그래프 = 추세와 하루동안의 평균 가격흐름

    # 현재시간이 자정 이전인 경우의 종가
    closeDf = forecast[forecast['ds'] == forecast.iloc[-1]['ds'].replace(hour=9)]

    # 현재시간이 자정 이후인 경우의 종가
    if len(closeDf) == 0:
        closeDf = forecast[forecast['ds'] == data.iloc[-1]['ds'].replace(hour=9)]
    closeValue = closeDf['yhat'].values[0]  # 당일 종가 예측 yhat = 예측가
    predicted_close_price = closeValue

predict_price("KRW-BTC")
schedule.every().hour.do(lambda: predict_price("KRW-BTC"))

# 로그인
access_key = 'MLamU33sStiOwNGAlkxT3HYQVZfCJyaxIWakLiIm'
secret_key = 'PSrJSoS0xeQE3QlJ45pBxSSwVyZxXXRGafiBr6ZM'
upbit = pyupbit.Upbit(access_key, secret_key)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)
        schedule.run_pending()

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.5)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price and current_price < predicted_close_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
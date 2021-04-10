import time

# Excel File Edit
today = time.strftime('%Y.%m.%d', time.localtime())
time_now = '오전' if time.localtime().tm_hour < 12 else '오후'
time_now += ' ' + time.strftime('%H:%M', time.localtime())
print(time_now)
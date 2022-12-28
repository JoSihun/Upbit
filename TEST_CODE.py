import time


def get_time_header():
    date_info = time.strftime("%a, %b %d %Y")
    time_info = time.strftime('%H:%M:%S')
    time_zone = time.strftime('GMT%z')
    return f'[{date_info}, {time_info} {time_zone}]'
import datetime
from django.utils import timezone
import requests


def is_workday():
    today = timezone.localdate()
    todaystr = "{}{}{}".format(today.year, today.month, today.day)
    r = requests.get('http://api.goseek.cn/Tools/holiday', params={'data': todaystr})
    result = r.json()['data']
    # 正常工作日对应结果为 0, 法定节假日对应结果为 1, 节假日调休补班对应的结果为 2，休息日对应结果为 3
    if result in (0, 2):
        return True
    else:
        return False


def is_ordertime():
    now = timezone.localtime().time()
    start = datetime.time(8, 30, 0)
    end = datetime.time(9, 30, 0)
    if (start < now < end) and is_workday():
        return True
    else:
        return False


def is_rechargetime():
    weekday = timezone.localdate().isoweekday()
    if weekday in (1, 3) and is_ordertime():
        return True
    else:
        return False

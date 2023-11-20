import datetime

# 2010年1月1日至2022年8月9日间数据，输入数据为期间每日的 9点30分和13点1分
import time

t = datetime.datetime.now()  # 获取当前时间
print(t.replace(t.year, t.month, t.day, 9, 0, 0, 0))  # 获取当天早上8点
print(t.replace(t.year, t.month, t.day, 13, 0, 0, 0))  # 获取当天早上8点

# t2 = t.timestamp() + 86400
t2 = t + datetime.timedelta(days=1)
print(t2.replace(t2.year, t2.month, t2.day, 13, 0, 0, 0))





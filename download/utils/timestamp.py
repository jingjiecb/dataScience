#-*- codeing = utf-8 -*-
# @Time: 2020-04-30 14:02
# @Author: Claws
# @File: timestamp.py
# @Software: PyCharm
# @Description: 时间戳转时间

import time

# 将一个13位整数时间戳转换为时间字符串
# 输入时间为13位整数时间戳
def tsToTime(t):
    timeStamp = float(t/1000)
    timeArray = time.localtime(timeStamp)
    # 可以自定义输出格式
    res = time.strftime("%m-%d-%H-%M-%S", timeArray)
    print(res)

if __name__=='__main__':
    t = 1582023290656
    tsToTime(t)

#-*- codeing = utf-8 -*-
# @Time: 2020-07-05 18:05
# @Author: Claws
# @File: main.py
# @Software: PyCharm
# @Description: 检查输出主程序

from check.check import check
from draw.draw import draw
from draw.draw_multi import draw_multi

BORDER=0.5

def getMultiDict(tests=[]):
    res = {}
    for test in tests:
        try:
            res[test]=check(testId)
        except:
            if test in res.keys():
                res.pop(test)

if __name__=='__main__':

    testId = "2209"
    testList = ["", "", "", "", ""]

    # while True:
    #     res=check(testId)
    #     bad_code=list(filter(lambda x:res[x]>BORDER,res))
    #     print(len(bad_code))
    #     print(bad_code)
    #     testId = input()

    draw(check(testId),testId)
    # draw_multi(getMultiDict(testList))
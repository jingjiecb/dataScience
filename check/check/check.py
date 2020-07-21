#-*- codeing = utf-8 -*-
# @Time: 2020-07-16 12:29
# @Author: Claws
# @File: check.py
# @Software: PyCharm
# @Description: 综合检查

from check.checkByIO import checkByIO
from check.countlines import checkByLines
from check.IfElse import checkByIfElse

'''
输入: testID 题目ID
输出: 字典，键为代码文件名，值为综合面向用例怀疑度(0.0~1.0)
'''

RATE_IO=0.484
RATE_IF_ELSE=0.363
RATE_LINE=0.153

def check(testId):
    resByIO=checkByIO(testId)
    resByLines=checkByLines(testId)
    resByIfElse=checkByIfElse(testId)
    finalRes={}

    try:
        for code in resByIO.keys():
            finalRes[code]=RATE_IO*resByIO[code]+RATE_IF_ELSE*resByIfElse[code]+RATE_LINE*resByLines[code]*0.5
    except:
        print("Error: "+testId)

    return finalRes
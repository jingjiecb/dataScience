# -*- codeing = utf-8 -*-
# @Time: 2020-07-02 20:33
# @Author: duolaharry
# @File: countlines.py
# @Software: PyCharm
# @Description: 统计代码行数

import os
import json
from configparser import ConfigParser

cfg=ConfigParser()
cfg.read("config.ini",encoding="UTF-8")
codeBasePath=cfg.get("path","code_path")
testBasePath=cfg.get("path","test_path")

def countlines(filepath):
    count1 = 0
    # 判断给定的路径是否是py文件
    if filepath.endswith('.py'):
        # 打开文件
        currentFile = open(filepath, 'r', encoding='utf-8')
        # 读取一行
        line = currentFile.readline()
        # 当读取的代码行不是空的时候进入while循环
        while line != '':
            # 判断代码行不是换行符\n且不是注释行时进入,代码行数加1
            if line != '\n' and '#' not in line :
                count1 += 1
                # 接着读取下一行
            line = currentFile.readline()
        currentFile.close()
    return count1


def getVar(list, average):
    tmpSum = 0
    for num in list:
        tmpSum += (num - average) * (num - average)
    return tmpSum / (len(list)-1)


def checkByLines(testId):
    sumOfLines = 0
    sumOfFiles = 0
    pathOfCode = codeBasePath
    pathOfQues = testBasePath
    # 输入要统计的题目的路径
    # print("请输入需要统计的题目代号")
    # question = input()
    eachPath = '\\'+str(testId)
    path = pathOfCode+eachPath
    pathOfQues = pathOfQues+eachPath+r"\testCases.json"
    # print(pathOfQues)
    #读取用例数目
    jFile = open(pathOfQues, encoding='utf-8')
    content = jFile.read()
    data = json.loads(content)
    standard = int(len(data))
    # print("测试用例总数为："+str(standard))
    count = 0
    listOfFiles = []
    listOfLines = []

    # 先进行系统抽样
    for subFile in os.listdir(path):
        # 系统抽样：每隔四个不选入样本中
        # if count % 4 != 3:
            fullName = os.path.join(path, subFile)
            tmpLines = countlines(fullName)
            listOfFiles.append(subFile)
            listOfLines.append(tmpLines)
            sumOfLines += tmpLines
            sumOfFiles += 1
        # count += 1
    # print("文件总数为：" + str(sumOfFiles))
    # print("代码行数为：" + str(listOfLines))

    #初始化怀疑度列表
    listOfDoubt = []
    for i in range(0,len(listOfFiles)):
        listOfDoubt.append(0)

    # 求均值与方差
    average = sumOfLines / sumOfFiles
    var = getVar(listOfLines, average)
    # print('样本均值为：' + str(average))
    # print('样本方差为：' + str(var))

    # # 用正态分布拟合样本确定置信区间
    # print("请输入置信水平：\n1.80%\n2.85%\n3.90%\n4.95%\n5.97.5%\n6.99%\n7.99.5%")
    # α = int(input())
    # z = 0
    # if α == 1:
    #     z = 0.84
    # elif α == 2:
    #     z = 1.04
    # elif α == 3:
    #     z = 1.28
    # elif α == 4:
    #     z = 1.65
    # elif α == 5:
    #     z = 1.96
    # elif α == 6:
    #     z = 2.33
    # elif α == 7:
    #     z = 2.58
    # else:
    #     print("输入置信水平有错。即将退出。")
    #     sys.exit()
    # print("置信水平为95%")
    z = 1.65

    # 计算在置信区间内的代码行数
    lowBound = average - z * ((var / sumOfFiles) ** 0.5)
    # print('置信区间为：[' + str(lowBound) + ',' + '+∞]')

    # 计算面向用例区间内的代码行数
    # print("请输入偏移量")
    # k = int(input())
    k = 7
    up = standard*2+k
    down = standard*2-k
    # print('面向用例区间为：['+str(down)+','+str(up)+']')

    # 找出在置信区间外的代码文件
    listOfdistrust = []
    for i in range(0, sumOfFiles):
        if not (lowBound < listOfLines[i]):
            listOfdistrust.append(listOfFiles[i])
            listOfDoubt[i]+=1
    # print('判定在置信区间外的文件为：' + str(listOfdistrust) + '\n,共' + str(len(listOfdistrust)) + '份。')

    # 找出在面向用例区间内的代码文件
    listOfExampleOriented = []
    for i in range(0, sumOfFiles):
        if down<=listOfLines[i]<=up:
            listOfExampleOriented.append(listOfFiles[i])
            listOfDoubt[i]+=1
    # print('判定在面向用例区间内的文件为：' + str(listOfExampleOriented) + '\n,共' + str(len(listOfExampleOriented)) + '份。')

    #找出共有区间
    # listOfDouble = []
    # for i in listOfExampleOriented:
    #     if i in listOfdistrust:
    #         listOfDouble.append(i)
    # print('判定有更大嫌疑的文件为：' + str(listOfDouble) + '\n,共' + str(len(listOfDouble)) + '份。')

    #返回一个字典
    dict = {}

    for i in range(0,len(listOfDoubt)):
        dict[listOfFiles[i]] = listOfDoubt[i]

    return dict

# if __name__=="__main__":
#     print(linesOfEO(2063))
#     list = [2063,2088,2171,2383,2617,2936,2618,2894,2701,2610,2558,2506,2467,2461,2444,2425,2397,2390,2371,2345,2338,2308,2288,2209,2190,2184,2177,2153,2097]
#     list.sort()
#     list2 = []
#     for i in list:
#         tmp = '\\'+str(i)
#         list2.append(linesOfEO(tmp))
#     for i in range(0,len(list)):
#         print("-----------------------"+str(list[i])+"---------------------------")
#         print()
#         print(str(list2[i]))
#         print()
#         print(len(list2[i]))
#         print()

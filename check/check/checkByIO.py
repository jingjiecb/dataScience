#-*- codeing = utf-8 -*-
# @Time: 2020-07-05 18:07
# @Author: Claws
# @File: checkByIO.py
# @Software: PyCharm
# @Description: 负责检查的模块

import json
import os
from configparser import ConfigParser

cfg=ConfigParser()
cfg.read("config.ini",encoding="UTF-8")
codeBasePath=cfg.get("path","code_path")
testBasePath=cfg.get("path","test_path")

simplePuts=["True","False","true","false","1","0","-1","2","-2","3","4","5","6","7","8","9","10","YES","NO","yes","no","Yes","No","TRUE","FALSE"]

def check(code, test):
    # 获得测试用例
    jFile = open(test, encoding='utf-8')
    content = jFile.read()
    tests = list(json.loads(content))

    inputs=[]
    outputs=[]

    for test in tests:
        inputs.append(test["input"].strip('\n').strip(']').strip('[').strip(r'\n'))
        outputs.append(test["output"].strip('\n').strip(']').strip('[').strip(r'\n'))
    total = len(inputs)


    # 对含有换行的测试用例进行拆解
    for i in range(total):
        inputs[i]=inputs[i].split("\n")
        outputs[i]=outputs[i].split("\n")


    # 获取代码内容
    cFile=open(code,encoding='utf-8')
    cContent=cFile.read()


    # 代码检查
    try:
        in_counter=0
        out_counter=0
        for _input in inputs:
            match = True
            simple = True
            for _part in _input:
                if _part not in simplePuts:
                    simple = False
                    if _part not in cContent:
                        match=False
                        break
            if match and not simple:
                in_counter+=1
                # print(_input)
        for _output in outputs:
            match = True
            simple = True
            for _part in _output:
                if _part not in simplePuts:
                    simple=False
                    if _part not in cContent:
                        match=False
                        break
            if match and not simple:
                out_counter+=1
                # print(_output)
    except:
        # print("can not parse")
        return -1.0

    return max(in_counter,out_counter)/total

def checkByTestId(testId,isBigData):
    codePath=codeBasePath+testId+'/'
    testPath=testBasePath+testId+'/'+"testCases.json"

    badCodes=dict()
    total=0

    g=os.walk(codePath)
    for path, dir_list, file_list in g:
        for file_name in file_list:
            total+=1
            # print(file_name)
            value=check(path + file_name, testPath)
            badCodes[file_name]=value

    if isBigData:
        offset=min(badCodes.values())
        if offset>=0.5:
            for badCode in badCodes.keys():
                badCodes[badCode]=0.0
        elif offset>0:
            for badCode in badCodes.keys():
                badCodes[badCode]-=offset

    # for badCode in badCodes:
    #     if badCode[1]==0.0:
    #         badCodes.remove(badCode)

    # badCounter=len(badCodes)
    # print("total: "+str(total)+" bad: "+str(badCounter),end="")
    # print(badCodes)
    return badCodes

def checkAllByTest(isBigData):
    badTests=[]

    g=os.walk(codeBasePath)
    for path, dir_list, file_list in g:
        for testId in dir_list:
            try:
                print(testId+": ",end="")
                checkByTestId(testId,isBigData)
            except:
                print(testId+" no such test file!!!**********************")
                continue

    print(badTests)

def checkByIO(testId):
    return checkByTestId(testId,True)
#-*- codeing = utf-8 -*-
# @Time: 2020-05-14 19:18
# @Author: Claws
# @File: unitFactory.py
# @Software: PyCharm
# @Description: json文件处理模块，提取信息供其他模块使用

import json
from utils.unit import CodeUnit,FullCodeUnit

class UnitFactory:
    dataList=[]
    dirT=1

    def __init__(self,path):
        # 导入json文件
        jFile = open(path, encoding='utf-8')
        content = jFile.read()
        data = json.loads(content)
        self.dataList = list(data.values())

    def setDirType(self,dirType):
        self.dirT=dirType

    def setRange(self,start,end):
        self.dataList=self.dataList[start-1:end]

    def getUserNum(self):
        return len(self.dataList)

    def processUsers(self):
        for user in self.dataList:
            yield user

    def getLastestCode(self):
        user_itr=self.processUsers()
        for user in user_itr:
            userId = str(user["user_id"])
            tests = user["cases"]

            for test in tests:
                testId=test["case_id"]
                codes=test["upload_records"]
                if len(codes)>0:
                    code=codes[-1]
                    url = code["code_url"]
                    yield CodeUnit(url,userId,testId,self.dirT)

    def getAllCode(self):
        user_itr=self.processUsers()
        for user in user_itr:
            userId = str(user["user_id"])
            tests = user["cases"]

            for test in tests:
                testId = test["case_id"]
                codes = test["upload_records"]
                for code in codes:
                    url=code["code_url"]
                    uploadId=str(code["upload_id"])
                    yield FullCodeUnit(url,userId,testId,uploadId,self.dirT)

    def getFullMarkCode(self):
        user_itr=self.processUsers()
        for user in user_itr:
            userId = str(user["user_id"])
            tests = user["cases"]

            for test in tests:
                testId = test["case_id"]
                codes = test["upload_records"]
                finallScore=test["final_score"]
                if finallScore!=100:
                    continue
                for code in codes:
                    score=int(code["score"])
                    if score!=100:
                        continue
                    url=code["code_url"]
                    uploadId=str(code["upload_id"])
                    yield FullCodeUnit(url,userId,testId,uploadId,self.dirT)
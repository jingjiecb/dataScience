# -*- codeing = utf-8 -*-
# @Time: 2020-05-14 18:51
# @Author: Claws
# @File: unit.py
# @Software: PyCharm
# @Description: 下载信息单元，包含储存路径和URL

class Unit:
    url = ""
    path = ""
    def getPath(self):
        return ""
    def getUrl(self):
        return self.url


class CodeUnit(Unit):
    dirType=0
    userId=""
    testId=""
    baseDir="./LatestCodeDownload/"

    def __init__(self,url,uid,tid,type):
        self.url=url
        self.testId=tid
        self.userId=uid
        self.dirType=type

    def getPath(self):
        if self.path!="":
            return self.path

        if self.dirType==1:
            self.path=self.baseDir+self.userId+'_'+self.testId
        elif self.dirType==2:
            self.path=self.baseDir+self.testId+'_'+self.userId
        elif self.dirType==3:
            self.path=self.baseDir+self.userId+'/'+self.testId
        elif self.dirType==4:
            self.path=self.baseDir+self.testId+'/'+self.userId
        else:
            pass
        self.path+='.zip'
        return self.path


class FullCodeUnit(Unit):
    dirType=0
    userId=""
    testId=""
    upid=""
    baseDir="./FullCodeDownload/"

    def __init__(self,url,uid,tid,upid,type):
        self.url=url
        self.testId=tid
        self.userId=uid
        self.dirType=type
        self.upid=upid

    def getPath(self):
        if self.path!="":
            return self.path

        if self.dirType==1:
            self.path=self.baseDir+self.userId+'_'+self.testId+'_'+self.upid
        elif self.dirType==2:
            self.path=self.baseDir+self.testId+'_'+self.userId+'_'+self.upid
        elif self.dirType==3:
            self.path=self.baseDir+self.userId+'/'+self.testId+'_'+self.upid
        elif self.dirType==4:
            self.path=self.baseDir+self.testId+'/'+self.userId+'_'+self.upid
        else:
            pass
        self.path+='.zip'
        return self.path
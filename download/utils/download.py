#-*- codeing = utf-8 -*-
# @Time: 2020-05-14 19:00
# @Author: Claws
# @File: download.py
# @Software: PyCharm
# @Description: 下载函数库

# 下载一个zip包
import requests
import os
from utils.unit import Unit
from utils.unzip import unzip_record,unzip_question

# 请求头，防止访问被拒绝
header2 = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    'Connection': 'Keep-Alive',
    'Referer': "http://mooctest-site.oss-cn-shanghai.aliyuncs.com"
}

def downloadCodeUnit(unit=Unit()):

    filePath=unit.getPath()
    url=unit.getUrl()
    dirname=os.path.dirname(filePath)
    # if not os.path.exists(dirname):
    #     os.mkdir(dirname)
    try:
        os.makedirs(dirname)
    except:
        pass

    try:
        with open(filePath, 'wb') as f:
            zipC = requests.get(url, headers=header2).content
            f.write(zipC)
    except Exception:
        print('\033[7;31merror || '+filePath+' 下载失败！\033[0m')

    unzip_record(filePath)
    os.remove(filePath)
    print("info || succeed to download and unzip ===> " + filePath)


# 下载一个zip包
def download_one(filePath,url):
    try:
        with open(filePath, 'wb') as f:
            zipC = requests.get(url, headers=header2).content
            f.write(zipC)
            print("info || succeed to download ===> " + filePath)
    except Exception:
        print('\033[7;31merror || '+filePath+' 下载失败！\033[0m')
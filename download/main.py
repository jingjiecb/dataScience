#-*- codeing = utf-8 -*-
# @Time: 2020-04-30 8:44
# @Author: Claws
# @File: main.py
# @Software: PyCharm
# @Description: 下载题目的压缩包

import json
import multiprocessing
import requests
import os
import time
from utils.unzip import unzip_record,unzip_question

# 请求头，防止访问被拒绝
header2 = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
    'Connection': 'Keep-Alive',
    'Referer': "http://mooctest-site.oss-cn-shanghai.aliyuncs.com"
}

# 下载一个user的所有数据
def download_user(user):
    userId=str(user["user_id"])
    cases=user["cases"]
    print("info || ready to download user ===> " + userId)

    # 创建用户目录
    try:
        os.mkdir('CodeDownload/'+userId)
    except Exception:
        print('\033[7;31mwarn || 创建用户文件夹失败，可能文件夹已经存在\033[0m')

    #遍历用户的所有题目数据
    for case in cases:
        caseId=case["case_id"]

        # 创建题目目录
        try:
            os.mkdir('CodeDownload/' + userId +'/' +caseId)
        except Exception:
            print('\033[7;31mwarn || 创建题目文件夹失败，可能文件夹已经存在\033[0m')

        # 题目目录
        basedir='CodeDownload/' + userId+'/'+case["case_id"] +'/'

        # 遍历提交记录
        records = case["upload_records"]
        for record in records:
            id=str(record["upload_id"])
            time=str(record["upload_time"])
            recordPath=basedir+id+'_'+time+'.zip'

            # 下载提交记录zip包
            download_one(recordPath,record["code_url"])

            # 用压缩文件中真正有用的部分替换整个压缩文件
            unzip_record(recordPath)
            os.remove(recordPath)

def download_user_latest(user):
    userId=str(user["user_id"])
    cases=user["cases"]
    print("info || ready to download user ===> " + userId)

    # 创建用户目录
    try:
        os.mkdir('CodeDownload/'+userId)
    except Exception:
        print('\033[7;31mwarn || 创建用户文件夹失败，可能文件夹已经存在\033[0m')

    #遍历用户的所有题目数据
    for case in cases:
        caseId=case["case_id"]

        # 储存地址
        basedir='CodeDownload/' + userId+'/'

        # 下载最后一次提交记录
        record = case["upload_records"][-1]
        recordPath=basedir+caseId+'.zip'

        # 下载提交记录zip包
        download_one(recordPath,record["code_url"])

        # 用压缩文件中真正有用的部分替换整个压缩文件
        unzip_record(recordPath)
        os.remove(recordPath)

# 下载一个zip包
def download_one(filePath,url):
    try:
        with open(filePath, 'wb') as f:
            zipC = requests.get(url, headers=header2).content
            f.write(zipC)
            print("info || succeed to download ===> " + filePath)
    except Exception:
        print('\033[7;31merror || '+filePath+' 下载失败！\033[0m')



if __name__=="__main__":
    # 创建根目录
    try:
        os.mkdir('CodeDownload')
    except Exception:
        print('\033[7;31mwarn || 创建下载文件夹失败，可能文件夹已经存在\033[0m')

    # 导入json文件
    jFile = open('data/sample.json', encoding='utf-8')
    content = jFile.read()
    data = json.loads(content)
    dataList=list(data.values())

    #多进程下载
    pool = multiprocessing.Pool(multiprocessing.cpu_count())


    print("input || 请选择下载方式，输入对应数字[default:2]：1-下载所有提交代码 2-仅下载最后一次提交代码")
    method=int(input())
    print("info || 检测到共 "+str(len(dataList))+" 个用户的数据")
    print("input || 请输入希望下载用户索引开始范围(包含)： ",end='')
    start=int(input())
    print("input || 请输入希望下载用户索引结束范围(包含)： ",end='')
    end=int(input())
    print("info || 将下载从第 " +str(start) +" 到 "+str(end)+" 个用户的数据。下载将于3s后马上开始。")
    time.sleep(3)

    if method==1:
        print("info || 开始下载全部代码")
        pool.map(download_user,dataList[start-1:end])
    else:
        print("info || 开始下载最后一次提交代码")
        pool.map(download_user_latest,dataList[start-1:end])

    pool.close()
    pool.join()
    print('****************************over****************************')

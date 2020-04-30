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
        os.mkdir('ZipDownload/'+userId)
    except Exception:
        print('\033[7;31mwarn || 创建用户文件夹失败，可能文件夹已经存在\033[0m')

    #遍历用户的所有题目数据
    for case in cases:
        caseId=case["case_id"]

        # 创建题目目录
        try:
            os.mkdir('ZipDownload/' + userId +'/' +caseId)
        except Exception:
            print('\033[7;31mwarn || 创建题目文件夹失败，可能文件夹已经存在\033[0m')

        # 下载题目zip包
        basedir='ZipDownload/' + userId+'/'+case["case_id"] +'/'
        questionPath = basedir+ "question.zip"
        download_one(questionPath,case["case_zip"])

        # 解压并删除题目zip包
        unzip_question(questionPath)
        os.remove(questionPath)

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
        os.mkdir('ZipDownload')
    except Exception:
        print('\033[7;31mwarn || 创建下载文件夹失败，可能文件夹已经存在\033[0m')

    # 导入json文件
    jFile = open('data/sample.json', encoding='utf-8')
    content = jFile.read()
    data = json.loads(content)

    #多进程下载
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(download_user,data.values())
    pool.close()
    pool.join()
    print('****************************over****************************')

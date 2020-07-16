#-*- codeing = utf-8 -*-
# @Time: 2020-04-30 8:44
# @Author: Claws
# @File: CodeDownload.py
# @Software: PyCharm
# @Description: 下载提交代码

import multiprocessing
import time
from sys import exit
from utils.unitFactory import UnitFactory
from utils.download import downloadCodeUnit
from utils.banner import printBanner


if __name__=="__main__":

    # 打印一个帅气的banner
    printBanner()

    # 多进程下载
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    # 打开文件
    print("input || 请输入json文件路径（带有文件名）：",end='')
    jsonPath=input()
    try:
        factory=UnitFactory(jsonPath)
    except:
        print('\033[7;31merror || 打开文件失败！\033[0m')
        exit(0)

    # 设置目录结构
    print('input || 请输入希望的目录结构：\n1. 全部在一个目录中，命名方式为用户ID+题目ID\n2. 全部在一个目录中，命名方式为题目ID+用户ID\n'+
    '3. 按照用户分子目录\n4. 按照题目分子目录\n请输入方法代号：',end='')
    dirType=int(input())
    factory.setDirType(dirType)

    # 设置下载方式
    print("input || 请选择下载方式，输入对应数字：\n1. 下载所有提交代码 \n2. 仅下载最后一次提交代码\n3. 仅下载满分代码\n请输入：",end='')
    method=int(input())

    # 选择下载范围
    print("info || 检测到共 "+str(factory.getUserNum())+" 个用户的数据")
    print("input || 请输入希望下载用户索引开始范围(包含)： ",end='')
    start=int(input())
    print("input || 请输入希望下载用户索引结束范围(包含)： ",end='')
    end=int(input())
    factory.setRange(start, end)

    # 确认下载
    print("info || 下载将于3s后马上开始，请再次确认下载内容。")
    time.sleep(3)

    # 下载计时
    last_time=time.time()

    # 根据选择的下载方式进行多线程下载
    if method==1:
        pool.map(downloadCodeUnit,factory.getAllCode())
    elif method==2:
        pool.map(downloadCodeUnit,factory.getLastestCode())
    elif method==3:
        pool.map(downloadCodeUnit,factory.getFullMarkCode())

    pool.close()
    pool.join()

    # 下载结束
    print('****************************over****************************')
    print('Totally took {} seconds'.format(time.time()-last_time))

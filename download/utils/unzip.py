#-*- codeing = utf-8 -*-
# @Time: 2020-04-30 11:51
# @Author: Claws
# @File: unzip.py
# @Software: PyCharm
# @Description: 解压文件

import zipfile
import tempfile
import os

# 解压一个文件夹中的全部文件到指定目录
def unzip_file(zip_src, dst_dir):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')

# 解压一个名为name的文件到指定目录
def unzip_one(zip_src, dst_dir, name):
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        fz.extract(name,dst_dir)
    else:
        print('This is not zip')

# 解压一个在压缩文件路径中为path的文件到同级目录
def unzip(zip_src,path):
    dir=os.path.dirname(zip_src)
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        fz.extract(path,dir)
    else:
        print('This is not zip')



# 用来将一个回答记录中的答案解压出来
# zip_src: zip包的相对路径
# 会把main.py提取到相同路径
# 相当于把zip包替换成一个同名文件
def unzip_record(zip_src):
    py_file_name=zip_src[:-3]+'py'
    # 传入参数dir可以在当前目录下创建临时文件夹（当前目录即此py文件所在目录）
    with tempfile.TemporaryDirectory(dir='') as tmp_dir:
        unzip_file(zip_src,tmp_dir)
        zip_src=tmp_dir+'/'+list(os.scandir(tmp_dir))[0].name
        unzip_one(zip_src,tmp_dir,'main.py')
        need_py_file=tmp_dir+'/main.py'
        # 这里用rename玩了一波骚操作，相当于把文件移动并改名了
        try:
            os.rename(need_py_file,py_file_name)
        except Exception:
            print('\033[7;31mwarn || 解压失败！可能文件已经存在\033[0m')

# 解压问题zip包中包含的有用信息：
# readme.md 题目描述
# .mooctest/testCases.json 测试用例
# .mooctest/answer.py c++官方解答
def unzip_question(zip_src):
    dir=os.path.dirname(zip_src)
    r = zipfile.is_zipfile(zip_src)
    if r:
        fz = zipfile.ZipFile(zip_src, 'r')
        fz.extract('readme.md',dir)
        fz.extract('.mooctest/testCases.json',dir)
        fz.extract('.mooctest/answer.py',dir)
    else:
        print('This is not zip')

if __name__=='__main__':
    zip_src='1581144899702.zip'
    unzip_question(zip_src)
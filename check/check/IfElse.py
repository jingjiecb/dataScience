import math
import os
import re
import numpy as np
from configparser import ConfigParser

cfg=ConfigParser()
cfg.read("config.ini",encoding="UTF-8")
codeBasePath=cfg.get("path","code_path")

# in: folder_name (Question Name)
# out: danger factors ( 0 or 1 )
def checkByIfElse(testId):
    # if-else 语句偏移计算
    # define: 一个分支（branch）是 if else elif 任意一个下的语句（不包含其中包含的二级 if else elif）
    # 思路： 1. 匹配 branch+print/return 模式
    #       // 2. 计算 if elif 条件句的平均句长，句长越长越有可能是面向用例

    # folder_name = input("打开的文件夹名：")
    # folder_name = "2064"

    path = codeBasePath + testId + '/'
    files = os.listdir(path)
    # print(files)  # get all files in the folder

    match_num_dict = {}
    condition_len = {}
    danger_factors = {}
    dfs = []

    for file in files:
        f_path = path + file
        with open(f_path, 'r', encoding='UTF-8') as code_file:
            code_text = code_file.read()
            code_lines = code_text.split('\n')
            i = len(code_lines) - 1
            while i > -1:
                pattern = re.compile(r'\s*#.*')
                if len(code_lines[i]) == 0 or re.match(pattern, code_lines[i]) != None:
                    code_lines.pop(i)
                    # remove empty line or code comments
                i -= 1

            code_text = str.join('#', code_lines)
            # print(code_text)

            pattern = re.compile(r'if.*?return')
            pattern1 = re.compile(r'if.*?print')
            pattern2 = re.compile(r'else.*?return')
            pattern3 = re.compile(r'else.*?print')
            find_arr = pattern.findall(code_text)
            find_arr = find_arr + pattern1.findall(code_text)
            find_arr = find_arr + pattern2.findall(code_text)
            find_arr = find_arr + pattern3.findall(code_text)

            i = len(find_arr) - 1
            hash_pattern = re.compile(r'#')
            while i > -1:
                if len(hash_pattern.findall(find_arr[i])) > 1:
                    find_arr.pop(i)
                i -= 1

            # print()
            # print("FOUND:", find_arr)
            # print("FOUND_NUM:", len(find_arr))

            pattern_cdt = re.compile(r'if.*?:')
            cdt = pattern_cdt.findall(''.join(find_arr))
            # print("CDT:", cdt)

            cdt_len_arr = [len(x.replace(" ", "")) - 3 for x in cdt]
            avg_cdt_len = np.mean(cdt_len_arr)
            # print("AVG_CDT_LEN:", avg_cdt_len)

            mid_cdt_len = np.median(cdt_len_arr)
            # print("MID_CDT_LEN:", mid_cdt_len)

            # print("CDT_LEN_ARR:", cdt_len_arr)
            
            find_num = len(find_arr)
            match_num_dict[file] = find_num
            if not math.isnan(mid_cdt_len):
                condition_len[file] = mid_cdt_len
            else:
                condition_len[file] = 0

            danger_factor = 0
            if find_num > 0 and mid_cdt_len > 0:
                danger_factor = find_num * mid_cdt_len ** 0.4
            danger_factors[file] = danger_factor

            if danger_factor > 0:
                dfs.append(danger_factor)

    # print(match_num_dict)
    # print(condition_len)
    # print(danger_factors)
    # print(dfs)

    sample_mean = np.mean(dfs)
    sample_var = np.var(dfs)
    z_0_995 = 2.575
    z_0_950 = 1.645
    z_0_900 = 1.285
    border_df = sample_mean + math.sqrt(sample_var / len(dfs)) * z_0_950
    
    # print(border_df)

    return_factors = {}
    danger_files = []
    for file in files:
        if danger_factors[file] > border_df:
            return_factors[file] = 1
            danger_files.append(file)
        else:
            return_factors[file] = 0
            
    # print()
    # print(border_df)
    # print("folder", testId, ":", danger_files)
    # print(len(danger_files))

    return return_factors


# test main func
# def main():
#     arr = [2063, 2088, 2171, 2383, 2617, 2936, 2618, 2894, 2701, 2610, 2558, 2506, 2467, 2461, 2444, 2425, 2397, 2390,
#            2371, 2345, 2338, 2308, 2288, 2209, 2190, 2184, 2177, 2153, 2097]
#     for fn in arr:
#         func(str(fn))


# main()

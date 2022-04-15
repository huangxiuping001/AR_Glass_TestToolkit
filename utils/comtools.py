# coding:utf-8
import sys

import os
import xlrd


# 字符串最小编辑距离
from datetime import datetime


def minDistance(word1, word2, cache={}):
    if not word1 and not word2:
        return 0
    if not len(word1) or not len(word2):
        return len(word1) or len(word2)
    if word1[0] == word2[0]:
        return minDistance(word1[1:], word2[1:])
    if (word1, word2) not in cache:
        inserted = 1 + minDistance(word1, word2[1:])
        deleted = 1 + minDistance(word1[1:], word2)
        replaced = 1 + minDistance(word1[1:], word2[1:])
        cache[(word1, word2)] = min(inserted, deleted, replaced)
    return cache[(word1, word2)]

# key_col 标识key所在的列；is_col 决定某行数据是否需要转换
def excel2json(file_path, key_col=0,sheet=0):
    data = xlrd.open_workbook(file_path)
    if data is not None:
        if isinstance(sheet,int):
            table = data.sheet_by_index(sheet)
        elif isinstance(sheet,str):
            table =data.sheet_by_name(sheet)
        else:
            return

        # 获取到数据的表头
        titles = table.row_values(0)
        # print titles
        result = {}
        ncols = table.ncols  # 列数
        # 按行取数据
        for i in range(1, table.nrows):
            row = table.row_values(i)
            # print "key:{0}".format(key)
            print(row[ncols-1])
            print(key_col)
            if int(row[ncols-1])==1:
                tmp = {}
                key = row[key_col]
                result[key] = {}
                for index, title in enumerate(titles):
                    ctype = table.cell(i,index).ctype
                    cell = table.cell_value(i,index)
                    if ctype == 2 and cell % 1 == 0:  # 如果是整形
                        cell = int(cell)
                    elif ctype == 3:
                        # 转成datetime对象
                        date = datetime(*xlrd.xldate_as_tuple(cell, 0))
                        cell = date.strftime('%Y/%d/%m')
                    elif ctype == 4:
                        cell = True if cell == 1 else False
                    tmp[title] = cell
                    # print "value:{0}".format(tmp[title])
                result[key] = tmp
        return result



# def get_audioPlay_state():
#     lines = os.popen('adb shell dumpsys audio |  findStr "state"').readlines()
#     if "stopped"in lines[len(lines)-1]:
#         return 0
#     else:
#         return 1
#
# if __name__ == '__main__':
#
#     s1 = "今天天气阴沉沉的，过一会可能会下雨，取消出行计划。"
#     s2 = "过一会可能会下雨，取消出行计划。"
#     print(excel2json(r"D:\ifly_code\translator__android__test_toolkit\script\LB\test_voicetrans_LB\check_lb.xlsx",0))

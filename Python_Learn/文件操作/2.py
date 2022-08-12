#!/usr/bin/python3
# -- coding:utf-8 --
# author: xiuping.huang
# @time:2022/8/12 0012 23:28
# 在当前目录新建目录img, 里面包含100个文件, 100个文件名各不相同(X4G5.png)
import os
import random
import string

if os.path.exists('F:\AR_Glass_TestToolkit\img') is not True:
    os.mkdir("F:\AR_Glass_TestToolkit\img")
img = "F:\AR_Glass_TestToolkit\img"
for i in range(5):
    name = ''.join(random.sample(string.ascii_letters + string.digits, 4))
    filename = img + '\\' + name + '.png'
    print(filename)
    with open(filename, 'w') as file:
        file.close()

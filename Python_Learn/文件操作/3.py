#!/usr/bin/python3
# -- coding:utf-8 --
# author: xiuping.huang
# @time:2022/8/13 0013 0:12

#将题目2中的img目录中所有以.png结尾的后缀名改为.jpg 。
import os

img = "F:\AR_Glass_TestToolkit\img"
for i in os.listdir(img):
    new = i.replace('.png', '.jpg')
    os.rename(img + "\\" + i, img + "\\" + new)

#!/usr/bin/python3
# -- coding:utf-8 --
# author: xiuping.huang
# @time:2022/8/13 0013 0:17
# 生成100个MAC地址并写入文件中，MAC地址前6位（16进制）为01-AF-3B，格式为：01-AF-3B-xx-xx-xx。
import string
import random


def create_mac():
    mac = '01-AF-3B'
    hex_num = string.hexdigits
    for i in range(3):
        n = random.sample(hex_num, 2)
        sn = '-' + ''.join(n).upper()
        mac += sn
    return mac


# 随机生成一个mac地址
def test():
    with open('mac.txt', 'w') as file:
        for i in range(100):
            mac = create_mac()
            print(mac)
            file.write(mac + '\n')


test()

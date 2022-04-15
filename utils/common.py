# -*- coding: utf-8 -*-
# File  : common.py
# Author: qxguo4
# Date  : 2021/4/15

import os
import sys

class common(object):

    def __init__(self):
        '''

        '''

    @staticmethod
    def read_device(case_path="test"):
        '''
        获取devices
        :return:
        '''

        pre_path=sys.path[0]
        pre_path_split=pre_path.split("\\")
        count=0
        for spath in pre_path_split:
            if spath=="translator__android__test_toolkit":
                break
            count+=1
        pre_path_new=""
        for i in range(0,count+1):
            pre_path_new = pre_path_new+pre_path_split[i]+"\\"

        device_path = pre_path_new + "PersistenceTest\\%s\\device.txt"%(case_path)
        device_file = open(device_path, "r")
        device = device_file.readlines()
        device_file.close()
        return device[0].strip()

    @staticmethod
    def get_root_path():
        '''
        获取根目录
        :return:
        '''
        pre_path=sys.path[0]
        pre_path_split=pre_path.split("\\")
        count=0
        for spath in pre_path_split:
            if spath=="translator__android__test_toolkit":
                break
            count+=1
        pre_path_new=""
        for i in range(0,count+1):
            pre_path_new = pre_path_new+pre_path_split[i]+"\\"
        return pre_path_new
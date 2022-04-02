# coding:utf-8
"""
Created on 2022年4月2日

@author: 黄秀平
"""
import codecs
import os
import random
import subprocess
import threading
import time
import unittest
import uiautomator2 as u2
import xlrd
import pyttsx3
import sys
deviceId = 'ad4dc83e'








class AI_Voice_Test(unittest.TestCase):

    def setup(self):
        self.d = u2.connect(deviceId)  # 设备号

    def teardown(self):
        pass

    def __TextToSpeech(self, text):
        self.engine = pyttsx3.init()
        volume = self.engine.getProperty('volume')
        self.engine.setProperty('volume', 1)
        print("开始播报...")
        self.engine.say(text)
        self.engine.runAndWait()  # 等待播报完毕
        self.engine.stop()  # 结束引擎

    def test_PlaySpeech(self):
        text01="hey,小纪，帮我打开相册"
        print(11111)
        self.__TextToSpeech(text01)

    def _GetTextFromExcel(self,Check_file):
        data = xlrd.open_workbook(Check_file)  # 打开excel文件，读取数据

        worksheet1 = data.sheet_by_name(u'Sheet1')  # 根据工作表的名称获取里面的行列内容
        # 获取工作表的名称、行数、列数
        # name = worksheet1.name  # 表名
        rowNum = worksheet1.nrows  # 行数
        # colNum = worksheet1.ncols  # 获取表的列数
        for curr_row in range(rowNum):
            # 遍历sheet1中所有行row
            row = worksheet1.row_values(curr_row)
            print('row%s is %s' % (curr_row, row))

        print(worksheet1.row_values(0))  # 获取工作表第一行的所有字段列表
    def test02_UseExcel(self):
        File = r'C:\Users\LX\android__test_toolkit\android__test_toolkit\AR_Glass'
        self._GetTextFromExcel(File)

if __name__ == '__main__':
    unittest.main()
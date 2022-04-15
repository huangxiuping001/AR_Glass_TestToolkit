# -*-coding: UTF-8 -*-
'''
Created on 2019年5月6日

@author: qxguo2
'''

import time
import os
import subprocess
import threading


class Logcat(object):
    '''
    classdocs
    '''

    def __init__(self, filenema):
        '''
        Constructor
        '''
        self.logcat_path = os.path.abspath(os.path.join(os.getcwd(), "../Logcat")) + "//"  # logcat日志存储路径
        self.filenema = filenema
        self.logcat_file = None
        self.Poplog = None
        self.isout = True
        self.iscontinue = True

    def logcat_outfile(self, tag=""):
        '''
        创建logcat输出文件
        '''
        os.system("adb logcat -c")
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))  # 获取当前时间
        self.filename = self.logcat_path + self.filenema + now + r"_log.txt"  # 日志文件名添加当前时间
        self.filename = self.filename.replace("//", "\\")
        self.logcat_file = open(self.filename, 'w')
        if tag == "":
            logcmd = "adb logcat -v time"
        else:
            logcmd = "adb logcat -v time -s %s" % (tag)
        self.Poplog = subprocess.Popen(logcmd, stdout=self.logcat_file, stderr=subprocess.PIPE)

    def logcat_close(self):
        '''
        关闭logcat输出文件
        '''
        self.logcat_file.close()
        self.Poplog.terminate()
        self.isout = True

    def logcat_create(self):

        while self.iscontinue:
            self.logcat_outfile()
            while self.isout:
                fsize1 = os.path.getsize(self.filename)
                fsize = (fsize1 / 1024) / 1024
                if fsize > 50:
                    self.isout = False
                    print("go to 50M++++++++++++++++")
                time.sleep(20)
            self.logcat_close()

    def logcat_start(self):
        t1 = threading.Thread(target=self.logcat_create)
        t1.start()

    def logcat_end(self):
        self.iscontinue = False
        self.isout = False

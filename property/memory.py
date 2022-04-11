# -*- coding: utf-8 -*-
import os

from property.datacollection import DataCollection
from property.dataschema import DataSchema
# from property.connectsql import ConnectSql
import threading
import re
import time
import numpy as np
from pyecharts import Line

from utils.filetools import fileUtils

class Memory(DataCollection):

    def __init__(self, packageName = '', deviceId = '', type = 1):
        super(Memory, self).__init__(packageName, deviceId)
        self.__looper_thread = None
        self.type = type

        self.totalPss = 0
        self.userPss = 0

        self.deviceId = deviceId
        #初始化折线图数据数组
        self.data1=[]
        self.data2=[]
        self.datalist = [self.data1, self.data2]

        self.data1_desc=''
        self.data2_desc = ''
        #self.dumpsysmeminfo = open("dumpsysmeminfo.txt", 'w')

        # self.con = ConnectSql("localhost", 3306, "root", "guoqx123", "test")

    #h获取总的和目标进程的pss
    def __getMem(self):

        try:
            cmd = 'dumpsys meminfo'

            pi = self.tools.shell_pi(cmd)
            lines = pi.stdout.readlines()
            pi.kill()

            for line in lines:

                if line is None:
                    continue
                line=str(line)
                # self.dumpsysmeminfo.write(line+"\n")
                # self.dumpsysmeminfo.flush()

                if 'offline' in line or 'Used' in line:
                    if 'offline' in line:
                        #print(line)
                        sum = int(re.findall("\d+", line)[0])
                        #print("sum = " + str(sum))
                        sum = sum * 1000 + int(re.findall("\d+", line)[1])

                        if sum is not None and sum > 0:
                            self.userPss = sum

                    elif 'Used' in line:
                        temp = line.split()
                        result = re.findall("\d+", temp[4])
                        len = result.__len__()

                        if len == 3:
                            self.totalPss = int(result[0]) * 1000000 + int(result[1]) * 1000 + int(result[2])
                        else:
                            result = re.findall("\d+", temp[5])

                            self.totalPss = int(result[0]) * 1000 + int(result[1])

            total_pss = round(self.totalPss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉
            user_pss = round(self.userPss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉

            print("TotalPss = " + str(total_pss) + ", UserPss = " + str(user_pss))
            # self.dumpsysmeminfo.write("+++++++++++++++++++++++++++++++++++++++++++++++++" + "\n")
            # self.dumpsysmeminfo.flush()
            fileUtils.write_file(self.logFileName, str(int(time.time() * 1000)) + "\t" + str(user_pss) + "\t" + str(total_pss) + "\n")

            # if user_pss > 100:
            #     ti = threading.Thread(target=self.__dump_memory(self.deviceId))
            #     ti.start()

            # self.data_queue.put_nowait([DataCollection.getCurrentTime(), total_pss, user_pss])
        except EOFError as E:
            print(E)

        # h获取总的和目标进程的pss
        def get_target_mem_and_total(self):

            try:
                cmd = 'dumpsys meminfo '

                pi = self.tools.shell_pi(cmd)
                lines = pi.stdout.readlines()
                pi.kill()

                for line in lines:

                    if line is None:
                        continue

                    line = str(line)

                    if 'offline' in line or 'Used' in line:
                        if 'offline' in line:
                            if self.totalPss != 0:
                                continue

                            sum = int(re.findall("\d+", line)[0])

                            sum = sum * 1000 + int(re.findall("\d+", line)[1])

                            if sum is not None and sum > 0:
                                self.userPss = sum
                            print("sum = " + str(sum))

                        elif 'Used' in line:
                            #print(line)
                            temp = line.split()

                            sum_list  = re.findall("\d+", temp[5])

                            sum_list.__len__()

                            print(str("length = " + sum_list))

                            self.totalPss = int(re.findall("\d+", temp[5])[0]) * 1000 + int(
                                re.findall("\d+", temp[5])[1])

                total_pss = round(self.totalPss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉
                user_pss = round(self.userPss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉

                print("TotalPss = " + str(total_pss) + ", UserPss = " + str(user_pss))

                # self.data_queue.put_nowait([DataCollection.getCurrentTime(), total_pss, user_pss])
            except EOFError as E:
                print(E)

    # 获取目标进程的pss
    def __getTargetPss(self):

        try:
            cmd = 'dumpsys meminfo ' +  self.packageName + ' | findstr TOTAL'

            pi = self.tools.shell_pi(cmd)
            line = pi.stdout.readline()
            pi.kill()

            line = str(line)

            if "TOTAL" in line:

                temp = line.split()

                pss = int(temp[2])

                user_pss = round(pss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉

                print("UserPss = " + str(user_pss))

                # self.data_queue.put_nowait([DataCollection.getCurrentTime(), user_pss, 0])

                fileUtils.write_file(self.logFileName, str(int(time.time() * 1000)) + "\t" + str(user_pss) + "\n")

        except EOFError as E:
            print(E)

    # 获取目标进程的pss
    def __getTargetPss_Native(self):

        try:
            cmd = 'dumpsys meminfo ' +  self.packageName+ ' | findstr "Native TOTAL"'

            pi = self.tools.shell_pi(cmd)
            lines = pi.stdout.readlines()
            pi.kill()
            if len(lines)>0:
                native=lines[0]
                temp = native.split()
                native_pss = int(temp[2])
                user_pss_native = round(native_pss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉

                total=lines[1]
                temp = total.split()
                total_pss = int(temp[1])
                total_pss = round(total_pss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉

                #添加折线图数组数据
                self.data1.append(total_pss)
                self.data2.append(user_pss_native)

                # 折线图数据汇总
                self.data1_desc = u'total内存'
                self.data2_desc = u'native内存'

                fileUtils.write_file(self.logFileName,str(int(time.time() * 1000)) + "\t" + str(total_pss) + "\t" + str(user_pss_native) + "\n")
        except EOFError as E:
            print(E)

    # 获取总的pss
    def __getTotalPss(self):

        try:
            cmd = 'procrank |findstr "TOTAL"'

            pi = self.tools.shell_pi(cmd)
            output = pi.stdout.readlines()
            pi.kill()

            for line in output:
                if line is None:
                    continue

                line = str(line)

                if 'TOTAL' in line:
                    sum = int(re.findall("\d+", line)[0])

                    if sum is not None and sum > 0:
                        self.totalPss = sum

            total_pss = round(self.totalPss / 1024, 2)  # 如果希望输出的内存数据单位为KB，就把这句备注掉

            print("TotalPss = " + str(total_pss))

            self.data_queue.put_nowait([DataCollection.getCurrentTime(), total_pss, 0])
            fileUtils.write_file(self.logFileName, str(int(time.time() * 1000)) + ":" + str(total_pss) + "\n")
        except EOFError as E:
            print(E)

    def start(self, logName = ""):
        self.switch = True

        self.data1=[]
        self.data2=[]

        if not logName == "":
            self.logFileName = logName

            if not self.logFileName.endswith('.txt'):
                self.logFileName = self.logFileName + '_pss.txt'

            fileUtils.clean_file(self.logFileName)

        if not self.isStart:
            self.isFirst = True
        else:
            print('Thread is start! What would you want to do?')
            return

        t1 = None
        if self.type == 1:
            t1 = threading.Thread(target=self.__looperPss)
        elif self.type == 2:
            t1 = threading.Thread(target=self.__looperTotal)
        elif self.type == 3:
            t1 = threading.Thread(target=self.__looperTarget)
        elif self.type == 4:
            t1 = threading.Thread(target=self.__looperTarget_native)

        t1.start()

    def __looperPss(self):
        while self.switch:
            self.__getMem()
            time.sleep(1)

    def __looperTotal(self):
        while self.switch:
            self.__getTotalPss()
            time.sleep(2)

    def __looperTarget(self):
        while self.switch:
            self.__getTargetPss()
            time.sleep(2)

    def __looperTarget_native(self):
        while self.switch:
            self.__getTargetPss_Native()
            time.sleep(2)


    def end(self, name = "",subname=""):
        # if self.data_queue is None or self.data_queue.qsize() == 0:
        #     print("Queue's is empty! Don't countiue")
        #     return
        self.switch = False
        # if self.type == 1:
        #     self.makeChart(2, name)
        # else:
        #     self.makeChart(8, name)
        self.isStart = False
        #获取平均值与最大值
        dataschema = DataSchema(name)
        # total_average_pss,total_max_pss=dataschema.average_max(self.data1)
        # native_average_pss, native_max_pss = dataschema.average_max(self.data2)
        # if not subname=="":
        #     update_sql="update camera_perform set perform_type='pss',total_max=%.2f,total_average=%.2f where res='%s'"%(total_max_pss,total_average_pss,subname)
        #     self.con.update_db(update_sql)
        #
        #     update_sql="update camera_perform set perform_type='pss',native_max=%.2f,native_average=%.2f where res='%s'"%(native_max_pss,native_average_pss,subname)
        #     self.con.update_db(update_sql)

        #折线图绘制
        self.data_desc = [self.data1_desc, self.data2_desc]
        dataschema.line_chart(self.data_desc,self.data1,self.data2)

        self.data1=[]
        self.data2=[]

    def __dump_memory(self, deviceId = ''):
        start = time.time()

        cmd = "adb -s " + deviceId + " shell dumpsys meminfo > " + os.getcwd() + "\dump_" + str(start).split(".")[
            0] + ".txt"

        os.system(cmd)

if "__name__" == "__main__":
    mem = Memory()
    mem.start()
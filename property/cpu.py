# -*- coding: utf-8 -*-
import sys
import threading
import re
import time
import numpy as np
from pyecharts import Line

from property.datacollection import DataCollection
from utils.filetools import fileUtils

class CPU(DataCollection):

    #type用来区分获取的是cpu占用时长还是cpu占用率, 1是cpu占用率，2是cpu占用时长
    def __init__(self, packageName = "", deviceId = "", type = 1):
        super(CPU, self).__init__(packageName, deviceId)
        self.type  = type
        self.last_idle = 0
        self.last_totalCpu = 0
        self.last_userCpu = 0

        self.last_userTime = 0

        self.logFileName = ""
        self.isStart = False
        self.isFirst = True

        #初始化折线图数据数组
        self.data1=[]
        self.data2=[]

    # 获取utime和stime
    # utime       该任务在用户态运行的时间，单位为jiffies
    # stime       该任务在核心态运行的时间，单位为jiffies
    # cutime      所有已死线程在用户态运行的时间，单位为jiffies
    # cstime      所有已死在核心态运行的时间，单位为jiffies
    def __get_u_s_time(self):
        print("self.pid = " + self.pid)

        output = self.__getUSTOutput()

        if output == '':
            print("pid change, re get pid by packageName")

            return -1, -1, -1, -1

        line = re.split(r'[\s]', output)

        try:
            utime = int(line[13])
            stime = int(line[14])
            cutime = int(line[15])
            cstime = int(line[16])

        except Exception as e:
            print(e)
            return -1, -1, -1, -1

        return utime, stime, cutime, cstime

    def __getUSTOutput(self):
        pi = self.tools.shell_pi("cat /proc/%s/stat" % (self.pid))
        output = pi.stdout.read()
        pi.kill()

        output = output.decode("utf-8")

        return output

    #每5s获取一次utime和stime并减去上一次的数据来获取5s内的cpu占用时长
    def __getCpuUsedTime(self):
        u, s, cu, cs = self.__get_u_s_time()

        if u == -1 and cu == -1:
            return

        usercpu = u + s + cu + cs

        if self.isFirst:
            self.isFirst = False
        elif usercpu > 0 :
            # 记录总的用户cpu占用时长
            # self.data_queue.put_nowait([DataCollection.getCurrentTime(), usercpu - self.last_userTime, 0])
            print("userCpu = " + usercpu)

        self.last_userTime = usercpu

    #获取idle以及去除idle之外的cpu占用
    def __getTotalCpuAndIdle(self):
        try:
            pi = self.tools.shell_pi('cat /proc/stat | findstr cpu')
            output = pi.stdout.read()
            pi.kill()

            output = output.decode("utf-8")

            if not output:
                return -1, -1

            res = output.split("\n")
            for line in res:
                if line.strip() == '':
                    print("none line")
                    continue
                info = line.split()

                if info[0] == "cpu":
                    # 各字段具体含义详见 Linux用户手册：http://man7.org/linux/man-pages/man5/proc.5.html
                    user = info[1]
                    nice = info[2]
                    system = info[3]
                    idle = info[4]
                    iowait = info[5]
                    irq = info[6]
                    softirq = info[7]
                    stealtolen = info[8]
                    guest = info[9]
                    guest_nice = info[10]

                    result = int(user) + int(nice) + int(system) + int(iowait) + int(irq) + int(softirq) + int(stealtolen) + int(guest) + int(guest_nice)
                    return int(result), int(idle)
        except EOFError as E:
            print(E)
            return -1, -1

    #获取目标进程和总的cpu占用率
    #idle和totalCpu是累计量，计算出1s内总的cpu增长值和用户占用增长值再相除得比例
    def __getCpuRate(self):
        try:
            totalCpu, idle = self.__getTotalCpuAndIdle()
            u, s, cu, cs = self.__get_u_s_time()

            if totalCpu == -1 or u == -1:
                print("totalCpu or utime/stime get error,maybe due to pid changes, countine.")
                self.pid = self._getPidByPkg()
                return False

            usercpu = u + s + cu + cs

            if self.isFirst:
                self.isFirst = False
                self.last_totalCpu = totalCpu
                self.last_idle = idle
                self.last_userCpu = usercpu
            elif totalCpu >= 0 and idle >= 0 and usercpu >= 0:

                t_cpu = totalCpu - self.last_totalCpu
                i_idle = idle - self.last_idle
                u_cpu = usercpu - self.last_userCpu

                self.last_idle = idle
                self.last_totalCpu = totalCpu
                self.last_userCpu = usercpu

                totalCpuRate = 100 *  t_cpu / (t_cpu + i_idle)
                userCpuRate = 100 * u_cpu / (t_cpu + i_idle)

                #保留2位小数
                cpu = round(totalCpuRate, 2)
                u_cpu = round(userCpuRate, 2)

                if cpu < 0:
                    cpu = 0
                elif cpu > 100:
                    cpu = 100

                if u_cpu < 0:
                    u_cpu = 0
                elif u_cpu > 100:
                    u_cpu = 100

                print("TotalCpu = " + str(cpu), ", targetCpu = " + str(u_cpu))
                fileUtils.write_file(self.logFileName, str(u_cpu) + "\t" + str(cpu))
                #添加折线图数组数据
                self.data1.append(cpu)
                self.data2.append(u_cpu)

                # self.data_queue.put_nowait([DataCollection.getCurrentTime(), cpu, u_cpu])
                return True
        except Exception as E:
            self.pid = self._getPidByPkg()
            print(E)
            return False

    # idle和totalCpu是累计量，计算出1s内总的cpu增长值和用户占用增长值再相除得比例
    def __getTargetCpuRate(self):
        try:
            totalCpu, idle = self.__getTotalCpuAndIdle()
            u, s, cu, cs = self.__get_u_s_time()
            usercpu = u + s + cu + cs

            if self.isFirst:
                self.isFirst = False
                self.last_totalCpu = totalCpu
                self.last_idle = idle
                self.last_userCpu = usercpu
            elif totalCpu >= 0 and idle >= 0 and usercpu >= 0:

                t_cpu = totalCpu - self.last_totalCpu
                i_idle = idle - self.last_idle
                u_cpu = usercpu - self.last_userCpu

                self.last_idle = idle
                self.last_totalCpu = totalCpu
                self.last_userCpu = usercpu

                userCpuRate = 100 * u_cpu / (t_cpu + i_idle)

                #保留2位小数
                u_cpu = round(userCpuRate, 2)

                if u_cpu < 0:
                    u_cpu = 0
                elif u_cpu > 100:
                    u_cpu = 100

                # self.data_queue.put_nowait([DataCollection.getCurrentTime(), u_cpu, 0])
                print("userCpu = " + str(u_cpu))

                if self.logFileName != "":
                    fileUtils.write_file(self.logFileName, str(u_cpu))
        except EOFError as E:
            print(E)

    def __getCpuByTop(self):
        cmd = 'top -o PID -o RES -o SHR -o CMDLINE -s 2 -n 1'

        pi = self.tools.shell_pi(cmd)

        for line in iter(pi.stdout.readline, ''):

            try:
                target_line = str(line, encoding='utf-8').strip()

                if 'cpu' in target_line and 'user' in target_line:
                    arr = target_line.split()

                    cpu = arr[1].rstrip('%user')

                    fileUtils.write_file(self.logFileName, str(cpu) + "\n")

                    return
            except Exception as e:
                print(e)

                self.pid = self._getPidByPkg()


    def __getTotalCpuRate(self):
        try:
            totalCpu, idle = self.__getTotalCpuAndIdle()

            if self.isFirst:
                self.isFirst = False
                self.last_totalCpu = totalCpu
                self.last_idle = idle
            elif totalCpu >= 0 and idle >= 0 :

                t_cpu = totalCpu - self.last_totalCpu
                i_idle = idle - self.last_idle

                self.last_idle = idle
                self.last_totalCpu = totalCpu

                totalCpuRate = 100 *  t_cpu / (t_cpu + i_idle)

                #保留2位小数
                cpu = round(totalCpuRate, 2)

                if cpu < 0:
                    cpu = 0
                elif cpu > 100:
                    cpu = 100

                print("TotalCpu = " + str(cpu))
                self.data_queue.put_nowait([DataCollection.getCurrentTime(), cpu, 0])

                if self.logFileName != "":
                    fileUtils.write_file(self.logFileName, str(cpu))

        except EOFError as E:
            print(E)

    def start(self, logName = ""):
        self.switch = True

        self.data1=[]
        self.data2=[]

        if not logName == "":
            self.logFileName = logName

            if not self.logFileName.endswith('.txt'):
                self.logFileName = self.logFileName + '_cpu.txt'

            fileUtils.clean_file(self.logFileName)

        if not self.isStart:
            self.isFirst = True
        else:
            print('Thread is start! What would you want to do?')
            return

        t1 = None

        if self.type == 1:
            t1 = threading.Thread(target=self.__looper_cpuRate)
        elif self.type == 2:
            t1 = threading.Thread(target=self.__looper_cpuTime)
        elif self.type == 3:
            t1 = threading.Thread(target=self.__looper_totalCpuRate)
        elif self.type == 4:
            t1 = threading.Thread(target=self.__looper_targetCpuRate)
        elif self.type == 5:
            t1 = threading.Thread(target=self.__looper_getCpuByTop)

        t1.start()

    def end(self, name = ""):
        # if self.data_queue is None or self.data_queue.qsize() == 0:
        #     print("Queue's is empty! Don't countiue")
        #     return

        self.switch = False
        # if self.type == 2:
        #     self.makeChart(6, name)
        # elif self.type == 1:
        #     self.makeChart(1, name)
        # else:
        #     self.makeChart(7, name)

        self.isStart = False

        #画折线图
        if not name=='':
            self.bar = Line(name, "统计如下")  # 主副标题
            t = np.linspace(1, len(self.data1), len(self.data1))  # 等间隔取值
            if len(self.data2)>10:
                self.bar.add("整机cpu占用", t, self.data1, mark_line=["average"], mark_point=["max", "min"])
                self.bar.add("应用cpu占用", t, self.data2, mark_line=["average"], mark_point=["max", "min"])
            else:
                self.bar.add("整机cpu", t, self.data1, mark_line=["average"], mark_point=["max", "min"])
            self.bar.render(r"%s.html" % (name))  # 保存到本地bokezhexiantu.html
        self.data1=[]
        self.data2=[]

    #循环获取cpu占用率
    def __looper_cpuRate(self):

        while self.switch:
            try:
                result = self.__getCpuRate()

                if result:
                    time.sleep(2)
                else:
                    continue
            except Exception as e:
                print(e)

    # 循环获取总的cpu占用率
    def __looper_totalCpuRate(self):

        while self.switch:
            try:
                self.__getTotalCpuRate()
            except EOFError as E:
                print(E)

            time.sleep(0.5)

    # 循环获取总的cpu占用率
    def __looper_targetCpuRate(self):

        while self.switch:
            try:
                self.__getTargetCpuRate()
            except EOFError as E:
                print(E)

            time.sleep(1)

    def __looper_getCpuByTop(self):

        while self.switch:
            try:
                self.__getCpuByTop()
            except EOFError as E:
                print(E)

            time.sleep(2)

    #循环获取cpu占用时长
    def __looper_cpuTime(self):

        while self.switch:
            self.__getCpuUsedTime()
            time.sleep(5)
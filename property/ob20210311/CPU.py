import sys
import threading
import re
import time
import subprocess
import numpy as np
from pyecharts import Line


class CPU(object):

    #type用来区分获取的是cpu占用时长还是cpu占用率, 1是cpu占用率，2是cpu占用时长
    def __init__(self, pidname,devices):

        self.pidname=pidname
        self.devices=devices
        self.pid=""
        self.last_idle = 0
        self.last_totalCpu = 0
        self.last_userCpu = 0

        self.last_userTime = 0

        self.logFileName = ""
        self.isStart = False
        self.isFirst = True
        self.cpu_file=None

        #初始化折线图数据数组
        self.data1=[]
        self.data2=[]

        #折线图标题
        self.chart_title=""
        self.chart_subtitle=u"统计如下"

        self.vm_file=None
        self.pid = self.getpid()

    def getpid(self):
        '''
        获取进程的pid
        '''
        try:
            pid = subprocess.Popen(["adb", "-s",self.devices,"shell", "pgrep",self.pidname], stdout=subprocess.PIPE)
            out, err = pid.communicate() 
            out_info = out.decode('unicode-escape') 
            return out_info.strip()
        except Exception as E:
            print(E)

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

        select_command="/proc/%s/stat"%(self.pid)
        pidstat= subprocess.Popen(["adb", "-s",self.devices,"shell", "cat",select_command], stdout=subprocess.PIPE)
        out, err = pidstat.communicate() 
        output = out.decode('unicode-escape')

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

            pidstat= subprocess.Popen(["adb", "-s",self.devices,"shell", "cat","/proc/stat | grep cpu"], stdout=subprocess.PIPE)
            out, err = pidstat.communicate() 
            output = out.decode('unicode-escape')

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
                self.pid = self.getpid()
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
                self.cpu_file.write(str(cpu) + "\t" + str(u_cpu)+"\n")
                self.cpu_file.flush()
                #添加折线图数组数据
                self.data1.append(cpu)
                self.data2.append(u_cpu)

                return True
        except Exception as E:
            self.pid = self.getpid()
            print(E)
            return False


    def start(self, logName = ""):
        self.switch = True

        if logName=="":
            self.logFileName=self.pidname
        else:
            self.logFileName=logName
        self.chart_title=self.logFileName+"_Cpu"
        #新建文件
        self.cpu_file=open(self.logFileName+"_Cpu.txt","w")

        t1 = threading.Thread(target=self.__looper_cpuRate)

        t1.start()

    def end(self, name = ""):

        self.switch = False

        self.isStart = False

        #画折线图
        # 折线图数据汇总
        self.data1_desc = u'total cpu'
        self.data2_desc = u'target cpu'
        self.data_desc = [self.data1_desc, self.data2_desc]
        self.line_chart(self.data_desc,self.data1,self.data2)

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

    def line_chart(self,data_desc,*datalist):
        '''
        折线图数据处理
        '''
        self.bar = Line(self.chart_title, self.chart_subtitle)  # 主副标题
        for data ,desc in zip(datalist,data_desc):
            if len(data)>0:
                t = np.linspace(1, len(data), len(data))
                self.bar.add(desc, t, data, mark_line=["average"], mark_point=["max"])
        self.bar.render(r"%s.html" % (self.chart_title))  


if __name__ == "__main__":
    cpu = CPU("translationserv","")
    cpu.start()
    for i in range(0,20):
        print("11111111")
        time.sleep(1)
    cpu.end()
import subprocess
import time
import threading
import numpy as np
from pyecharts import Line


class Memory(object):

    def __init__(self,pidname,devices):

        self.pidname=pidname#监控的进程名
        self.devices=devices
        self.iscontinue=True
        self.vm_file = None#写入文件名
        self.isclose=False
        #折线图标题
        self.chart_title=""
        self.chart_subtitle=u"统计如下"
        #初始化折线图数据数组
        self.data1=[]
        self.data2=[]
        self.data3=[]
        self.datalist = [self.data2,self.data3]

        self.data1_desc=''
        self.data2_desc = ''
        self.data3_desc = ''

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

    def getPidVm(self):
        '''
        获取进程的虚拟内存与物理内存
        '''
        try:
            pid=self.getpid()
            select_command="/proc/%s/status"%(pid)
            pidstatus= subprocess.Popen(["adb", "-s",self.devices,"shell", "cat",select_command], stdout=subprocess.PIPE)
            out, err = pidstatus.communicate() 
            out_info = out.decode('unicode-escape')
            lines = []
            lines = out_info.strip().split('\n')
            VmSize=lines[13][7:].strip().split(" ")[0].strip()
            VmRSS=lines[17][7:].strip().split(" ")[0].strip()

            VmSize = round(int(VmSize) / 1024, 2)#MB
            VmRSS = round(int(VmRSS) / 1024, 2)#MB
            MemAvailable=self.getTotalVm()
            fd_num=self.getPidFd()
            self.vm_file.write(str(VmSize)+"\t"+str(VmRSS)+"\t"+MemAvailable+"\t"+fd_num+"\n")
            self.vm_file.flush()
            print(VmSize)#VmPeak: 
            print(VmRSS)#VmSize:
            print(MemAvailable)#MemAvailable:
            #添加折线图数组数据
            #self.data1.append(str(VmSize))
            self.data2.append(str(VmRSS))
            self.data3.append(str(MemAvailable))

        except Exception as E:
            print(E)

    def getPidFd(self):
        '''
        获取程序句柄数量
        '''
        pid = self.getpid()
        select_command = "ls -l /proc/%s/fd |wc -l" % (pid)
        fd_num = subprocess.Popen(["adb", "-s", self.devices, "shell", select_command],stdout=subprocess.PIPE)
        out, err = fd_num.communicate()
        out_info = out.decode('unicode-escape')
        lines = out_info.strip().split('\n')
        return str(lines)

    def getTotalVm(self):
        '''
        获取剩余内存
        '''
        try:
            pid=self.getpid()
            select_command="/proc/meminfo"
            pidstatus= subprocess.Popen(["adb", "-s",self.devices,"shell", "cat",select_command], stdout=subprocess.PIPE)
            out, err = pidstatus.communicate() 
            out_info = out.decode('unicode-escape')
            lines = []
            lines = out_info.strip().split('\n')
            MemFree=lines[1][8:].strip().split(" ")[0].strip()
            MemAvailable=lines[2][13:].strip().split(" ")[0].strip()

            MemFree = round(int(MemFree) / 1024, 2)#MB
            MemAvailable = round(int(MemAvailable) / 1024, 2)#MB

            return str(MemAvailable)


        except Exception as E:
            print(E)

    def looper_vm(self):
        '''
        循环执行命令获取内存值
        '''
        while self.iscontinue:
            self.getPidVm()
            time.sleep(1)
        self.isclose=True

    def start(self,filename=""):
        '''
        开启监控线程
        '''
        if filename=="":
            filename=self.pidname
        self.chart_title=filename+"_Memory"
        #新建文件
        self.vm_file=open(filename+"_mem.txt","w")

        #开启线程
        t1 = threading.Thread(target=self.looper_vm)
        t1.start()

    def end(self):
        '''
        关闭监控线程
        '''
        self.iscontinue=False
        if(self.isclose):
            self.vm_file.close()
        
        # 折线图数据汇总
        #self.data1_desc = u'虚拟内存'
        self.data2_desc = u'物理内存'
        self.data3_desc = u'剩余内存'
        self.data_desc = [self.data2_desc, self.data3_desc]
        self.line_chart(self.data_desc,self.data2,self.data3)
        #清空数组
        self.data1=[]
        self.data2=[]
        self.data3=[]


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
    mem = Memory("translationserv","")
    mem.start()
    for i in range(0,20):
        print("11111111")
        time.sleep(1)
    mem.end()


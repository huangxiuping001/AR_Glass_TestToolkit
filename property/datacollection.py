# -*- coding: utf-8 -*-

from utils.adbtools import AdbTools
from abc import ABCMeta, abstractmethod
from queue import Queue
import plotly.offline as plotoff
import plotly.graph_objs as go
import time

class DataCollection(object):
    __metaclass__ = ABCMeta

    def __init__(self, packageName='', deviceId=''):

        self.packageName = packageName
        self.isFirst = True              # 标记各子类模块是否是第一次收集
        self.isStart = False             # 标记各线程是否正在执行
        self.tools = AdbTools(deviceId)

        self.pid = self._getPidByPkg()

        #存储数据的FIFO队列，队列中每个元素都是一个列表元素，格式为['time', 'value1', 'value2']
        #像fps这些只有一个value的性能项列表的value2为0，像流量这种有上传和下载流量的，value1/value2都有值
        self.data_queue = Queue()

        #开关，各内部循环是用while写的，循环结束的标志就是 switch = False
        self.switch = True
        pass

    def _getPidByPkg(self):
        return self.tools.get_pid(self.packageName)

    #开启性能监控的方法
    @abstractmethod
    def start(self):
        pass
    
    #关闭性能监控并生成图表的方法
    @abstractmethod
    def end(self, name):
        pass

    @abstractmethod
    def endAndSave(self, product, rom_version, scene, process):
        pass

    #生成折线图
    #type用于区分各性能项
    #1：cpu，2：memory，3：battery，4：fps，5：netflow，6：utime，stime
    #name为生成图表的名称
    def makeChart(self, type, name):
        dataset = {
            'time' : [],
            'value_1' : [],
            'value_2' : []
        }

        data_list = self.data_queue

        i = 1
        #构造数据集
        while not data_list.empty():
            data = data_list.get()

            # 纵坐标可以选择使用时间或者次数， data[0]中记录的是时间，i 记录的是次数
            #dataset['time'].append(data[0])
            dataset['time'].append(i)
            dataset['value_1'].append(data[1])
            dataset['value_2'].append(data[2])
            i = i + 1

        title2 = ''
        #根据type命名title1，目前只有流量的title2有值
        if type == 1:
            title1 = 'TotalCpu'
            title2 = 'ProcessCpu'
        elif type == 2:
            title1 = 'TotalPss'
            title2 = 'ProcessPss'
        elif type == 3:
            title1 = 'Battery'
        elif type == 4:
            title1 = 'Fps'
        elif type == 5:
            title1 = 'ReceiveNetflow'
            title2 = 'SendNetflow'
        elif type ==6:
            title1 = 'CpuOccupyTime'
        elif type == 7:
            title1 = 'Cpu'
        elif type == 8:
            title1 = "Pss"
        else:
            title1 = ''

        self.__getChart(name, dataset, title1, title2)
    
    #生成折线图
    #chartname：生成图表的名称
    #dataset：对应性能项的数据集
    #title1/title2：对应性能项y轴的名称，x轴恒为time
    def __getChart(self, chart_name, dataset, title1, title2):
        if title1 == '' and title2 == '':
            print("what just happen?")
            return

        data_gra = []

        #构造关系数据
        relation1 = go.Scatter(
            x = dataset['time'],
            y = dataset['value_1'],
            name = title1
        )
        #加入一条折线
        data_gra.append(relation1)

        #像流量这种有2个value参数的会生成2条折线
        if not title2 ==  '':
            relation2 = go.Scatter(
                x = dataset['time'],
                y = dataset['value_2'],
                name = title2
            )
            data_gra.append(relation2)

        #命名y轴，是流量的话用netflow统称，其他的跟title1一致
        if title1 == 'ReceiveNetflow':
            yname = 'NetFlow'
        elif title1 == 'TotalCpu':
            yname = 'CpuRate'
        elif title1 == 'TotalPss':
            yname = "Pss"
        else:
            yname = title1

        #设置图表布局   图标顶部的title可以自定义，通过改变下面title参数即可
        layout = go.Layout(title="Diagram",
            xaxis={'title': 'time'}, yaxis={'title': yname})
        fig = go.Figure(data = data_gra, layout = layout)

        if  chart_name == '':
            chart_name = "testcase.html"

        if '.html' not in chart_name:
            chart_name = chart_name + ".html"
        #生成离线html-本地html文件
        plotoff.plot(fig, filename = chart_name, auto_open = False)   # 可以设置图表绘制好后是否自动在浏览器中打开

    # 公共方法，获取当前时间，精确到秒
    @staticmethod
    def getCurrentTime():
        return time.strftime('%H:%M:%S')
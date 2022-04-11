# -*- coding: utf-8 -*-

from property.datacollection import DataCollection
import threading
import time

class NetFlow(DataCollection):

    def __init__(self, pkgName = '', deviceId = ''):
        super(NetFlow, self).__init__(pkgName, deviceId)
        self.uid = self.tools.get_uid(self.pid)
        self.last_rcv = 0
        self.last_snd = 0

    def start(self):
        if not self.isStart:
            self.isFirst = True
        else:
            print('Thread is start! What would you want to do?')
            return

        t1 = threading.Thread(target=self.__looper)
        t1.start()
        pass

    def __getNetFlowData(self):
        #获取上传和下载流量值，单位是B
        tcp_rcv, tcp_snd = self.tools.get_flow_data_tcp(self.uid)

        if tcp_rcv == None or tcp_snd == None:
            print("get netflow failed!")
            return
        tcp_rcv = int(tcp_rcv)
        tcp_snd = int(tcp_snd)

        if self.isFirst:
            self.isFirst = False
            self.last_rcv = tcp_rcv
            self.last_snd = tcp_snd
        else:
            rcv = tcp_rcv - self.last_rcv
            snd = tcp_snd - self.last_snd

            #从B转换为M
            rcv = (rcv / 1024) / 1024
            rcv = round(rcv, 2)

            snd = (snd /1024) /1024
            snd = round(snd, 2)

            #数据存储
            self.data_queue.put_nowait([DataCollection.getCurrentTime(), rcv, snd])

            self.last_rcv = tcp_rcv
            self.last_snd = tcp_snd
        pass

    def end(self, name):
        if self.data_queue is None or self.data_queue.qsize() == 0:
            print("Queue's size is zero! Don't countiue")
            return

        self.switch = False

        self.makeChart(5, name)

        self.isStart = False
        pass

    def __looper(self):
        while self.switch:
            self.__getNetFlowData()
            time.sleep(1)
        pass
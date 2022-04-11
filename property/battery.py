# -*- coding: utf-8 -*-

from property.datacollection import DataCollection
import threading
import re
import time

class Battery(DataCollection):

    def __getBattery(self):
        try:
            output = self.tools.shell("dumpsys battery | findstr level").read()
            print(output)
            
            battery_count = re.sub("\D", "", output)
            battery_count = int(battery_count)
            print(str(battery_count))
            self.data_queue.put_nowait([DataCollection.getCurrentTime(), battery_count, 0])
        except EOFError as E:
            print(E)

    def start(self):
        if not self.isStart:
            self.isFirst = True
        else:
            print('Thread is start! What would you want to do?')
            return

        t1 = threading.Thread(target=self.__looper)
        t1.start()
        pass

    def end(self, name):
        if self.data_queue is None or self.data_queue.qsize() == 0:
            print("Queue's size is zero! Don't countiue")
            return

        self.switch = False

        self.makeChart(3, name)

        self.isStart = False
        pass
    
    def __looper(self):
        while self.switch:
            self.__getBattery()
            time.sleep(1)
        pass
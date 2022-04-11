# -*- coding: utf-8 -*-
import datetime

from property.datacollection import DataCollection
import re
import time
import threading

from utils.filetools import fileUtils

class FPS(DataCollection):
    def __init__(self, packageName='', deviceId=''):
        super(FPS, self).__init__(packageName, deviceId)

        self._start_timestamp = 0
        self._end_timestamp = 0

        self.data_list = []

        self.fileName = ''
        self.pi = None
        self.limitProcess = True


    def start(self, fileName = '', limitProcess = True):
        self.fileName = fileName
        self.limitProcess = limitProcess

        if not self.isStart:
            self.isFirst = True
        else:
            print('Thread is start! What would you want to do?')
            return

        p = self.tools.shell('logcat -c')
        p.close()

        self.__startToCollect()

        self._start_timestamp = self.__get_time_from_devices()

        fileUtils.clean_file(self.fileName)
        fileUtils.clean_file(self.fileName.split('.')[0] + '_tmp.txt')

    def end(self, name=''):
        self._end_timestamp = self.__get_time_from_devices()

        print("startTime = %s, endTime = %s"%(str(self._start_timestamp), str(self._end_timestamp)))

        self.switch = False
        self.pi.terminate()

        self.isStart = False

        self.__dealData()

    def _get_fps_data(self):
        try:
            self.pi = self.tools.shell_pi("logcat -v time Choreographer:I *:S")

            for line in iter(self.pi.stdout.readline, ''):

                line = str(line, encoding='utf-8').strip()
                print(line)

                if line.strip() == '':
                    continue

                if self.fileName != "":
                    fileUtils.write_file(self.fileName.split('.')[0] + "_tmp.txt",
                                         line)

                if self.switch is False:
                    self.pi.stdout.close()
                    self.pi.terminate()
                    return

                '''该行不是丢帧日志'''
                if 'Choreographer' not in line:
                    continue

                '''不是目标进程丢的帧'''
                if self.limitProcess:
                    if self.pid != self.get_pid_from_log_line(line):
                        print("pid is %s, not equal!"%(self.pid))
                        continue

                current_timestamp = int(self.get_timestamp_from_line(line))
                skipped_frame = int(self.get_skiped_frame(line))

                self.data_list.append(FPSParams(current_timestamp, skipped_frame))

        except Exception as e:
            print(e)

            self.pid = self._getPidByPkg()

    def __dealData(self):
        print("deal data")

        result_list = []

        if len(self.data_list) == 0:
            print("Queue is empty!")

            for i in range(self._start_timestamp, self._end_timestamp):
                result_list.append(FPSParams(i, 0))

        for item in self.data_list:

            print(str(item))

            if item.get_time() < self._start_timestamp:
                continue

            if item.get_time() > self._end_timestamp:
                break

            if len(result_list) == 0:
                for stamp in range(int(self._start_timestamp), int(item.get_time())):
                    result_list.append(FPSParams(stamp, 0))

                result_list.append(item)

            if (item.get_time()-result_list[-1].get_time()) >= 1:
                for i in range(result_list[-1].get_time() + 1, item.get_time()):
                    result_list.append(FPSParams(i, 0))

                result_list.append(item)
            elif item.get_time() < result_list[-1].get_time():
                continue
            elif item.get_time() == result_list[-1].get_time():

                result_list[-1].set_data(result_list[-1].get_data() + item.get_data())

            index = len(result_list)-1
            print("len = " + str(index))

            while result_list[index].get_data() > 60:

                surplus = result_list[index].get_data() - 60

                result_list[index].set_data(60)
                index -= 1

                if index == -1:
                    break

                result_list[index].set_data(result_list[index].get_data() + surplus)

        if len(result_list) == 0:
            print("Has no skipped frame!")
            return

        if result_list[-1].get_data() < self._end_timestamp:
            for i in range(int(result_list[-1].get_time())+1, int(self._end_timestamp)+1):
                print("add timestramp = " + str(i))
                result_list.append(FPSParams(i, 0))

        print(str(result_list))

        if self.fileName != "":
            print("write file")
            for param in result_list:
                fileUtils.write_file(self.fileName, str(param.get_time()) + '\t' + str(param.get_data()))

            fileUtils.write_file(self.fileName, 'end')

    '''从单行中取出pid'''
    def get_pid_from_log_line(self, line):
        pid = re.sub(r'\D', " ", line).split()[6]

        print("pid from line is " + str(pid))
        return pid

    '''获取行中的丢帧数'''
    def get_skiped_frame(self, line):
        skipped_frame = re.sub(r'\D', " ", line).split()[7]
        return skipped_frame

    '''根据完整日期获取时间戳'''
    def get_timestamp_from_date(self, date):
        timeArray = time.strptime(date, "%Y-%m-%d %H:%M:%S")

        timestampe = time.mktime(timeArray)
        return str(int(timestampe))

    '''根据时间获取一行中的时间戳'''
    def get_timestamp_from_line(self, line):
        params = line.split()
        years = str(datetime.datetime.now().year)

        str_time = years + '-' + params[0] + ' ' + params[1].split('.')[0]

        return self.get_timestamp_from_date(str_time)

    '''获取设备时间'''
    def __get_time_from_devices(self) -> int:
        cmd = "date +%s"
        pi = self.tools.shell(cmd)

        time = str(pi.readline())
        return int(time)

    def __startToCollect(self):
        t = threading.Thread(target=self._get_fps_data)
        t.setDaemon(True)
        t.start()

class FPSParams(object):

    def __init__(self, str_time = 0, data = 0):
        self.str_time = str_time
        self.data = data

    def get_time(self):
        return self.str_time

    def get_data(self) -> int:
        return self.data

    def set_data(self, data):
        self.data = data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.str_time == other.str_time
        else:
            return False

    def __str__(self):
        return "timestamp = %s, skippedFrame = %s" % (self.str_time, self.data)

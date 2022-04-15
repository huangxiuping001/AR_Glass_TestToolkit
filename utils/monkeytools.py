# -*- coding: utf-8 -*-
import datetime
import os
import pathlib
import random
import re
import time
import unittest
from configparser import ConfigParser

from utils.adbtools import AdbTools

deviceId = '3b750eee'

configFileName = 'config.ini'

class MonkeyTools(unittest.TestCase):

    config = ConfigParser()

    def setUp(self) -> None:
        if not pathlib.Path(configFileName).exists():
            self.config['MonkeyTools'] = {'shutDown': 'True'}

            with open(configFileName, 'w') as configfile:
                self.config.write(configfile)
        else:
            if not 'MonkeyTools' in self.config:
                self.config['MonkeyTools'] = {'shutDown': 'True'}

                with open(configFileName, 'w') as configfile:
                    self.config.write(configfile)

    def tearDown(self) -> None:
        pass

    def test_startMonkey(self):
        MonkeyTools.starMonkey(monkey_cmd = '-p com.iflytek.easytrans.launcher -s %s -v 10000000 >D:/%s_%s_monkey.txt'%
                               (str(random.randint(0, 10000)), deviceId, datetime.date.today().strftime('%m%d')))

    def test_stopMonkey(self):
        MonkeyTools.stopMonkey()

    @staticmethod
    def starMonkey(monkey_cmd = '-p packageName -s 1224 -v 100000 >D:/monkey.txt'):
        '''
        :param monkey_cmd: monkey命令后面的字符串
        :return: None
        '''
        MonkeyTools.__setConfig(False)

        tools = AdbTools(deviceId)
        params = ['--monitor-native-crashes', '--hprof', '--bugreport']

        # 自动补全关键参数
        for param in params:
            if param not in monkey_cmd:
                monkey_cmd = param + ' ' + monkey_cmd

        tools.adb('logcat -c').close()

        i = -1
        while not MonkeyTools.__getConfig():
            i += 1

            startTime = time.time()
            print(str(i) + "th start, time = " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

            if i != 0:
                # 非第一次循环会更换随机种子seed
                monkey_cmd = MonkeyTools.__getRandomSeed(monkey_cmd)

            cmd = 'monkey %s' % (monkey_cmd)

            # 输出文件名添加编号
            if '>' in cmd:
                cmd = cmd.rstrip('.txt') + '_' + str(i) + '.txt'

            print("cmd = " + cmd)

            tools.shell(cmd).close()

            endTime = time.time()
            print(str(i) + "th end, time = " + time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))

            if MonkeyTools.__getConfig():
                print('------------ monkey end ------------')
                return

            if (endTime - startTime) < 5:
                print('------------Monkey command maybe occur error, check it!------------')
                return

            MonkeyTools.__reboot()

    @staticmethod
    def stopMonkey():
        '''
        停止monkey通用工具封装，cmd里启起来的monkey也可以停
        '''
        MonkeyTools.__setConfig(True)

        tools = AdbTools(deviceId)
        pi = tools.shell('ps | findstr monkey')
        line = pi.readline()
        pi.close()

        if line:
            monkey_pid = re.sub(r'\D', " ", line).split()[0]
            print("monkey pid is %s"%(monkey_pid))
            tools.shell('kill -9 %s' % (monkey_pid)).close()
        else:
            print("has no monkey process")

    @staticmethod
    def __getRandomSeed(cmd):

        temp = cmd.split('-s')

        right_str = temp[1].split()

        result = str(random.randint(0, 10000))
        for i in range(1, len(right_str)):
            result += (' ' + right_str[i])

        cmd = temp[0] + '-s ' + result

        return cmd

    @staticmethod
    def __reboot():
        print('reboot devices %s\n'%(deviceId))
        os.system('adb -s %s reboot'%(deviceId))

        time.sleep(70)

    @staticmethod
    def __getConfig():
        MonkeyTools.config.read(configFileName)

        return MonkeyTools.config['MonkeyTools']['shutDown'] == 'True'

    @staticmethod
    def __setConfig(st=False):
        MonkeyTools.config.read(configFileName)

        MonkeyTools.config.set('MonkeyTools', 'shutDown', str(st))

        with open(configFileName, 'w') as f:
            MonkeyTools.config.write(f)
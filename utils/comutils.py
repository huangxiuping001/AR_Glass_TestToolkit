import os
import random
import time


class ComUtils:

    def __init__(self):
        pass

    @staticmethod
    def installApkAndStart(devicesId = "", apk_path = "E:\python_home\translator__android__test_toolkit\apk\speechDemo_old.apk",
                           package = 'com.iflytek.voicedemo/.MainActivity'):
        try:
            cmd = "adb -s %s install %s"%(devicesId, apk_path)

            os.system(cmd)

            os.system("adb shell am start %s"%(package))

        except Exception as e:
            print(e)

    @staticmethod
    def sleepRandomTime(min_limit = 0, max_limit = 10):
        t = random.randint(min_limit, max_limit)

        time.sleep(t)
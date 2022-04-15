import os
from time import sleep
from utils import get_device_info
from utils.get_device_info import *
from utils.adb_util import *

class Operations(object):


    def __init__(self,devices):
        #global device
        print("333333333333333333")
        self.device = get_device_info.get_device_connect(devices)
        self.deviceID=devices
        print("44444444444444444444")
        #device= self.device

    def installSpeechDemo(self, demoPath = ''): #安装音频demo APK
        if self.deviceID:
            cmd = 'adb -s %s install -r -t -d %s'%(self.deviceID, demoPath)
        else:
            cmd = 'adb install -r -t -d %s' % (demoPath)

        print('install apk, package = ' + cmd)
        os.system(cmd)

    # -------------------------------------------------检查屏幕状态
    def BrightScreen(self):
        powervalue1 = "Display Power: state=OFF"
        powervalue2 = "Display Power: state=ON"
        print("BrightScreen"+self.deviceID)
        result = os.popen('adb -s %s shell dumpsys power | findstr Display'%(self.deviceID)).readlines()
        if powervalue1 in result[5]:
            cmd = 'adb -s %s shell input keyevent 26'%(self.deviceID)
            os.system(cmd)
            print('=============触发亮屏==============')
        else:
            print('============屏幕已处于亮屏状态===============')
    #-------------等待设备
    # def wait_for_device(self):
    #     self.adb_stdout("wait-for-device")
    #
    #     self.adb_stdout("root")
        sleep(1)

    def StartVoicedemo(self):
        """启动音频合成软件
        """
        if self.deviceID:
            cmd = "adb -s %s shell am start -n  com.iflytek.voicedemo/com.iflytek.voicedemo.MainActivity" % (self.deviceID)
        else:
            cmd = "adb shell am start -n com.iflytek.voicedemo/com.iflytek.voicedemo.MainActivity"

        os.system(cmd)

    def PlayAudio(self, speechfile, speechfloder):
        # 播放音频文件
        if self.deviceID:
            cmd = 'adb -s %s shell am broadcast -a NEW_REDIOPLAY --es name %s --es path %s' % (
            self.deviceID, speechfile, speechfloder)
        else:
            cmd = 'adb shell am broadcast -a NEW_REDIOPLAY --es name %s --es path %s' % (speechfile, speechfloder)
        print(cmd)
        os.system(cmd)

    @staticmethod
    def input_pover_key():
        """
        短按电源键
        :return:
        """
        cmd = "adb shell input keyevent 26"
        os.system(cmd)

    @staticmethod
    def input_long_power_key():
        """
        长按电源按键
        :return:
        """
        cmd = "adb shell input keyevent --longpress 26"
        os.system ( cmd )

    @staticmethod
    def input_long_key(event_num,event_key,time):
        """

        :param event_num:   电源键 :event_num 0,event_key 64,
                            红键:event_num 3,event_key 64,
                            白键:event_num 0,event_key 63,
                            BACK键:event_num 0,event_key 60
        :param event_key:
        :param time:
        :return:
        """
        '''方法一
        cmd = "adb shell input keyevent --longpress 26"
        os.system(cmd)
        '''
        #方法二
        cmd1 = 'adb shell sendevent /dev/input/event%s 1 %s 1' %(event_num,event_key)
        cmd2 = 'adb shell sendevent /dev/input/event%s 1 %s 0' %(event_num,event_key)
        cmd3 = 'adb shell sendevent /dev/input/event%s 0 0 0' %event_num
        os.system(cmd1)
        os.system(cmd3)
        sleep(time)
        os.system(cmd2)
        os.system(cmd3)


    def input_back_key(self):
        """
        按下返回键
        :return:
        """
        cmd = "adb -s %s shell input keyevent 4"%(self.deviceID)
        os.system ( cmd )


    def input_long_back_key(self):
        """
        按下返回键
        :return:
        """
        cmd = "adb  -s %s shell input keyevent --longpress 4"%(self.deviceID)
        os.system ( cmd )

    @staticmethod
    def back_home():
        """
        按下HOME键
        :return:
        """
        cmd = "adb shell am broadcast -a com.iflytek.action.F2.down"
        os.system(cmd)

    @staticmethod
    # -------------------------------------------------查找日志
    def GetAllLog(self, logfile):
        if self.deviceId:
            cmd = 'adb -s %s logcat -d -s "GLOBAL" |grep -E "ocrTrans onSuccess:" > %s' % (self.deviceId, logfile)
        else:
            cmd = 'adb logcat -d -s "GLOBAL" |grep -E "ocrTrans onSuccess:" > %s' % (logfile)

        os.system(cmd)

    @staticmethod
    def GetPerforLog(self, logfile):
        if self.deviceId:
            cmd = 'adb -s %s logcat -d -s "CollectLogger" |grep -E "DripCollectLogger.performLogCollect" > %s' % (
            self.deviceId, logfile)
        else:
            cmd = 'adb logcat -d -s "CollectLogger" |grep -E "DripCollectLogger.performLogCollect" > %s' % (logfile)

            os.popen(cmd)

    @staticmethod
    def KillAdb(self):
        """查询当前进程"""
        if self.deviceId:
            cmd = "adb -s %s kill-server" % (self.deviceId)
        else:
            cmd = "adb kill-server"

        os.system(cmd)

    @staticmethod
    def RemoveLogcat(self):
        """清除日志"""
        if self.deviceId:
            cmd = "adb -s %s logcat -c" % (self.deviceId)
        else:
            cmd = "adb logcat -c"
        os.system(cmd)

    @staticmethod
    def input_red_key():
        """
        按下红键
        :return:
        """
        cmd = "adb shell input keyevent --longpress F5"
        os.system ( cmd )

    @staticmethod
    # 按键抬起---------------
    def KoreaKeyup(self, deviceId=""):
        cmd = "adb -s " + deviceId + " shell am broadcast -a com.iflytek.action.F6.up"
        os.system(cmd)

    @staticmethod
    def input_write_key():
        """
        按下白健
        :return:
        """
        cmd = "adb shell input keyevent --longpress F6"
        os.system ( cmd )

    def ChineseKeydown(self):
        """按下中文录音键
        """
        if self.d:
            cmd = "adb -s %s shell am broadcast -a com.iflytek.action.F6.down" % (self.deviceID)
        else:
            cmd = "adb -s shell am broadcast -a com.iflytek.action.F6.down"
        os.system(cmd)

    def chineseKeyDownNew(self):
        if self.d:
            cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.down -p com.iflytek.easytrans.launcher" % (
                self.d)
        else:
            cmd = "adb shell am startservice -a com.iflytek.action.F6.down -p com.iflytek.easytrans.launcher"
        os.system(cmd)

    @staticmethod
    def chineseKeyDownNew(self):
        if self.d:
            cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.down -p com.iflytek.easytrans.launcher" % (
                self.d)
        else:
            cmd = "adb shell am startservice -a com.iflytek.action.F6.down -p com.iflytek.easytrans.launcher"

        os.system(cmd)

    def chineseKeyDownLB(self):
        # if self.deviceId:
        #     cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.down -p com.iflytek.easytrans.launcher" % (
        #         self.deviceId)
        # else:
        cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.down -p com.iflytek.easytrans.launcher"%(self.deviceID)
        os.system(cmd)

    @staticmethod
    def ChineseKeyup(self):
        """松开中文录音键
        """
        if self.deviceId:
            cmd = "adb -s %s shell am broadcast -a com.iflytek.action.F6.up" % (self.deviceId)
        else:
            cmd = "adb shell am broadcast -a com.iflytek.action.F6.up"

        os.system(cmd)

    @staticmethod
    def chineseKeyUpNew(self):
        if self.deviceId:
            cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.up -p com.iflytek.easytrans.launcher" % (
                self.deviceId)
        else:
            cmd = "adb shell am startservice -a com.iflytek.action.F6.up -p com.iflytek.easytrans.launcher"

        os.system(cmd)


    def chineseKeyUpLB(self):
        # if self.deviceId:
        #     cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.up -p com.iflytek.easytrans.launcher" % (
        #         self.deviceId)
        # else:
        cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.up -p com.iflytek.easytrans.launcher"%(self.deviceID)

        os.system(cmd)

    @staticmethod
    def ForeignKeydown(self):
        """按下外文录音键
        """
        if self.deviceId:
            cmd = "adb -s %s shell am broadcast -a com.iflytek.action.F5.down" % (self.deviceId)
        else:
            cmd = "adb shell am broadcast -a com.iflytek.action.F5.down"
        os.system(cmd)

    @staticmethod
    def foreignKeyDownNew(self):
        if self.deviceId:
            cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.down -p com.iflytek.easytrans.launcher" % (
                self.deviceId)
        else:
            cmd = "adb shell am startservice -a com.iflytek.action.F5.down -p com.iflytek.easytrans.launcher"
        os.system(cmd)

    @staticmethod
    def foreignKeyDownNew(self):
        if self.deviceId:
            cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.down -p com.iflytek.easytrans.launcher" % (
                self.deviceId)
        else:
            cmd = "adb shell am startservice -a com.iflytek.action.F5.down -p com.iflytek.easytrans.launcher"

        os.system(cmd)


    def foreignKeyDownLB(self):
        # if self.deviceId:
        #     cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.down -p com.iflytek.easytrans.launcher" % (
        #         self.deviceId)
        # else:
        cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.down -p com.iflytek.easytrans.launcher"%(self.deviceID)
        os.system(cmd)

    @staticmethod
    def ForeignKeyup(self):
        """松开外文录音键
        """
        if self.deviceId:
            cmd = "adb -s %s shell am broadcast -a com.iflytek.action.F5.up" % (self.deviceId)
        else:
            cmd = "adb shell am broadcast -a com.iflytek.action.F5.up"

        os.system(cmd)

    @staticmethod
    def foreignKeyUpNew(self):
        # if self.deviceId:
        #     cmd = "adb -s %s shell am startservice -a com.iflytek.action.F5.up -p com.iflytek.easytrans.launcher" % (
        #         self.deviceId)
        # else:
        cmd = "adb shell am startservice -a com.iflytek.action.F5.up -p com.iflytek.easytrans.launcher"

        os.system(cmd)


    def foreignKeyUpLB(self):
        # if self.deviceId:
        #     cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.up -p com.iflytek.easytrans.launcher" % (
        #         self.deviceId)
        # else:
        cmd = "adb -s %s shell am startservice -a com.iflytek.action.F6.up -p com.iflytek.easytrans.launcher"%(self.deviceID)

        os.system(cmd)

    @staticmethod
    def input_PAGE_UP():
        """
        按下向上翻页键
        :return:
        """
        cmd = "adb shell input keyevent 93"
        os.system ( cmd )

    @staticmethod
    def input_PAGE_DOWN():
        """
        按下向下翻页键
        :return:
        """
        cmd = "adb shell input keyevent 92"
        os.system (cmd)

    def open_pakage(self,package):
        """
        打开应用
        :param package:传入包名
        :return:
        """
        self.device.app_start(package)


    def close_pakage(self,package):
        """
        关闭应用
        :param package:传入包名
        :return:
        """
        self.device.app_stop ( package )

    def close_all_pakage(self):
        """
        关闭应用
        :param package:传入包名
        :return:
        """
        self.device.app_stop_all ()

    def double_swape_down(self):
        """
        :return:返回音量值
        """
        point1 = (100, 1050)
        point2 = (100, 350)
        point3 = (560, 1050)
        point4 = (560, 350)
        self.device(scrollable= True).gesture(point2,point4,point1,point3)
        voice_value = get_device_info.get_voice_value()
        return voice_value


    def double_swape_up(self):
        """
        :return:返回音量值
        """
        point1 = (100, 1050)
        point2 = (100, 350)
        point3 = (560, 1050)
        point4 = (560, 350)
        self.device( scrollable=True).gesture(point1,point3,point2,point4)
        voice_value = get_device_info.get_voice_value()
        return voice_value


    def double_swape_left(self):
        """
        :return: 返回亮度值
        """
        point1 = (100, 1050)
        point2 = (100, 350)
        point3 = (560, 1050)
        point4 = (560, 350)
        self.device( scrollable=True).gesture(point3,point4,point1,point2)
        screen_value = get_device_info.get_screen_value()
        return screen_value


    def double_swape_right(self):
        """

        :return: 返回亮度值
        """
        point1 = (100, 1050)
        point2 = (100, 350)
        point3 = (560, 1050)
        point4 = (560, 350)
        self.device( scrollable=True).gesture(point1,point2,point3,point4)
        screen_value = get_device_info.get_screen_value()
        return screen_value


    def swape_direction(self,direction):
        """

        :param direction: 左滑left，右滑right
        :return:
        """
        self.device.session().swipe_ext(direction)



    @staticmethod

    # -------------------------------------------------弹出状态栏
    def StatusBar(self):
            cmd = 'adb shell cmd statusbar expand-notifications'
            os.system(cmd)


    def OpenWIFI(self):
        cmd = "adb -s %s shell svc wifi enable"%(self.device)

        os.system(cmd)


    def CloseWIFI(self):
        cmd = "adb -s %s shell svc wifi disable"%(self.device)

        os.system(cmd)

        # -------------------------------------------------发送广播，触发SOS
    def sos(self):
            cmd = 'adb -s %s shell am broadcast -a com.iflytek.easytrans.powerclick5'%(self.device)
            os.system(cmd)

        # -------------------------------------------------查找日志
    def GetAllLog(self, logfile):

        cmd = 'adb logcat -d -s "GLOBAL" |grep -E "ocrTrans onSuccess:" > %s' % (logfile)
        os.system(cmd)

    def GetPerforLog(self, logfile):

        cmd = 'adb logcat -d -s "CollectLogger" |grep -E "DripCollectLogger.performLogCollect" > %s' % (logfile)
        os.popen(cmd)

    def KillAdb(self):
        """查询当前进程"""
        cmd = "adb kill-server"
        os.system(cmd)

        def RemoveLogcat(self):
            """清除日志"""
            cmd = "adb logcat -c"
            os.system(cmd)

        # -----------------------------------------------------发送广播

        def InsertImg(self, imgfile, deviceId=""):
            """查找手机中图片发送广播作为识别图片
            """
            if deviceId is "":
                cmd = "adb shell am broadcast -a get_ocr_img_path_action --es path %s" % (imgfile)
            else:
                cmd = "adb -s %s shell am broadcast -a get_ocr_img_path_action --es path %s" % (deviceId, imgfile)
            os.system(cmd)

            sleep(1)

        def SendSpeech(self, speechfile, speechtype):
            """查找手机中图片发送广播作为识别图片
            """
            cmd = "adb shell am broadcast -a com.iflytek.action.record.trans --es record_path /sdcard1/testspeech/%s --es trans_type %s" % (
                speechfile, speechtype)
            os.system(cmd)


    # -------------------------------------------------弹出状态栏
    def StatusBar(self):
        cmd = 'adb shell cmd statusbar expand-notifications'
        os.system(cmd)

    # -------------------------------------------------发送广播，触发SOS
    def sos(self):
        cmd = 'adb shell am broadcast -a com.iflytek.easytrans.powerclick5'
        os.system(cmd)

    # -------------------------------------------------查找日志
    def GetAllLog(self, logfile):

        cmd = 'adb logcat -d -s "GLOBAL" |grep -E "ocrTrans onSuccess:" > %s' % (logfile)
        os.system(cmd)

    def GetPerforLog(self, logfile):

        cmd = 'adb logcat -d -s "CollectLogger" |grep -E "DripCollectLogger.performLogCollect" > %s' % (logfile)
        os.popen(cmd)

    def KillAdb(self):
        """查询当前进程"""
        cmd = "adb kill-server"
        os.system(cmd)

    def RemoveLogcat(self):
        """清除日志"""
        cmd = "adb logcat -c"
        os.system(cmd)

    # -----------------------------------------------------发送广播

    def InsertImg(self, imgfile, deviceId=""):
        """查找手机中图片发送广播作为识别图片
        """
        if deviceId is "":
            cmd = "adb shell am broadcast -a get_ocr_img_path_action --es path %s" % (imgfile)
        else:
            cmd = "adb -s %s shell am broadcast -a get_ocr_img_path_action --es path %s" % (deviceId, imgfile)
        os.system(cmd)
        sleep(1)

    def SendSpeech(self, speechfile, speechtype):
        """查找手机中图片发送广播作为识别图片
        """
        cmd = "adb shell am broadcast -a com.iflytek.action.record.trans --es record_path /sdcard1/testspeech/%s --es trans_type %s" % (
        speechfile, speechtype)
        os.system(cmd)



# if __name__ == '__main__':
#     # input_PAGE_UP()
#     # doubleswape_right()
#     # doubleswape_left()
#     # doubleswape_up()
#     # doubleswape_down()
#     # input_long_back_key()
#     # input_red_key()
#     # Operations().input_long_power_key(3,64,3)
#     # Operations.input_write_key()
#     # Operations.input_long_power_key()
#     # Operations.input_long_back_key()
#     # Operations().input_long_key(0,64,3)
#     # Operations().double_swape_up()
#     Operations().close_pakage('com.android.settings')


#-*-coding: UTF-8 -*-
"""
Created on 2022年4月2日

@author: admin
"""
import os
import subprocess
import time

from mutagen.mp3 import MP3

class AdbOperate(object):
    '''
    classdocs
    '''

    adbpid=True

    def __init__(self, deviceId = ''):
        '''
        Constructor
        '''
        self.deviceId = deviceId

    def GAPlayAudio(self, playFilePath):
        os.system('adb -s %s shell am broadcast -a com.test.player --es path %s' % (self.deviceId, playFilePath))


#-------------------------------------------------查找日志    
    def GetAllLog(self,logfile):
        if self.deviceId:
            cmd='adb -s %s logcat -d -s "GLOBAL" |grep -E "ocrTrans onSuccess:" > %s'%(self.deviceId, logfile)
        else:
            cmd = 'adb logcat -d -s "GLOBAL" |grep -E "ocrTrans onSuccess:" > %s' % (logfile)

        os.system(cmd)

    def GetPerforLog(self,logfile):
        if self.deviceId:
            cmd = 'adb -s %s logcat -d -s "CollectLogger" |grep -E "DripCollectLogger.performLogCollect" > %s'%(self.deviceId, logfile)
        else:
            cmd = 'adb logcat -d -s "CollectLogger" |grep -E "DripCollectLogger.performLogCollect" > %s' % (logfile)

        os.popen(cmd)

    def KillAdb(self):
        """查询当前进程"""
        if self.deviceId:
            cmd = "adb -s %s kill-server" % (self.deviceId)
        else:
            cmd = "adb kill-server"

        os.system(cmd)


    def reboot(self):
        """查询当前进程"""
        if self.deviceId:
            cmd = "adb -s %s kill-server" % (self.deviceId)
        else:
            cmd = "adb kill-server"

        os.system(cmd)
        
    def RemoveLogcat(self):
        """清除日志"""
        if self.deviceId:
            cmd = "adb -s %s logcat -c" % (self.deviceId)
        else:
            cmd = "adb logcat -c"
        os.system(cmd)

#-----------------------------------------------------发送广播

    def InsertImg(self,imgfile):
        """查找手机中图片发送广播作为识别图片
        """
        if not self.deviceId:
            cmd = "adb shell am broadcast -a get_ocr_img_path_action --es path %s" %(imgfile)
        else:
            cmd = "adb -s %s shell am broadcast -a get_ocr_img_path_action --es path %s" %(self.deviceId, imgfile)

        os.system(cmd)

        time.sleep(1)
        
    def SendSpeech(self,speechfile,speechtype):
        """查找手机中图片发送广播作为识别图片
        """
        if not self.deviceId:
            cmd = "adb shell am broadcast -a com.iflytek.action.record.trans --es record_path /sdcard1/testspeech/%s --es trans_type %s" % (speechfile, speechtype)
        else:
            cmd = "adb -s %s shell am broadcast -a com.iflytek.action.record.trans --es record_path /sdcard1/testspeech/%s --es trans_type %s" %(self.deviceId, speechfile, speechtype)
        os.system(cmd)

    def voiceDownFyb(self):
        if self.deviceId:
            cmd = "adb -s %s shell dbus-send --system --type=signal --dest=com.iflytek.launcher.method.subscriber" \
                  " /com/iflytek/powerkey/signal/subscriber com.iflytek.powerkey.signal.subscriber.voiceDown  string:'70'" % (
                  self.deviceId)
        else:
            cmd = "adb shell dbus-send --system --type=signal --dest=com.iflytek.launcher.method.subscriber" \
                  " /com/iflytek/powerkey/signal/subscriber com.iflytek.powerkey.signal.subscriber.voiceDown  string:'70'"

        os.system(cmd)

    def voice_down_event_FYB(self):
        command = "/mnt/{0}/{1} >>/dev/input/event0".format("voice", "voicedown")
        print("command:{0}".format(command))
        if self.deviceId:
            pidstatus = subprocess.Popen(["adb", "-s", self.deviceId, "shell", "cat", command],
                                         stdout=subprocess.PIPE)
        else:
            pidstatus = subprocess.Popen(["adb", "shell", "cat", command],
                                         stdout=subprocess.PIPE)


    def voice_up_event_FYB(self):
        command = "/mnt/{0}/{1} >>/dev/input/event0".format("voice", "voiceup")
        print("command:{0}".format(command))
        if self.deviceId:
            pidstatus = subprocess.Popen(["adb", "-s", self.deviceId, "shell", "cat", command],
                                         stdout=subprocess.PIPE)
        else:
            pidstatus = subprocess.Popen(["adb", "shell", "cat", command],
                                         stdout=subprocess.PIPE)




    def voice_up_event(self,device):
        command = "/mnt/{0}/{1} >>/dev/input/event0".format("voice", "voiceup")
        print("command:{0}".format(command))
        pidstatus = subprocess.Popen(["adb", "-s", device, "shell", "cat", command],
                                     stdout=subprocess.PIPE)

    def voiceUpFyb(self):
        if self.deviceId:
            cmd = "adb -s %s shell dbus-send --system --type=signal --dest=com.iflytek.launcher.method.subscriber" \
                  " /com/iflytek/powerkey/signal/subscriber com.iflytek.powerkey.signal.subscriber.voiceUp  string:'70'" % (
                  self.deviceId)
        else:
            cmd = "adb shell dbus-send --system --type=signal --dest=com.iflytek.launcher.method.subscriber" \
                  " /com/iflytek/powerkey/signal/subscriber com.iflytek.powerkey.signal.subscriber.voiceUp  string:'70'"

        os.system(cmd)

    def AIUIdown(self):
        """按下AIUI键
        """
        if self.deviceId:
            cmd="adb -s %s shell am broadcast -a com.iflytek.action.F2.down" % (self.deviceId)
        else:
            cmd = "adb shell am broadcast -a com.iflytek.action.F2.down"

        os.system(cmd)

    def backHome(self):
        if self.deviceId:
            cmd = 'adb -s %s shell am broadcast -a com.iflytek.action.F2.home' % (self.deviceId)
        else:
            cmd = 'adb shell am broadcast -a com.iflytek.action.F2.home'

        os.system(cmd)

    def AIUIup(self):
        """松开AIUI键
                """
        if self.deviceId:
            cmd = "adb -s %s shell am broadcast -a com.iflytek.action.F2.up" % (self.deviceId)
        else:
            cmd = "adb shell am broadcast -a com.iflytek.action.F2.up"

        os.system(cmd)

    #----------------------------------------------------------------操作文件夹
        
    def MkFolder(self):
        """新建测试图片文件夹
        """
        if self.deviceId:
            cmd = "adb -s %s shell mkdir /sdcard1/testimg" % (self.deviceId)
        else:
            cmd = "adb shell mkdir /sdcard1/testimg"
        os.system(cmd) 
        
    def PushImg(self,imgfile):
        """向手机传入测试图片
        """
        if self.deviceId:
            cmd = "adb -s %s push %s /sdcard1/testimg" %(self.deviceId, imgfile)
        else:
            cmd = "adb push %s /sdcard1/testimg" %(imgfile)

        os.system(cmd) 
        
    def RomveImg(self):
        """向手机传入测试图片
        """
        if self.deviceId:
            cmd = "adb -s %s shell rm -r /sdcard1/testimg" % (self.deviceId)
        else:
            cmd = "adb shell rm -r /sdcard1/testimg"

        os.system(cmd) 
        
        
    def MkSpeechFolder(self):
        """新建音频文件夹
        """
        if self.deviceId:
            cmd = "adb -s %s shell mkdir /sdcard1/testspeech" % (self.deviceId)
        else:
            cmd = "adb shell mkdir /sdcard1/testspeech"

        os.system(cmd) 
        
    def PushSpeech(self,imgfile):
        """向手机传入测试音频
        """
        if self.deviceId:
            cmd = "adb -s %s push %s /sdcard1/testspeech" %(self.deviceId, imgfile)
        else:
            cmd = "adb push %s /sdcard1/testspeech" % (imgfile)

        os.system(cmd) 
        
    def RomveSpeech(self):
        """向手机传入测试音频
        """
        if self.deviceId:
            cmd = "adb -s %s shell rm -r /sdcard1/testspeech" % (self.deviceId)
        else:
            cmd = "adb shell rm -r /sdcard1/testspeech"

        os.system(cmd)
        
#--------------------------------------------------------
    def installSpeechDemo(self, demoPath = ''):
        if self.deviceId:
            cmd = 'adb -s %s install -r -t -d %s'%(self.deviceId, demoPath)
        else:
            cmd = 'adb install -r -t -d %s' % (demoPath)

        print('install apk, package = ' + cmd)
        os.system(cmd)

    def getMp3Length(self, filePath = ''):
        audio = MP3(filePath)
        return audio.info.length

    def StartVoicedemo(self):
        """启动音频合成软件
        """
        if self.deviceId:
            cmd = "adb -s %s shell am start com.iflytek.voicedemo/.MainActivity" % (self.deviceId)
        else:
            cmd = "adb shell am start com.iflytek.voicedemo/.MainActivity"

        os.system(cmd) 
        
    def StopVoicedemo(self):
        """关闭音频合成软件
        """
        if self.deviceId:
            cmd = "adb -s %s shell am force-stop com.iflytek.voicedemo" % (self.deviceId)
        else:
            cmd = "adb shell am force-stop com.iflytek.voicedemo"

        os.system(cmd)  
        
    def PlayAudio(self,speechfile,speechfloder):
        # 播放音频文件
        if self.deviceId:
            cmd = 'adb -s %s shell am broadcast -a NEW_REDIOPLAY --es name %s --es path %s'%(self.deviceId, speechfile, speechfloder)
        else:
            cmd = 'adb shell am broadcast -a NEW_REDIOPLAY --es name %s --es path %s'%(speechfile, speechfloder)
        print(cmd)
        os.system(cmd)

    def playAudioNew(self, filePath = ''):
        if self.deviceId:
            cmd = 'adb -s %s shell am broadcast -a NEW_REDIOPLAY --es path %s'%(self.deviceId, filePath)
        else:
            cmd = 'adb shell am broadcast -a NEW_REDIOPLAY --es path %s'%(filePath)

        print(cmd)
        os.system(cmd)

    def startAudioTools(self):
        """启动音频合成软件
        """
        if self.deviceId:
            cmd = "adb -s %s shell am start com.iflytek.easytrans.app_test_lb/.audio.AudioCreator" % (self.deviceId)
        else:
            cmd = "adb shell am start com.iflytek.easytrans.app_test_lb/.audio.AudioCreator"

        os.system(cmd)

    # 音频播放工具comb的音频播放
    def playAudioFile(self, path ='', speed = '1'):

        if self.deviceId:
            cmd = 'adb -s %s shell am broadcast -a NEW_REDIOPLAY --es path %s --es speed %s'%(self.deviceId, path, speed)
        else:
            cmd = 'adb shell am broadcast -a NEW_REDIOPLAY --es path %s --es speed %s'%(path, speed)

        print(cmd)
        os.system(cmd)

    # 音频播放工具comb的tts合成并播放
    def playTtsResult(self, lang, text, type = '0', speed = '1'):

        if self.deviceId:
            cmd = "adb -s %s shell am broadcast -a TTS_AUDIOPLAY --es lang %s --es text '%s' --es type %s --es speed %s" %\
                  (self.deviceId, lang, text, type, speed)
        else:
            cmd = "adb shell am broadcast -a TTS_AUDIOPLAY --es lang %s --es text '%s' --es type %s --es speed %s" %\
                  (lang, text, type, speed)

        print(cmd)
        os.system(cmd)

    def TextToSpeech01(self,role,text):
        """文本转语音播报
        """
        a="\\"
        if self.deviceId:
            cmd = 'adb -s %s shell am broadcast -a NEW_TTSPARAM --es role %s --es text %s"%s"'%(self.deviceId, role, a, text)
        else:
            cmd = 'adb shell am broadcast -a NEW_TTSPARAM --es role %s --es text %s"%s"'%(role,a,text)

        os.system(cmd)

    def TextToSpeech02(self,role,text):
        """文本转语音播报
        """
        if self.deviceId:
            cmd = 'adb -s %s shell am broadcast -a NEW_TTSPARAM --es role %s --es text %s'%(self.deviceId, role, text)
        else:
            cmd = 'adb shell am broadcast -a NEW_TTSPARAM --es role %s --es text %s'%(role,text)

        os.system(cmd)                          
#---------------------------------------------------  
    def Unlock(self):
        """解锁屏幕
        """
        cmd1 = "adb shell input keyevent KEYCODE_POWER" 
        cmd2 = "adb shell input keyevent 82" 
        cmd3 = "adb shell svc power stayon true" 
        os.system(cmd1) 
        time.sleep(2)
        os.system(cmd1) 
        time.sleep(1)
        os.system(cmd2)
        time.sleep(1) 
        os.system(cmd3)  

    def logcat(self,logfile):
        """获取打印的日志
        """
        result = os.popen('adb logcat -d').readlines()
        if len(result):
            return str(result).decode("string_escape")
            #return result[0]

        else:
            return None

#---------------------------------------------------网络打开关闭
    def openwifi(self):
        """打开wifi连接
        """

        if self.deviceId != '':
            cmd = "adb -s %s shell svc wifi enable"%(self.deviceId)
        else:
            cmd = "adb shell svc wifi enable"

        os.system(cmd)
        
    def closewifi(self):
        """关闭wifi连接
        """
        if self.deviceId:
            cmd = "adb -s %s shell svc wifi disable" % (self.deviceId)
        else:
            cmd = "adb shell svc wifi disable"

        os.system(cmd) 

    def opendata(self):
        """打开数据连接
        """
        if self.deviceId:
            cmd = "adb -s %s shell svc data enable" % (self.deviceId)
        else:
            cmd = "adb shell svc data enable"

        os.system(cmd)

    def closedata(self):
        """关闭数据连接
        """
        if self.deviceId:
            cmd = "adb -s %s shell svc data disable" % (self.deviceId)
        else:
            cmd = "adb shell svc data disable"

        os.system(cmd)  

#================================================================

    # 初始化uiautomator
    def initUiautomator(self):
        cmd = 'python -m uiautomator2 init'
        os.system(cmd)

    # push文件到sdcard目录下
    def pushFile2Sdcard(self, filePath = '/audio/wav/.'):
        rootPath = os.path.abspath(os.path.join(os.getcwd(), "../..")) + filePath

        if self.deviceId:
            cmd = 'adb -s %s push %s %s' % (self.deviceId, filePath, '/sdcard/')
        else:
            cmd = 'adb push %s %s' % (rootPath, '/sdcard/')

        os.system(cmd)

    # 按下电源键并抬起
    def clickPower(self):
        if self.deviceId:
            cmd = 'adb -s %s shell input keyevent KEYCODE_POWER' % (self.deviceId)
        else:
            cmd = 'adb shell input keyevent KEYCODE_POWER'

        print('click power')
        os.system(cmd)

    # 3.0 时长版机器获取网络类型 wifi   null:无网   hardsim:硬卡   softsim:软卡
    def getNetworkType(self):
        if self.deviceId:
            cmd = 'adb -s %s shell getprop runtime.if.networktype'%(self.deviceId)
        else:
            cmd = 'adb shell getprop runtime.if.networktype'

        pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = pi.stdout.read()
        pi.kill()

        output = output.decode("utf-8").strip()

        print("network_Type = " + str(output))

        if output == "WIFI":
            return 'wifi'
        elif output == "NULL":
            return 'null'
        elif output == "HARDSIM":
            return 'hardsim'
        elif output == "SOFTSIM":
            return 'softsim'
        else:
            return 'null'

    def click_mainscreen(self):
        """会话翻译点击主屏
        """
        cmd = "adb shell am broadcast -a com.iflytek.vt.test_mainscreen_click"
        os.system(cmd)

    def click_subscreen(self):
        """会话翻译点击副屏
        """
        cmd = "adb shell am broadcast -a com.iflytek.vt.test_subscreen_click"
        os.system(cmd)

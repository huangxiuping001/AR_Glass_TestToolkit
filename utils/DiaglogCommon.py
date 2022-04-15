"""
# @Time : 2019/10/2719:33
# @Author : qxguo2
# @File : DiaglogCommon.py

"""
import subprocess
import os
import wave

class DiaglogCommon(object):
    '''
    classdocs
    '''

    def __init__(self, object,logprint):
        '''
        Constructor
        '''
        self.d=object
        self.log=logprint
        self.screenpath = os.path.abspath(os.path.join(os.getcwd(), "../../../Screenshot/Diaglog")) + "//"


    def gain_device(self):
        result2 = os.popen('adb devices ').readlines()
        device = result2[1]
        return device[:-7].strip()

    def gain_rec_tran_text(self):
        ScreenText_list=[]
        #result3 = os.popen(("adb logcat -d -s IFLY_CT_ConversationActivity| findstr mIsEnd=true")).readlines()
        svnlog1 = subprocess.Popen("adb logcat -d -s IFLY_CT_ConversationActivity| findstr mIsEnd=true", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result1 = svnlog1.stdout.readlines()
        if len(result1)>0:

            result1 = result1[len(result1) - 1]
            result1=str(result1, encoding="UTF-8")
            print(result1)

            RecUpScreenText_index01=result1.find("mRecText")
            RecUpScreenText_index02 = result1.find(", mRecTextTag")
            TransUpScreenText_index01=result1.find("mTransText")
            TransUpScreenText_index02 = result1.find(", mTransTextTag")

            RecUpScreenText=result1[RecUpScreenText_index01+10:RecUpScreenText_index02-1]
            TransUpScreenText=result1[TransUpScreenText_index01+12:TransUpScreenText_index02-1]

            print (TransUpScreenText)
            print(RecUpScreenText)
            ScreenText_list.append(RecUpScreenText)
            ScreenText_list.append(TransUpScreenText)
            return  ScreenText_list
        else:
            ScreenText_list.append("null")
            ScreenText_list.append("null")
            return ScreenText_list



    def gain_audio_time(self,filepath):
        '''
        获取wav音频时长
        '''
        file = wave.open(filepath)
        time_count = file.getparams().nframes / file.getparams().framerate
        return time_count

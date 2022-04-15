# coding:utf-8

import os
import sqlite3
import time
import uiautomator2 as u2
import xlrd

from utils import comtools as ctools

# reload(sys)
# sys.setdefaultencoding('utf-8')
# cn_esr = u"离线翻译测试，您好，今天天气怎么样？"
# trans= {"en": u"Hello, what's the weather like today?",
#         "ja": u"万一，こんにちは，今日の機械はどうですか。"}

prepareText = u"离线翻译准备中，请稍等"


class uiTools(object):
    def __init__(self, driver, AdbTools, AdbOperate, deviceId=''):
        self.d = driver
        self.deviceId = deviceId
        self.tools = AdbTools
        self.adb = AdbOperate
        self.play_state = 1 # 音频播放状态，0代表stopper,代表 started

    def uiautomatorInit(self):
        # 判断atx-agent进程是否存在，若不存在则初始化uiautomator2
        u2_init = os.popen("adb -s {0} shell ps | findStr atx-agent".format(self.deviceId)).readlines()
        if len(u2_init) < 0:
            init_result = os.popen('python -m uiautomator2 init').readlines()
            #     if "success" in init_result[len(init_result) - 1]:
            #         return True
            #     else:
            #         return False
            # return True
            time.sleep(30)

            # 从home界面切换离线语种

    def switchLanguage(self, language, sleepTime):
        self.backHomeNew()
        # self.d.click(0.436, 0.75)
        try:
            if not self.d(text = language).exists():
                self.d(resourceId="com.iflytek.easytrans.launcher:id/language_layout").click()
                # 从父布局中根据text查找目标控件并点击
                self.d(className="android.support.v7.widget.RecyclerView",
                       resourceId="com.iflytek.easytrans.launcher:id/recyclerView_Language") \
                    .child_by_text(language, allow_scroll_search=True, className="android.widget.TextView").click()
                time.sleep(sleepTime)
        except u2.UiObjectNotFoundError as e:
            print(e)
            raise


    # 返回主界面
    def backHomeNew(self):
        # print("activity = " + str(self.d.current_app()['activity']))
        # print("package = " + str(self.d.current_app()['package']))

        while self.d.current_app()['package'] != 'com.iflytek.easytrans.launcher' \
                or not self.d(resourceId='com.iflytek.easytrans.launcher:id/date').exists():
            os.popen("adb -s {0} shell input keyevent --longpress 4".format(self.deviceId))
            time.sleep(1)

        # print('current is home page !')
        # self.d.press('home')
        #
        # self.d.press('back')

    # 返回按键翻译主界面
    def backHome_voice(self):
        while not (self.d.current_app()['package'] == 'com.iflytek.easytrans.launcher'
                   and self.d(resourceId='com.iflytek.easytrans.launcher:id/title_tv').exists()) or \
                self.d(resourceId = "com.iflytek.easytrans.launcher:id/modify_edt").exists():
            print("Not home page ! Go back !")

            # self.d.press('back')
            # 短按进入语音翻译
            self.adb.chineseKeyDownLB(self.deviceId)
            time.sleep(0.1)
            self.adb.chineseKeyUpLB(self.deviceId)
            time.sleep(0.5)

        print("Already home page!")


    def check_toast(self, text):
        result = self.d.toast.get_message(10.0, 10.0)
        # print "\n Toast:{0}".format(result)
        if result == text:
            return 1
        else:
            return 0

    def check_preparing(self, text):
        self.adb.chineseKeyDownNew()
        time.sleep(1)
        self.adb.chineseKeyUpNew()
        result = self.check_toast(text)
        print("check_preparing:{0}".format(result))
        if result == 1:
            return 1
        else:
            return 0

    def check_preparing_lb(self, text):
        self.adb.chineseKeyDownLB(self.deviceId)
        time.sleep(1)
        self.adb.chineseKeyUpLB(self.deviceId)
        result = self.check_toast(text)
        # print("check_preparing:{0}".format(result))
        if result == 1:
            return 1
        else:
            return 0


    # 截图保存
    def save_screen(self, fileName):
        fileName = time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + "_" + fileName + ".png"

        # folder = os.path.join(folder, time.strftime('%Y%m%d', time.localtime(time.time())))
        folder = time.strftime('%Y%m%d', time.localtime(time.time()))
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.d.screenshot(os.path.join(folder, fileName))

    # 触发按键翻译,返回识别结果和翻译结果   cn 中文按键  foreign 外文按键,
    # 文件需要放在/sdcard/目录下, audio传完整文件名
    def voiceTrans(self, audio, keytype='foreign'):
        fileName = os.path.split(audio)[1]
        if fileName.endswith('.mp3'):
            fileName = fileName.split('.')[0]
        print("\n audio:{0},fileName:{1}".format(audio, fileName))
        try:
            if keytype == 'cn':
                self.adb.chineseKeyDownNew()
                # self.adb.ChineseKeydown(self.deviceId)

                self.adb.PlayAudio(fileName, "/")
                print("\n audioLen:{0}".format(int(self.adb.getMp3Length(audio)) + 1))
                time.sleep(int(self.adb.getMp3Length(audio)) + 2)
                self.adb.chineseKeyUpNew()
                # self.adb.ChineseKeyup(self.deviceId)
            else:
                self.adb.foreignKeyDownNew()
                # self.adb.ForeignKeydown(self.deviceId)

                self.adb.PlayAudio(fileName, "/")
                time.sleep(int(self.adb.getMp3Length(audio)) + 2)
                self.adb.foreignKeyUpNew()
                # self.adb.ForeignKeyup(self.deviceId)
        except Exception as e:
            print(e)
            raise

        # 触发按键翻译,返回识别结果和翻译结果   cn 中文按键  foreign 外文按键,

    # 文件需要放在/sdcard/目录下, audio传完整电脑本地文件名
    def voiceTrans_lb(self, audio, keytype='foreign'):
        print(audio)
        fileName = os.path.split(audio)[1]
        if fileName.endswith('.mp3'):
            fileName = fileName.split('.')[0]
        print("\n audio:{0},fileName:{1}".format(audio, fileName))
        # 向翻译机推送音频
        os.popen('adb -s {0} push "{1}" "{2}"'.format(self.deviceId, audio, "/sdcard/"))
        try:
            if keytype == 'cn':
                self.adb.chineseKeyDownLB(self.deviceId)

                self.adb.PlayAudio(fileName, "/", self.deviceId)
                print("\n audioLen:{0}".format(int(self.adb.getMp3Length(audio)) + 1))
                time.sleep(int(self.adb.getMp3Length(audio)) + 2)
                self.adb.chineseKeyUpLB(self.deviceId)
            else:
                self.adb.foreignKeyDownLB(self.deviceId)

                self.adb.PlayAudio(fileName, "/", self.deviceId)
                time.sleep(int(self.adb.getMp3Length(audio)) + 2)
                self.adb.foreignKeyUpLB(self.deviceId)
        except Exception as e:
            print(e)
            raise

    def getEsr_and_trans_Content(self, keytype='foreign'):
        try:
            self.d(resourceId='com.iflytek.easytrans.launcher:id/tlv_trans_loading').wait_gone(40)
            self.d(resourceId='com.iflytek.easytrans.launcher:id/lv_trans_loading').wait_gone(40)

            if keytype == 'foreign':
                resourceId = 'com.iflytek.easytrans.launcher:id/foreign_layout'
                esr_resourceId = 'com.iflytek.easytrans.launcher:id/other_original'
                trans_resourceId = 'com.iflytek.easytrans.launcher:id/other_translate'
            else:
                resourceId = 'com.iflytek.easytrans.launcher:id/chinese_layout'
                esr_resourceId = 'com.iflytek.easytrans.launcher:id/chinese_original'
                trans_resourceId = 'com.iflytek.easytrans.launcher:id/chinese_translate'

            count = self.d(resourceId=resourceId, className="android.widget.RelativeLayout").count

            print(str(count))
            translater = self.d(resourceId=resourceId, instance=count - 1) \
                .child(resourceId=trans_resourceId).get_text(5).strip()
            # 翻译文本超过一屏时需拖动屏幕查找esr
            while self.d(resourceId=resourceId). \
                    child(resourceId=esr_resourceId).count == 0:
                self.d.swipe(0.5, 0.2, 0.5, 0.25, duration=0.01)
                time.sleep(0.5)

            esr = self.d(resourceId=resourceId, instance=count - 1) \
                .child(resourceId=esr_resourceId).get_text(5).strip()



            print("esr = " + esr)
            print("trans = " + translater)

            return esr, translater
        except Exception as e:
            print(e)
            raise



    # def check_offline_init(self, checklang):
    #     self.voiceTrans(os.path.join(audioFolder, check_cn_file), "cn")
    #     result = self.check_trans_result(cn_esr, trans[checklang], "cn")
    #     return result

    # 删除所有记录
    def deleteAll(self,btn="删除"):
        try:
            print("开始删除所有翻译记录\n")
            # 如果不在翻译记录页，则进入翻译记录页
            if not self.d(resourceId = "com.iflytek.easytrans.launcher:id/tv_target_Lang").exists():
                self.adb.chineseKeyDownNew()
                time.sleep(0.5)
                self.adb.chineseKeyUpNew()
                self.d(resourceId = "com.iflytek.easytrans.launcher:id/tv_error").wait_gone()

            if self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout').exists():
                self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout').long_click()
                self.d(resourceId='com.iflytek.easytrans.launcher:id/delete_all').click_exists(1)
                self.d(text= btn).click_exists(1)
                time.sleep(1)
            elif self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout').exists():
                self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout').long_click()
                self.d(resourceId='com.iflytek.easytrans.launcher:id/delete_all').click_exists(1)
                self.d(text= btn).click_exists(1)
                time.sleep(1)
        except Exception as e:
            print(e)
            raise



     # 删除单条记录
    def delete_single(self, btn="删除"):
        try:
            content = " no result"
            # 如果不在翻译记录页，则进入翻译记录页
            if not self.d(resourceId="com.iflytek.easytrans.launcher:id/tv_target_Lang").exists():
                self.adb.chineseKeyDownNew()
                time.sleep(0.5)
                self.adb.chineseKeyUpNew()
                self.d(resourceId="com.iflytek.easytrans.launcher:id/tv_error").wait_gone()

            if self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout').exists():
                content = self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout')\
                           .child(resourceId = "com.iflytek.easytrans.launcher:id/chinese_original").get_text(5)
                self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout').long_click()
                self.d(text="删除本条").click_exists(1)
                self.d(text=btn).click_exists(1)
                time.sleep(1)
            elif self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout').exists():
                content = self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout', instance=0) \
                           .child(resourceId="com.iflytek.easytrans.launcher:id/other_original").get_text(5)
                self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout').long_click()
                self.d(text=  "删除本条").click_exists(1)
                self.d(text= btn).click_exists(1)
                time.sleep(1)
            return content
        except Exception as e:
            print(e)
            raise


    # 根据语种设置音频文件名称
    def get_foreign_fileName(self, lang='en'):
        if lang == "en":
            fileName = 'en-US'
        elif lang == "ja":
            fileName = 'ja-JP'
        elif lang == "ko":
            fileName = 'ko-KR'
        else:
            fileName = 'ru-RU'
        return fileName

    def check_trans_result(self, EsrCheck, TransCheck, keytype):
        try:
            print(EsrCheck, TransCheck)
            esr, trans = self.getEsr_and_trans_Content(keytype)
            esrDistance = ctools.minDistance(esr, EsrCheck)
            transDistance = ctools.minDistance(trans, TransCheck)

            # 如果esr和trans 最小编辑率大于90%，则认为翻译失败
            print(float(esrDistance / len(EsrCheck)), float(transDistance / len(TransCheck)))
            if float(esrDistance / len(EsrCheck)) > 0.9 or float(transDistance / len(TransCheck)) > 0.9:
                return 0
            return 1
        except Exception as e:
            print(e)
            raise


    # 进行一次翻译，mode=1 只进行中翻外，mode=2进行双向翻译
    def check_voice_trans(self, data, audioFolder=r"D:/untitled/audio/offline/", mode=1, sleep=15):
        try:
            print("\n switch to {0}".format(data["selectName"]))
            result1 =1
            result2 =1
            self.switchLanguage(data["selectName"], sleep)

            self.voiceTrans(os.path.join(audioFolder, data["audioSrc"]), "cn")
            result1 = self.check_trans_result(data["esrSrc"], data["transSrc"],"cn")
            # assert result == 1, "check_voice_trans:{0} to {1} failed!".format(data["srcLangName"], data["targetLangName"])
            if mode == 2:
                self.voiceTrans(os.path.join(audioFolder, data["audioTarget"]), "foreign")
                result2 = self.check_trans_result(data["esrTarget"], data["transTarget"], "foreign")
                # assert result == 1, "check_voice_trans:{0} to {1} failed!".format(data["targetLangName"], data["srcLangName"])
            return result1==1 & result2==1
        except Exception as e:
            print(e)
            raise

    def get_mp3_name(self, audioFolder, lang):
        for root, dirs, files in os.walk(os.path.join(audioFolder,lang)):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    return os.path.join(audioFolder,lang,file)


    # 进行一次拍照翻译
    def ocr_trans(self,ocrlang):
        # 切换到拍照翻译使用一次拍照
        self.d.app_start("com.iflytek.easytrans.ocr")
        time.sleep(3)
        try:
            if not self.d(text = ocrlang):
                self.d(resourceId = "com.iflytek.easytrans.ocr:id/ll_lang").click_exists(10)
                self.d(resourceId = "com.iflytek.easytrans.ocr:id/tv_src_language",text = ocrlang).click_exists(10)
            self.d(resourceId="com.iflytek.easytrans.ocr:id/iv_capture").click_exists(10)
            self.d(resourceId="com.iflytek.easytrans.ocr:id/iv_translate").click_exists(10)
            time.sleep(3)

        except Exception as e:
            print(e)
            raise

    def into_wsl(self):
        try:
            # 下拉出状态栏
            self.d.swipe(0.5,0.02, 0.5,0.5,0.01)
            self.d(text = "怎么跟外国人说第一句话？").click_exists(3)
            time.sleep(0.5)
        except Exception as e:
            print(e)
            raise

    def into_helper(self):
        try:
            # 下拉出状态栏
            self.d.swipe(0.5, 0.02, 0.5, 0.5, 0.01)
            self.d(resourceId="com.android.systemui:id/help_button").click_exists(3)
            time.sleep(0.5)
        except Exception as e:
            print(e)
            raise

    def into_setting(self):
        try:
            # 下拉出状态栏
            self.d.swipe(0.5, 0.02, 0.5, 0.5, 0.01)
            self.d(resourceId="com.android.systemui:id/settings_button").click_exists(timeout=3)
            time.sleep(0.5)
        except Exception as e:
            print(e)
            raise

    def into_wlan(self):
        try:
            # 下拉出状态栏
            self.d.swipe(0.5, 0.02, 0.5, 0.5, 0.01)
            ele = self.d(resourceId="com.android.systemui:id/ifly_wifi_layout")
            if ele.exists(3):
                ele.long_click()
                time.sleep(0.5)
        except Exception as e:
            print(e)
            raise

    def into_bluetooth(self):
        try:
            # 下拉出状态栏
            self.d.swipe(0.5, 0.02, 0.5, 0.5, 0.01)
            ele = self.d(resourceId="com.android.systemui:id/ifly_bluetooth_layout")
            if ele.exists(3):
                ele.long_click()
                time.sleep(0.5)
        except Exception as e:
            print(e)
            raise

    def into_mobile_data(self):
        try:
            # 下拉出状态栏
            self.d.swipe(0.5, 0.02, 0.5, 0.5, 0.01)
            ele = self.d(resourceId="com.android.systemui:id/ifly_mobile_data_layout")
            if ele.exists(3):
                ele.long_click()
                time.sleep(0.5)
        except Exception as e:
            print(e)
            raise

   # 该方法只供 录音、翻译流程中使用
    def into_app(self,appname):
        print("into app")
        try:
            while not self.d(text = appname).exists(timeout=0.5):
                self.d.swipe(0.9, 0.5, 0.1, 0.5, 0.01)
            self.d(text=appname).click()
            time.sleep(2)
        except Exception as e:
            print(e)
            raise

    def check_stop(self, keyTypes="cn_foreign"):
        try:
            self.d(resourceId='com.iflytek.easytrans.launcher:id/tlv_trans_loading').wait_gone()
            self.d(resourceId='com.iflytek.easytrans.launcher:id/lv_trans_loading').wait_gone()
            f_resourceId = 'com.iflytek.easytrans.launcher:id/foreign_layout'
            cn_resourceId = 'com.iflytek.easytrans.launcher:id/chinese_layout'
            keys = keyTypes.split("_")
            print(keys)

            if len(keys)==1:
                if keys[0] == 'cn' and self.d(resourceId=f_resourceId).count==0 and self.d(
                        resourceId=cn_resourceId).count==1:
                    return 1
                elif self.d(resourceId=cn_resourceId).count==0 and self.d(resourceId=f_resourceId).count==1:
                    return 1
                else:
                    return 0
            else:
                for i in range(0,len(keys)):

                    if keys[i]=="cn" and self.d(resourceId=cn_resourceId).count<1:
                        return 0

                    if keys[i]=="foreign" and self.d(resourceId=f_resourceId).count<1:
                        return 0
                return 1
        except Exception as e:
            print(e)
            raise

    def check_play_state(self, piid="",timeout =1):
        self.play_state = 1
        while timeout >0 :
            lines = os.popen('adb -s {0} shell dumpsys audio |  findStr "state:"'.format(self.deviceId)).readlines()

            if piid == "":
                r= lines[len(lines)-1]
            else:
                for i in range(0,len(lines)):
                    if piid in lines[len(lines)-1-i]:
                        r = lines[len(lines)-1-i]
                        break
            print("\n play state:{0}".format(r))
            if "stopped"in r :
                self.play_state=0
                break
            time.sleep(0.5)
            timeout = timeout -1


    # 获取最后某个状态的ppid,playstate有started、stopped2个状态
    def get_last_piid(self,playstate= "", timeout =1):
        result = ""

        while timeout >0 :
            lines = os.popen('adb -s {0} shell dumpsys audio |  findStr "state:"'.format(self.deviceId)).readlines()
            r = lines[len(lines)-1]
            print(r)
            if  playstate in r:
                result = r.split(" ")[3]
                break
            time.sleep(0.5)
            timeout = timeout-1
        return result


    def transRecord_exist(self,type=""):
        try:
            f_resourceId = 'com.iflytek.easytrans.launcher:id/foreign_layout'
            cn_resourceId = 'com.iflytek.easytrans.launcher:id/chinese_layout'

            if type=="离线结果":
                if self.d(text = "离线结果").exists(timeout =10):
                    return  True
                else:
                    return False
            elif type == "在线结果":
                if (self.d(resourceId=f_resourceId).count + self.d(resourceId=cn_resourceId).count - self.d(text = "离线结果").count)>0:
                    return True
            else:
                if self.d(resourceId=f_resourceId).count > 0:
                    return True
                if self.d(resourceId=cn_resourceId).count > 0:
                    return True
            return False
        except Exception as e:
            print(e)
            raise



    def record_feedback(self, tag= "离线结果"):
        try:
            # 如果不在翻译记录页，则进入翻译记录页
            if not self.d(resourceId="com.iflytek.easytrans.launcher:id/tv_target_Lang").exists():
                self.adb.chineseKeyDownNew()
                time.sleep(0.5)
                self.adb.chineseKeyUpNew()
                self.d(resourceId="com.iflytek.easytrans.launcher:id/tv_error").wait_gone()
            if tag == "离线结果":
                if self.d(text = tag).exists():
                    self.d(text=tag).long_click()
                    self.d(resourceId = "com.iflytek.easytrans.launcher:id/feedback_error").click()
                    return
            elif tag == "在线结果":
                cn_count = self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout').count
                f_count = self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout').count
                while cn_count>0 :
                    if self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout',instance = cn_count-1).\
                            sibling(resourceId = "com.iflytek.easytrans.launcher:id/offline_tip_layout").exists():
                        cn_count = cn_count  -1
                        print(cn_count)
                    else:
                        self.d(resourceId='com.iflytek.easytrans.launcher:id/chinese_layout', instance=cn_count - 1).\
                            long_click()
                        self.d(resourceId="com.iflytek.easytrans.launcher:id/feedback_error").click()
                        return
                while f_count >0 :
                    if self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout',instance = f_count-1).\
                            sibling(resourceId = "com.iflytek.easytrans.launcher:id/offline_tip_layout").exists():
                        f_count = f_count  -1
                        print(f_count)
                    else:
                        self.d(resourceId='com.iflytek.easytrans.launcher:id/foreign_layout', instance=f_count - 1).\
                            long_click()
                        self.d(resourceId="com.iflytek.easytrans.launcher:id/feedback_error").click()
                        return
        except Exception as e:
            print(e)
            raise



    # 从翻译机pull 数据库到本地，然后进行数据查询，返回结果
    def query_db(self,dir, sql, ):
        save_dir = os.path.join(os.getcwd(), dir.split("/")[-1])
        os.popen("adb -s {0} pull {1} {2} ".format(self.deviceId,dir,os.getcwd()))
        time.sleep(3)
        conn = sqlite3.connect(save_dir)
        c = conn.cursor()

        c.execute(sql)
        # conn.commit()
        result = c.fetchall()
        conn.close()
        print(result)
        return result

    #从翻译机pull数据库到本地然后进行数据插入，最后push
    def change_db(self,dir,sqls):
        save_dir = os.path.join(os.getcwd(), dir.split("/")[-1])
        os.popen("adb -s {0} pull {1} {2} ".format(self.deviceId, dir, os.getcwd()))
        time.sleep(3)
        conn = sqlite3.connect(save_dir)
        c = conn.cursor()
        for sql in sqls:
            c.execute(sql)
        conn.commit()
        # result = c.fetchall()
        conn.close()
        # print(result)
        # return result
        os.popen("adb -s {0} push {1} {2}".format(self.deviceId,save_dir,dir))
        time.sleep(3)


    # 通过点击桌面图标进入语音翻译记录页
    def enter_voice_by_icon(self):
        if not (self.d.current_app()['package'] == 'com.iflytek.easytrans.launcher'
                and self.d(resourceId='com.iflytek.easytrans.launcher:id/title_tv').exists()) or\
                self.d(resourceId="com.iflytek.easytrans.launcher:id/modify_edt").exists():
            self.backHomeNew()
            print(" back home")
            self.d(text = "语音翻译",resourceId = "com.iflytek.easytrans.launcher:id/tv_voice_trans").click()


    def big_voiceTrans(self, lang, audio_folder, audio_len, t_time, keytype='foreign'):

        targetFolder = "/sdcard/" + lang

        os.popen("adb -s {1} shell mkdir -p {0}".format(targetFolder, self.deviceId))
        # 向翻译机推送音频
        os.popen('adb -s {0} push "{1}\{2}_audio\." "{3}"'.format(self.deviceId, audio_folder, lang, targetFolder))
        print('adb -s {0} push "{1}\{2}_audio\." "{3}"'.format(self.deviceId, audio_folder, lang, targetFolder))

        try:
            start = 1
            count = 0

            if keytype == 'cn' or keytype == 'hanyu':
                for root, dirs, files in os.walk(audio_folder):
                    for file in files:
                        if count < t_time:
                            if start == 1:
                                self.adb.chineseKeyDownNew()
                                start = 0
                                t = 0

                            if t < audio_len:
                                if os.path.splitext(file)[1] == ".mp3":
                                    self.adb.PlayAudio("'{0}'".format(os.path.splitext(file)[0]), lang)
                                    # print("\n audioLen:{0}".format(int(self.adb.getMp3Length(audio)) + 1))
                                    audio_t = int(self.adb.getMp3Length(os.path.join(root, file)))
                                    time.sleep(audio_t)
                                    t = t + audio_t
                            else:
                                print("\nt:{0}".format(t))
                                self.adb.chineseKeyUpNew()
                                # self.wait_trans_end(40)
                                esr, trans = self.getEsr_and_trans_Content("cn")

                                self.deleteAll()
                                if esr != " " and trans != " ":
                                    self.save_esr_trans(count, esr, trans,
                                                        lang + time.strftime('%Y%m%d', time.localtime(time.time()))+ ".txt")
                                else:
                                    return 0
                                count = count + 1
                                start = 1
                return 1
            else:
                for root, dirs, files in os.walk(audio_folder):
                    for file in files:
                        if count < t_time:
                            if start == 1:
                                self.adb.foreignKeyDownNew()
                                start = 0
                                t = 0

                            if t < audio_len:
                                if os.path.splitext(file)[1] == ".mp3":
                                    self.adb.PlayAudio("'{0}'".format(os.path.splitext(file)[0]), lang)
                                    # print("\n audioLen:{0}".format(int(self.adb.getMp3Length(audio)) + 1))
                                    audio_t = int(self.adb.getMp3Length(os.path.join(root, file)))
                                    time.sleep(audio_t)
                                    t = t + audio_t
                            else:
                                print("\nt:{0}".format(t))
                                self.adb.foreignKeyUpNew()
                                # self.wait_trans_end(40)
                                esr, trans = self.getEsr_and_trans_Content("foreign")
                                self.deleteAll()
                                if esr != " " and trans != " ":
                                    self.save_esr_trans(count, esr, trans,
                                                        lang + time.strftime('%Y%m%d', time.localtime(time.time()))+ ".txt")
                                else:
                                    return 0
                                count = count + 1
                                start = 1
                return 1
        except Exception as e:
            print(e)
            raise


    def save_esr_trans(self,count,esr,trans,f_name):
        with open(f_name, "a+",encoding="utf-8") as file:
            file.write("|".join([str(count),esr,trans,"\n"]))

# if __name__ == '__main__':

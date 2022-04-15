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


class uitoolsLB(object):
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


    # 默认不重复切换语种
    def switchLanguage_lb(self, src, tar, sleepTime=15,re_switch =False):
        self.backVoice_by_key()
        # self.d.click(0.436, 0.75)
        try:
            # re_switch = False 则判断当前语种是否与目标语种一致
            print("src:{0},tar:{1}".format(self.d(resourceId="com.iflytek.easytrans.launcher:id/src_lang_tv", text=src).exists(),
                                           self.d(resourceId="com.iflytek.easytrans.launcher:id/target_lang_tv",
                                                  text=tar).exists()))
            if re_switch or not self.d(resourceId="com.iflytek.easytrans.launcher:id/src_lang_tv", text=src).exists() or\
                    not self.d(resourceId="com.iflytek.easytrans.launcher:id/target_lang_tv", text=tar).exists():
                self.d(resourceId="com.iflytek.easytrans.launcher:id/select_lyt").click()

                if not self.d(resourceId = "com.iflytek.easytrans.launcher:id/tv_src_language").get_text() ==src:
                    self.d(resourceId="com.iflytek.easytrans.launcher:id/rl_src_language").click()
                    time.sleep(0.3)
                    # 从父布局中根据text查找目标控件并点击
                    self.d(className="android.support.v7.widget.RecyclerView",
                           resourceId="com.iflytek.easytrans.launcher:id/recyclerView_Language") \
                        .child_by_text(src, allow_scroll_search=True, className="android.widget.TextView").click()

                # 从父布局中根据text查找目标控件并点击
                self.d(className="android.support.v7.widget.RecyclerView",
                       resourceId="com.iflytek.easytrans.launcher:id/recyclerView_Language") \
                    .child_by_text(tar, allow_scroll_search=True, className="android.widget.TextView").click()
            time.sleep(sleepTime)
        except u2.UiObjectNotFoundError as e:
            print(e)
            raise

    # 返回主界面
    def backHomeLB(self):
        # print("activity = " + str(self.d.current_app()['activity']))
        # print("package = " + str(self.d.current_app()['package']))

        # while self.d.current_app()['package'] != 'com.iflytek.easytrans.launcher' \
        #         or not self.d(resourceId='com.iflytek.easytrans.launcher:id/tv_time').exists():
        while not self.d(resourceId='com.iflytek.easytrans.launcher:id/tv_voice_trans').exists():
            os.popen("adb -s {0} shell input keyevent --longpress 4".format(self.deviceId))
            time.sleep(1)

        # print('current is home page !')
        # self.d.press('home')
        #
        # self.d.press('back')

    # 返回按键翻译主界面
    def backVoice_by_key(self):
        while not (self.d.current_app()['package'] == 'com.iflytek.easytrans.launcher'
                   and self.d(resourceId='com.iflytek.easytrans.launcher:id/title_tv').exists()) or \
                self.d(resourceId = "com.iflytek.easytrans.launcher:id/modify_edt").exists():
            print("Not home page ! Go back !")

            # self.d.press('back')
            # 短按进入语音翻译
            self.adb.chineseKeyDownLB()
            time.sleep(0.1)
            self.adb.chineseKeyUpLB()
            time.sleep(0.5)

        print("Already home page!")


    def check_toast(self, text):
        result = self.d.toast.get_message(10.0, 10.0)
        # print "\n Toast:{0}".format(result)
        if result == text:
            return 1
        else:
            return 0


    def check_preparing_lb(self, text):
        self.adb.chineseKeyDownLB()
        time.sleep(1)
        self.adb.chineseKeyUpLB()
        result = self.check_toast(text)
        # print("check_preparing:{0}".format(result))
        if result == 1:
            return 1
        else:
            return 0


    # 截图保存
    def save_screen(self, fileName):
        fileName = time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + "_" + fileName + ".png"
        log_name = time.strftime('%Y%m%d%H%M', time.localtime(time.time())) + "_" + fileName + ".txt"

        # folder = os.path.join(folder, time.strftime('%Y%m%d', time.localtime(time.time())))
        folder = time.strftime('%Y%m%d', time.localtime(time.time()))
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.d.screenshot(os.path.join(folder, fileName))
        os.system("adb -s {0} logcat -v time -d >{1}".format(self.deviceId, os.path.join(folder, log_name)))



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
                self.adb.chineseKeyDownLB()

                self.adb.PlayAudio(fileName, "/")
                print("\n audioLen:{0}".format(int(self.adb.getMp3Length(audio)) + 1))
                time.sleep(int(self.adb.getMp3Length(audio)) + 2)
                self.adb.chineseKeyUpLB()
            else:
                self.adb.foreignKeyDownLB()

                self.adb.PlayAudio(fileName, "/")
                time.sleep(int(self.adb.getMp3Length(audio)) + 2)
                self.adb.foreignKeyUpLB()
        except Exception as e:
            print(e)
            raise

    def big_voiceTrans_lb(self, lang,audio_folder,audio_len,t_time, keytype='foreign'):

        targetFolder = "/sdcard/" + lang

        os.popen("adb -s {1} shell mkdir -p {0}".format(targetFolder, self.deviceId))
        # 向翻译机推送音频
        os.popen('adb -s {0} push "{1}\{2}_audio\." "{3}"'.format(self.deviceId, audio_folder,lang, targetFolder))
        print('adb -s {0} push "{1}\{2}_audio\." "{3}"'.format(self.deviceId, audio_folder,lang, targetFolder))

        try:
            start =1
            count =0

            if keytype == 'cn':
                for root, dirs, files in os.walk(audio_folder):
                    for file in files:
                        if count < t_time:
                            if start ==1:
                                self.adb.chineseKeyDownLB()
                                start =0
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
                                self.adb.chineseKeyUpLB()
                                self.wait_trans_end(40)
                                esr, trans = self.getEsr_and_trans_Content_lb("cn")
                                if esr != " " and trans != " ":
                                    self.save_esr_trans(count,esr,trans,lang+time.strftime('%Y%m%d', time.localtime(time.time()))+ ".txt")
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
                                self.adb.foreignKeyDownLB()
                                start = 0
                                t=0

                            if t < audio_len:
                                if os.path.splitext(file)[1] == ".mp3":
                                    self.adb.PlayAudio("'{0}'".format(os.path.splitext(file)[0]), lang)
                                    # print("\n audioLen:{0}".format(int(self.adb.getMp3Length(audio)) + 1))
                                    audio_t = int(self.adb.getMp3Length(os.path.join(root, file)))
                                    time.sleep(audio_t)
                                    t = t + audio_t
                            else:
                                print("\nt:{0}".format(t))
                                self.adb.foreignKeyUpLB()
                                self.wait_trans_end(40)
                                esr, trans = self.getEsr_and_trans_Content_lb("cn")
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


    def getEsr_and_trans_Content_lb(self, keytype='foreign'):
        try:
            self.d(resourceId='com.iflytek.easytrans.launcher:id/play_iv').wait(timeout=20)

            # resourceId = 'com.iflytek.easytrans.launcher:id/text_container'
            esr_resourceId = 'com.iflytek.easytrans.launcher:id/src_lang_tv'
            trans_resourceId = 'com.iflytek.easytrans.launcher:id/target_lang_tv'

            esr_count = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                child(resourceId = esr_resourceId).count
            trans_count = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                child(resourceId=trans_resourceId).count

            print("__getEsr_and_trans_Content:esr_count={0},trans_count={1}".format(str(esr_count),str(trans_count)))
            if trans_count > 0 and esr_count>0:
                esr = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                    child(resourceId=esr_resourceId,instance=esr_count - 1).get_text(5).strip()

                translater = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                    child(resourceId=trans_resourceId,instance=trans_count - 1).get_text(5).strip()
            elif trans_count>0 and esr_count==0:
                translater = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                    child(resourceId=trans_resourceId,instance=trans_count - 1).get_text(5).strip()
                # 翻译文本超过一屏时需拖动屏幕查找esr
                while self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                        child(resourceId=esr_resourceId).count ==0:
                    self.d.swipe(0.5,0.3,0.5,0.32,duration=0.01)
                    time.sleep(0.5)
                esr_count = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt"). \
                    child(resourceId=esr_resourceId).count
                esr = self.d(resourceId="com.iflytek.easytrans.launcher:id/content_lyt").\
                    child(resourceId=esr_resourceId,instance=esr_count - 1).get_text(5).strip()
            else:
                esr = " "
                translater = " "
            print("esr:{0}\n".format(esr))
            print("trans:{0}\n".format(translater))
            return esr, translater
        except Exception as e:
            print(e)
            raise


    # def check_offline_init(self, checklang):
    #     self.voiceTrans(os.path.join(audioFolder, check_cn_file), "cn")
    #     result = self.check_trans_result(cn_esr, trans[checklang], "cn")
    #     return result


    # 删除所有记录
    def deleteAll_lb(self, btn="删 除"):
        try:
            # 进入语音翻译并下拉出翻译记录
            self.backVoice_by_key()
            if self.d(text="下拉查看翻译记录").exists():
                self.d.swipe(0.5, 0.19, 0.5, 0.5, duration=0.01)
                time.sleep(1)

            if self.d(resourceId='com.iflytek.easytrans.launcher:id/text_container').exists():
                self.d(resourceId='com.iflytek.easytrans.launcher:id/text_container').long_click()
                self.d(resourceId='com.iflytek.easytrans.launcher:id/multi_choose_tv').click_exists(1)
                self.d(resourceId = "com.iflytek.easytrans.launcher:id/dlt_all_tv").click_exists(1)
                self.d(text=btn).click_exists(1)
                time.sleep(1)

        except Exception as e:
            print(e)
            raise

    # 删除单条记录
    def delete_single_lb(self, btn="删 除"):
        try:
            content = " no transrecord"
            # 进入语音翻译并下拉出翻译记录
            self.backVoice_by_key()

            if self.d(text = "下拉查看翻译记录").exists():
                self.d.swipe(0.5, 0.19, 0.5, 0.5, duration=0.01)

            if self.d(resourceId='com.iflytek.easytrans.launcher:id/text_container').exists():
                content = self.d(resourceId='com.iflytek.easytrans.launcher:id/src_lang_tv').get_text(5)
                self.d(resourceId='com.iflytek.easytrans.launcher:id/text_container').long_click()
                self.d(text="删除").click_exists(1)
                self.d(text=btn).click_exists(1)
                time.sleep(1)

            return content
        except Exception as e:
            print(e)
            raise


    def check_trans_result_lb(self, EsrCheck, TransCheck, keytype):
        try:
            print(EsrCheck, TransCheck)
            esr, trans = self.getEsr_and_trans_Content_lb(keytype)
            esrDistance = ctools.minDistance(esr, EsrCheck)
            transDistance = ctools.minDistance(trans, TransCheck)

            # 如果esr和trans 最小编辑率大于90%，则认为翻译失败
            print(float(esrDistance / len(EsrCheck)), float(transDistance / len(TransCheck)))
            if float(esrDistance / len(EsrCheck)) > 0.95 or float(transDistance / len(TransCheck)) > 0.95:
                return 0
            return 1
        except Exception as e:
            print(e)
            raise

    def get_mp3_name(self, audioFolder, lang):
        for root, dirs, files in os.walk(os.path.join(audioFolder,lang)):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    return os.path.join(audioFolder,lang,file)



    # 进行一次翻译，mode =0 只进行外翻中，mode=1 只进行中翻外，mode=2进行双向翻译
    def check_voice_trans_lb(self, data, audioFolder=r"D:/untitled/audio/offline/", check_file="", mode=1, sleep=15,re_switch=True):
        try:
            print("\n switch to {0} {1}".format(data["srcLangName"], data["targetLangName"]))
            result1 = 0
            result2 = 0
            self.switchLanguage_lb(data["srcLangName"], data["targetLangName"],sleep,re_switch)
            if mode ==0:
                self.voiceTrans_lb(self.get_mp3_name(audioFolder, data["targetLangCode"]), "foreign")
                esr_check, trans_check = self.get_handshake_check_lb(data["targetLangCode"], data["srcLangCode"],
                                                                     check_file)

                result1 = self.check_trans_result_lb(esr_check, trans_check, "foreign")
                return result1

            elif mode ==1:
                self.voiceTrans_lb(self.get_mp3_name(audioFolder, data["srcLangCode"]), "cn")
                esr_check,trans_check = self.get_handshake_check_lb(data["srcLangCode"], data["targetLangCode"],check_file)

                result1 = self.check_trans_result_lb(esr_check,trans_check, "cn")
                return result1
            # assert result == 1, "check_voice_trans:{0} to {1} failed!".format(data["srcLangName"], data["targetLangName"])
            else :
                self.voiceTrans_lb(self.get_mp3_name(audioFolder, data["srcLangCode"]), "cn")
                esr_check, trans_check = self.get_handshake_check_lb(data["srcLangCode"], data["targetLangCode"],
                                                                     check_file)
                result1 = self.check_trans_result_lb(esr_check, trans_check, "cn")
                self.voiceTrans_lb(self.get_mp3_name(audioFolder, data["targetLangCode"]), "foreign")
                esr_check, trans_check = self.get_handshake_check_lb(data["targetLangCode"],data["srcLangCode"], check_file)

                result2 = self.check_trans_result_lb(esr_check, trans_check, "foreign")
                # assert result == 1, "check_voice_trans:{0} to {1} failed!".format(data["targetLangName"], data["srcLangName"])
                return result1 == 1 & result2 == 1
        except Exception as e:
            print(e)
            raise

    def get_handshake_check_lb(self,src_code,tar_code,check_file):
        # 读取EXCEL中内容到数据库中
        wb = xlrd.open_workbook(check_file)
        sh = wb.sheet_by_index(4)
        nrows = sh.nrows  # 行数
        src_check = ""
        tar_check = ""
        src_flag =0
        tar_flag =0
        for i in range(1, nrows):
            if src_flag ==1 and tar_flag==1:
                break
            elif src_flag==0 and src_code == sh.cell(i, 2).value:
                    src_check = sh.cell(i,3).value
                    src_flag =1
            elif tar_flag==0 and tar_code == sh.cell(i, 2).value:
                 tar_check = sh.cell(i,3).value
                 tar_flag =1

        return src_check.strip(" "),tar_check.strip(" ")



    # 进行一次拍照翻译
    def ocr_trans_lb(self, ocrlang):
        # 切换到拍照翻译使用一次拍照
        self.d.app_start("com.iflytek.easytrans.ocr")
        time.sleep(3)
        try:
            if not self.d(text=ocrlang):
                self.d(resourceId="com.iflytek.easytrans.ocr:id/iv_select").click_exists(10)
                self.d(resourceId="com.iflytek.easytrans.ocr:id/tv_src_language", text=ocrlang).click_exists(10)
            self.d(resourceId="com.iflytek.easytrans.ocr:id/iv_capture").click_exists(10)
            # self.d(resourceId="com.iflytek.easytrans.ocr:id/iv_translate").click_exists(10)
            time.sleep(5)

        except Exception as e:
            print(e)
            raise

    def text_trans_lb(self,keytype = 'cn',modify_text=""):
        try:

            self.d(resourceId="com.iflytek.easytrans.launcher:id/text_container").long_click()
            self.d(resourceId = "com.iflytek.easytrans.launcher:id/modify_rec_tv").click()
            ori_text = self.d(resourceId = "com.iflytek.easytrans.launcher:id/modify_edt").get_text()
            modify_text=str(modify_text)
            if modify_text=="":
                if keytype == 'cn':
                    modify_text =ori_text + "测试原文修改"
                else:
                    modify_text = ori_text +"test revise original text"

            self.d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
            self.d.clear_text()
            self.d.send_keys(modify_text)  # adb广播输入
            time.sleep(1)
            self.d.set_fastinput_ime(False)  # 切换成正常的输入法
            self.d(resourceId = "com.iflytek.easytrans.launcher:id/advanced_setting_iv").click()
        except Exception as e:
            print(e)
            raise

    # 对最新翻译记录进行原文修改，并返回
    def check_text_trans_lb(self,keytype = 'cn',isinit=True, modify_text="test"):
        try:

            self.text_trans_lb(keytype,modify_text)
            if  not isinit:
                self.check_toast(prepareText)
                time.sleep(10)
                self.d(resourceId="com.iflytek.easytrans.launcher:id/advanced_setting_iv").click()
            esr,trans = self.getEsr_and_trans_Content_lb(keytype)
            if str(esr) in str(modify_text) :
                return 1
            else:
                print("modify_test:{0}".format(modify_text))
                print("esr:{0}".format(esr))
                return 0
        except Exception as e:
            print(e)
            raise


    # 根据esr或trans内容查找翻译记录进行原文修改,前提条件：已经进入翻译记录页
    def text_trans_by_content(self,content,keytype = 'cn',isinit=True, modify_text=""):
        try:

            if not self.transRecord_exist_lb():
                return 0
            else:
                # 从父布局中根据text查找目标控件并点击
                self.d(className="android.support.v7.widget.RecyclerView",
                       resourceId="com.iflytek.easytrans.launcher:id/rv") \
                    .child_by_text(content, allow_scroll_search=True, className="android.widget.TextView").long_click()
                time.sleep(1)
                self.d(resourceId="com.iflytek.easytrans.launcher:id/modify_rec_tv").click()
                ori_text = self.d(resourceId="com.iflytek.easytrans.launcher:id/modify_edt").get_text()

                if modify_text=="":
                    if keytype == 'cn':
                        modify_text =ori_text + "测试原文修改"
                    else:
                        modify_text = ori_text +"test revise original text"
                self.d.set_fastinput_ime(True)  # 切换成FastInputIME输入法
                self.d.clear_text()
                self.d.send_keys(modify_text)  # adb广播输入
                time.sleep(1)
                self.d.set_fastinput_ime(False)  # 切换成正常的输入法
                self.d(resourceId="com.iflytek.easytrans.launcher:id/advanced_setting_iv").click()
                if not isinit:
                    self.check_toast(prepareText)
                    time.sleep(10)
                    self.d(resourceId="com.iflytek.easytrans.launcher:id/advanced_setting_iv").click()
                esr, trans = self.getEsr_and_trans_Content_lb()
                if modify_text in esr:
                    return 1
                else:
                    return 0

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

    # pressedKey=1 代表白键翻译
    def check_recordPressedKey_lb(self, check=[]):
        try:
            sql = "select pressedKey from TRANS_INFO_DB ORDER BY id desc;"
            result = self.query_db("/data/data/com.iflytek.easytrans.launcher/databases/trans_record.db", sql)
            if result == check:
                return 1
            else:
                return 0

            # keys = keyTypes.split("_")
            # print(keys)

            #
            # if len(keys)==1:
            #     if keys[0] == 'cn' and len(result)==1 and result[0]==(1):
            #         return 1
            #     elif len(result)==1 and result[0]==(2):
            #         return 1
            #     else:
            #         return 0
            # else:
            #     if len(result)<2:
            #         return 0
            #     else:
            #         r1 =0
            #         r2=0
            #         for key in keys:
            #             if key == 'cn' and (1)  in result:
            #                 r1 =0
            #             elif key == 'foreign' and (2)  in result:
            #                 return 0
            #         return 1

        except Exception as e:
            print(e)
            raise

    # 判断播放音频是否被打断
    def check_play_state_lb(self, piid="",timeout =1):
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
        return self.play_state


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


    def transRecord_exist_lb(self,type=""):
        try:
            resourceId = 'com.iflytek.easytrans.launcher:id/text_container'
            time.sleep(1)
            if self.d(text = "下拉查看翻译记录").exists():
                self.d.swipe(0.5,0.19,0.5,0.5,duration=0.01)

            if type=="离线结果":
                if self.d(resourceId= "com.iflytek.easytrans.launcher:id/offline_tv",text = "离线结果").exists(timeout =10):
                    return  True
                else:
                    return False
            elif type == "在线结果":
                if ( self.d(resourceId=resourceId).count - self.d(resourceId= "com.iflytek.easytrans.launcher:id/offline_tv",text = "离线结果").count)>0:
                    return True
            else:
                if self.d(resourceId=resourceId).count > 0:
                    return True
            print("no trans record\n")
            return False
        except Exception as e:
            print(e)
            raise



    def record_feedback_lb(self, tag="离线结果"):
        try:
            # 进入语音翻译并下拉出翻译记录
            self.backVoice_by_key()
            if self.d(text="下拉查看翻译记录").exists():
                self.d.swipe(0.5, 0.1, 0.5, 0.9, duration=0.1)
            if tag == "离线结果":
                if self.d(resourceId = "com.iflytek.easytrans.launcher:id/offline_tv").exists():
                    self.d(resourceId = "com.iflytek.easytrans.launcher:id/offline_tv").\
                        sibling(resourceId = "com.iflytek.easytrans.launcher:id/text_container").long_click()
                    self.d(resourceId="com.iflytek.easytrans.launcher:id/feedback_tv").click()
                    return
            else:
                self.d(resourceId = "com.iflytek.easytrans.launcher:id/text_container").long_click()
                self.d(resourceId="com.iflytek.easytrans.launcher:id/feedback_tv").click()
                return
        except Exception as e:
            print(e)
            raise


    # LB握手礼资源检查
    def check_handshake_lb(self,data,check_file):
        try:
            self.backVoice_by_key()
            self.switchLanguage_lb(data["srcLangName"], data["targetLangName"], 0.5)
            self.d(resourceId = "com.iflytek.easytrans.launcher:id/shake_hands_imv").click()
            hs_src = self.d(resourceId = "com.iflytek.easytrans.launcher:id/shake_hands_top_content").get_text()
            hs_tar = self.d(resourceId = "com.iflytek.easytrans.launcher:id/shake_hands_bottom_content").get_text()

            hs_src_check,hs_tar_check = self.get_handshake_check_lb(data["srcLangCode"],data["targetLangCode"],check_file)

            if hs_src != hs_src_check or hs_tar!= hs_tar_check:
                print("hs_src:{0} hs_tar:{1}\n".format(hs_src, hs_tar))
                print("hs_src_check:{0} hs_tar_check:{1}".format(hs_src_check.strip("."), hs_tar_check))
                return 0
            else:
                return 1
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
        # 删除数据库文件，避免对下次结果造成影响
        os.popen("del {0}".format(save_dir))
        return result

    #从翻译机pull数据库到本地然后进行数据插入，最后push
    def change_db(self,dir,sqls):
        os.popen("adb -s {0} root".format(self.deviceId))
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
            self.backHomeLB()
            print(" back home")
            self.d(text = "语音翻译",resourceId = "com.iflytek.easytrans.launcher:id/tv_voice_trans").click()


    def wait_trans_end(self,timeout=20):
        self.d(resourceId="com.iflytek.easytrans.launcher:id/trans_waiting_iv").wait_gone(10)
        # 等待出现播报小喇叭代表翻译结束
        self.d(resourceId='com.iflytek.easytrans.launcher:id/play_iv').wait(True,timeout)



# if __name__ == '__main__':
#     dir = "/data/data/com.iflytek.easytrans.launcher/databases/trans_record.db"
#     sql = sql = "select pressedKey from TRANS_INFO_DB ORDER BY id desc limit 1;"
#     deviceId = "35a9c5a0"
#     save_dir = os.path.join(os.getcwd(), dir.split("/")[-1])
#     os.popen("adb -s {0} pull {1} {2} ".format(deviceId, dir, os.getcwd()))
#     time.sleep(3)
#     conn = sqlite3.connect(save_dir)
#     c = conn.cursor()
#
#     c.execute(sql)
#     # conn.commit()
#     result = c.fetchall()
#     conn.close()
#     print(result)
#     # 删除数据库文件，避免对下次结果造成影响
#     os.popen("del {0}".format(save_dir))


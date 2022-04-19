""""
源代码
    1、录音
    2、语音识别 （将录音内容进行语音识别转成文字）
    3、接入图灵机器人（将文字发送给机器人获得回复）
    4、语音合成 （将回复的文字进行语音合成）
    5、播放语音
"""
import speech_recognition as sr   #pyaudio SpeechRecognition模块

def rec(rate=16000):     #从系统麦克风拾取音频数据，采样率为 16000
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say:")  #这里会打印please say:，提示你说话进行录音
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:   #把采集到的音频数据以 wav 格式保存在当前目录下的recording.wav 文件
        f.write(audio.get_wav_data())
    return 1


rec()  #运行rec函数，录制音频



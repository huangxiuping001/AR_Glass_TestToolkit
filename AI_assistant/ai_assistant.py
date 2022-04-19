""""
1、录音 （将说话人的声音录入）
2、语音识别 （将录音内容进行语音识别转成文字）
3、接入图灵机器人（将文字发送给机器人获得回复）
4、语音合成 （将回复的文字进行语音合成）
5、播放语音（将合成的语音播放出来）
"""
import speech_recognition as sr
from aip import AipSpeech
import requests
import json

import pygame

#01录音
def rec(rate=16000):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=rate) as source:
        print("please say something")
        audio = r.listen(source)

    with open("recording.wav", "wb") as f:
        f.write(audio.get_wav_data())

    return 1

#02语音识别
APP_ID = '25984923'
API_KEY = 'cwucKGfTZeN8CkOmlRU0z2pE'
SECRET_KEY = 'MCFIfiXHLWTaHbshizEwPtxcN7E00Utj'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
def listen():
    with open('recording.wav', 'rb') as f:
        audio_data = f.read()

    results = client.asr(audio_data, 'wav', 16000, {
        'dev_pid': 1537,
    })
    if 'result' in results:
        print("you said: " + results['result'][0])
        return results['result'][0]
    else:
        print("出现错误，错误代码：" , results['err_no'])

#03调用图灵机器人
TURING_KEY = "35c7652f6a0c4f8393a62d3519fc4799"
URL = "http://openapi.tuling123.com/openapi/api/v2"
HEADERS = {'Content-Type': 'application/json;charset=UTF-8'}
def robot(text=""):
    data = {
        "reqType": 0,
        "perception": {
            "inputText": {
                "text": ""
            },
            "selfInfo": {
                "location": {
                    "city": "成都",
                    "street": "中国华商金融中心T118楼"
                }
            }
        },
        "userInfo": {
            "apiKey": '35c7652f6a0c4f8393a62d3519fc4799',
            "userId": "123"
        }
    }

    data["perception"]["inputText"]["text"] = text
    response = requests.request("post", URL, json=data, headers=HEADERS)
    response_dict = json.loads(response.text)

    result = response_dict["results"][0]["values"]["text"]
    print("the AI said: " + result)
    return result

#04语音合成
def speak(text=""):
    result = client.synthesis(text, 'zh', 1, {
        'spd': 4,
        'vol': 5,
        'per': 4,
    })

    if not isinstance(result, dict):
        with open('audio.mp3', 'wb') as f:
            f.write(result)

#05播放音频
def play():
    pygame.mixer.init()
    pygame.mixer.music.load("D:/AR_Glass_Toolkit/AI_assistant/audio.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass
    pygame.mixer.music.unload()

if __name__ == "__main__":
    while True:
        rec()  # 保存录音文件：recording.wav
        text = listen()  # 自动打开录音文件recording.wav进行识别,返回 识别的文字存到text
        if '结束程序' in text:  #设置了一个结束语，说“结束程序”的时候就结束
            break
        text_1 = robot(text)  # 将text中的文字发送给机器人，返回机器人的回复存到text_1
        speak(text_1)  # 将text_1中机器人的回复用语音输出，保存为audio.mp3文件
        play() #播放audio.mp3文件

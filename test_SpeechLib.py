# coding:utf-8
"""
Created on 2022年4月15日
@author: 黄秀平
Content：将文本内容转换为音频的 方法2
"""
from comtypes.client import CreateObject
from comtypes.gen import SpeechLib

engine = CreateObject('SAPI.SpVoice') # 创建引擎对象
stream = CreateObject('SAPI.SpFileStream') # 输出到目标对象流的对象
infile = 'demo.txt'
outfile = 'demo_audio.wav'
stream.open(outfile,SpeechLib.SSFMCreateForWrite)
# engine.AudioOutputStream = stream # 将音频文件存下来

# 读取文件
f = open(infile,'r',encoding='utf-8')
theText = f.read()
f.close()

engine.speak(theText)
stream.close() # 将音频输出流关闭


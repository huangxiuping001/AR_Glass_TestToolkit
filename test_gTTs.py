# coding:utf-8
from gtts import gTTS  #Google Text-to-Speech，会连接超时，使用vpn可以
import os

tts = gTTS('你好，小纪')
tts.save('hello.mp3')
os.system("mpg321 hello.mp3")
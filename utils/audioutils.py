#-*-coding: UTF-8 -*-

import wave

class AudioUtils:

    # 获取音频文件播放时长  支持 wav pcm mp3等格式  其他未尝试过
    @staticmethod
    def getAudioPlayTime(path = ''):
        if path == '':
            print("path is null, return")
            return 1

        with wave.open(path, 'rb') as f:
            f = wave.open(path)

            print(f.getparams())
            print(str(type(f.getparams())))

            nframs = f.getparams().nframes
            framerate = f.getparams().framerate

        consum_time = nframs / framerate
        print(str(consum_time))
        return consum_time

if __name__ == '__main__':
    utils = AudioUtils()

    utils.getWavAudioPlayTime("E:\\python_home\\translator__android__test_toolkit\\audio\mp3\\7.mp3")
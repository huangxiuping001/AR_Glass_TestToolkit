from pygame import mixer

mixer.init() # initiate the mixer instance
mixer.music.load(r'D:\AR_Glass_TestToolkit\start.mp3') # loads the music, can be also mp3 file.
mixer.music.play() # plays the music
mixer.music.stop()

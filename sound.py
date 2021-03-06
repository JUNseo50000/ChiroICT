from gtts import gTTS
from time import sleep
import os
import pyglet

'''
https://gtts.readthedocs.io/en/latest/
https://github.com/pndurette/gTTS/issues/26
'''


def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = './temp.mp3'
    tts.save(filename)

    music = pyglet.media.load(filename, streaming=False)
    music.play()

    sleep(music.duration)
    os.remove(filename)


test = '잘 목소리가 나오는지 테스트 하는 방법입니다. you got it?'
speak(test)



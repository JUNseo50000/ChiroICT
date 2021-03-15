# import winsound

# winsound.Beep(262 ,2000)
# winsound.Beep(294 ,2000)
# winsound.Beep(330 ,2000)




# # rbpi는 linux로 돌아가니까 리눅스버젼은 playsound에서 직접 찾아보자.
# def _playsoundWin(sound, block = True):
#     '''
#     Utilizes windll.winmm. Tested and known to work with MP3 and WAVE on
#     Windows 7 with Python 2.7. Probably works with more file formats.
#     Probably works on Windows XP thru Windows 10. Probably works with all
#     versions of Python.

#     Inspired by (but not copied from) Michael Gundlach <gundlach@gmail.com>'s mp3play:
#     https://github.com/michaelgundlach/mp3play

#     I never would have tried using windll.winmm without seeing his code.
#     '''
#     from ctypes import c_buffer, windll
#     from random import random
#     from time   import sleep
#     from sys    import getfilesystemencoding

#     def winCommand(*command):
#         buf = c_buffer(255)
#         command = ' '.join(command).encode(getfilesystemencoding())
#         errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
#         if errorCode:
#             errorBuffer = c_buffer(255)
#             windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
#             exceptionMessage = ('\n    Error ' + str(errorCode) + ' for command:'
#                                 '\n        ' + command.decode() +
#                                 '\n    ' + errorBuffer.value.decode())
#             raise PlaysoundException(exceptionMessage)
#         return buf.value

#     alias = 'playsound_' + str(random())
#     winCommand('open "' + sound + '" alias', alias)
#     winCommand('set', alias, 'time format milliseconds')
#     # durationInMS = winCommand('status', alias, 'length')
#     durationInMS = b'5913' # 밀리세컨드단위로 이렇게 표기하는 것임.
#     winCommand('play', alias, 'from 0 to', durationInMS.decode())
#     print(durationInMS)

#     if block:
#         sleep(float(durationInMS) / 1000.0)


# _playsoundWin("Piano.mf.C4.aiff"); _playsoundWin("Piano.mf.D4.aiff")




# import pygame

# pygame.init()
# pygame.mixer.init()
# firstSound = pygame.mixer.music('./sound1.mp3')
# secondSound = pygame.mixer.music('./sound2.mp3')
# firstSound.play()
# secondSound.play()





# import pygame, time

# pygame.init()
# pygame.mixer.init()

# pygame.mixer.music.load('sound1.mp3')
# pygame.mixer.music.play()
# time.sleep(1)
# pygame.mixer.music.load('sound2.mp3')
# pygame.mixer.music.play()
# time.sleep(1)
# pygame.mixer.music.load('sound3.mp3')
# pygame.mixer.music.play()
# pygame.mixer.music.fadeout(2000)
# time.sleep(5)






# import pygame, time

# pygame.mixer.pre_init(44100, 16, 2, 4096)
# # pygame.mixer.pre_init()
# pygame.init()
# pygame.mixer.init()
# # mp3파일은 못열고 wav파일은 연다.
# sound1 = pygame.mixer.Sound('test1.wav')
# sound2 = pygame.mixer.Sound('test2.wav')
# # pygame.mixer.Channel(0).play(sound1)
# pygame.mixer.Channel.play(sound1)
# time.sleep(0.5)
# pygame.mixer.Channel.play(sound2)


# time.sleep(5)





# import pygame
# import os
# pygame.mixer.init()
# os.getcwd() # Log this line.
# soundObj = pygame.mixer.Sound('test1.wav')
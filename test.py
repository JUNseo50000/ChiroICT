# import random
# from threading import Thread
# import multiprocessing
# multiprocessing.set_start_method('spawn')

# def work1():
#     while True:
#         print("ok")

# def work2():
#     while True:
#         print("@@@@@@@@@@@@@@@")

# # work1 = multiprocessing.Process(target=work1, args=())
# # work2 = multiprocessing.Process(target=work2, args=())
# work1 = Thread(target=work1, args=())
# work2 = Thread(target=work2, args=())

# if __name__ == '__main__':
#     work1.start()
    
#     while True:
#         print("@@@@@@@@@@@@@@@")


# a = set()
# a.add(3)
# a.add(4)

# print(a)
# b = a.pop()
# print(b)
# print(a)


from midiutil.MidiFile import MIDIFile
import constants
import time

print("[INFO] Sequencing MIDI")
midi = MIDIFile(1)
track = 0
time = 0
channel = 0
volume = 100

midi.addTrackName(track, time, "Track")
midi.addTempo(track, time, 60)

duration = 2
pitch = constants.pitch2MIDI["E4"]
midi.addNote(track, channel, pitch, time, duration, volume)
time += duration


pitch = constants.pitch2MIDI["D4"]
time += duration
midi.addNote(track, channel, pitch, time, duration, volume)
time += duration


# time += duration

'''
time이 22인데 mid파일은 14초였다.
22 * 0.666을 하면 14.54가 나온다.
'''

print(time)
binfile = open("output.mid", 'wb')
midi.writeFile(binfile)
binfile.close()
print("TEST")

bgasd = 3
print(time.time())
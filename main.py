import time, os
import keyboard

from threading import Thread
import multiprocessing
from midiutil.MidiFile import MIDIFile

import pianokeyboard
import led
import constants

# class init
pianokeyboard = pianokeyboard.PianoKeyboard('Resources/PianoSamples')

### piano mode state ###
guide_state = False
record_state = False
marking_state = False



'''
TODO
안드로이드로 py파일의 state를 바꾸는 것.
라즈베리 전원 들어오면 바로 실행되게 하는 것. -> 어렵지 않음.
'''


class Note:
    def __init__(self, pitch_list, duration):
        self.pitch = pitch_list
        self.duration = duration

    def addStarttime(self, starttime):  
        self.starttime = starttime

    def addEndtime(self, endtime):    
        self.endtime = endtime

def convertNote(path):
    temp_datas = []
    with open(path,"r") as f :
    # with open("./music/output.txt","r") as f :
        # [g3,0.5 z,1 a3,0.5 ... f3,1 ]
        temp_datas = f.read().split(" ")
    
    notes = []
    for temp_data in temp_datas:
        # "" is a last element of temp_datas
        if temp_data != "":
            temp_note = temp_data.split(',')

            # note
            duration = temp_note[-1]
            pitch_list = []
            for ix in range(len(temp_note) - 1):
                pitch = temp_note[ix]
                pitch_list.append(pitch)
            note = Note(pitch_list, duration)
            notes.append(note)

    return notes

def getStandard_time(speed):
    if speed == 'Moderato':
        standard_time = 0.666
    # 120 bpm
    elif speed == 'Allegro':
        standard_time = 0.5
    # Moderato
    else:
        standard_time = 0.666
    return standard_time

def guide_mode(notes, speed='Moderato'):
    # Moderato 보통빠르게 BPM 90 -> Quarter note per 0.666..second
    standard_time = getStandard_time(speed)

    for note in notes:
        led.guideLEDmode(note)

    global guide_state
    guide_state = False

def record_mode(pressing_keyboard_set):
    record_list = []
    past_time = time.time()
    current_time = time.time()

    # while True:
    # todo : change break condition
    while len(record_list) <= 50:
        # # memorry limit
        # if len(record_list) >= 1000:
        #     record_state = False

        # print(len(pressing_keyboard_set))

        # rest
        if len(pressing_keyboard_set) == 0:
            past_time = time.time()

            while True:
                # 이게 없으면 과부화때문인지 돌아가지 않는다..
                time.sleep(0.01)

                if len(pressing_keyboard_set) != 0:
                    current_time = time.time()
                    duration = current_time - past_time
                    note = Note('z', duration)
                    record_list.append(note)
                    break
        # note
        else:
            num_pitch = len(pressing_keyboard_set)
            past_time = time.time()
            pitch_list = []
            for ix in pressing_keyboard_set:
                pitch = constants.index2pitch[ix]
                pitch_list.append(pitch)

            
            while True:
                time.sleep(0.01)

                if len(pressing_keyboard_set) != num_pitch:
                    current_time = time.time()
                    duration = current_time - past_time
                    note = Note(pitch_list, duration)
                    # note = Note(pitch_list[0], duration)

                    # for ix in range(len(pitch_list) - 1):
                    #         note.addPitch(pitch_list[ix + 1])

                    record_list.append(note)
                    break

    # convert to MIDI file
    midi = MIDIFile(1)
    track = 0
    record_time = 0
    channel = 0
    volume = 100

    midi.addTrackName(track, record_time, "Track")
    # 60 : bpm -> 1beat for 1second
    midi.addTempo(track, record_time, 60)

    for note in record_list:
        # rest
        if note.pitch[0] == 'z':
            record_time += note.duration
        # single note
        elif len(note.pitch) == 1:
            pitch = constants.pitch2MIDI[note.pitch[0]]
            duration = note.duration
            midi.addNote(track, channel, pitch, record_time, duration, volume)
            record_time += duration
        # harmony
        else:
            duration = note.duration
            for ix_pitch in note.pitch:
                pitch = constants.pitch2MIDI[ix_pitch]
                midi.addNote(track, channel, pitch, record_time, duration, volume)
            record_time += duration                

    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()

    print("Record Done")
    global record_state
    record_state = False
    

def marking_mode(compared_notes, pressing_keyboard_set, speed='Moderato'):
    past_time = None
    current_time = None
    marking_list = []

    # while True: 
    while len(marking_list) < 5: 

        time.sleep(0.01)


        if len(pressing_keyboard_set) != 0:
            num_pitch = len(pressing_keyboard_set)
            past_time = time.time()
            pitch_list = []
            for ix in pressing_keyboard_set:
                pitch = (constants.index2pitch[ix]).lower()
                pitch_list.append(pitch)
            

            while True:
                time.sleep(0.01)

                if  len(pressing_keyboard_set) != num_pitch:
                    current_time = time.time()
                    duration = current_time - past_time
                    # deal as harmony
                    # 인식률이 완벽하진 않은데..
                    if duration <= 0.05:
                        break
                    else:
                        note = Note(pitch_list, duration)
                        marking_list.append(note)
                        break

    print("\nMarking Done\n")
    # for note in marking_list:
    #     print(note.pitch)

    # compare with compared_notes
    ix = 0
    standard_time = getStandard_time(speed)
    for order, comparing_note in enumerate(marking_list):
        # do not count about rest
        while compared_notes[ix].pitch[0] == 'z':
            ix += 1
        compared_note = compared_notes[ix]
        ix += 1
        # compare about pitch
        if comparing_note.pitch != compared_note.pitch:
            print("-------------------------------------------")
            print("Wrong pressing about " + str(order + 1) + "th note.")
            print("You press the " + str(comparing_note.pitch))
            print("Origin note is  " + str(compared_note.pitch))
            print("-------------------------------------------")
            continue
        # compare about duration
        diff_duration = float(comparing_note.duration) - float(compared_note.duration) * float(standard_time)
        if diff_duration >= 0.3:
            print("Too long press about " + str(order + 1) + "th note.")
        elif diff_duration <= -0.3:
            print("Too short press about " + str(order + 1) + "th note.")

    print("Done marking mode")
    global marking_state
    marking_state = False

### main loop ###
def loop():
    while True:
        if guide_state:
            # multi processing
            guide_mode.start()
            while True:
                pianokeyboard.piano_mode()
                # 이상하게 계속 True로 있다. 어떻게 종료시킬지 생각해보자.
                if not guide_state:
                    print("IN")
                    break

        elif record_state:
            record_mode.start()
            while True:
                pianokeyboard.piano_mode()
                led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)
                if not record_state:
                    break

        elif marking_state:
            marking_mode.start()
            while True:
                pianokeyboard.piano_mode()
                # led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)
                if not marking_state:
                    break
        else:
            pianokeyboard.piano_mode()
            led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)




if __name__ == '__main__':

    notes = convertNote('./music/output.txt')
    guide_mode = Thread(target = guide_mode, args=(notes, ))
    record_mode = Thread(target = record_mode, args=(pianokeyboard.pressing_keyboard_set, ))
    marking_mode = Thread(target = marking_mode, args=(notes, pianokeyboard.pressing_keyboard_set, ))
    print("Setup complete")

    loop()
import time, os
import keyboard
import bluetooth
from threading import Thread
from midiutil.MidiFile import MIDIFile

import pianokeyboard
import led
import constants

# keyboard class init
pianokeyboard = pianokeyboard.PianoKeyboard('Resources/PianoSamples')

### piano mode state ###
guide_state = False
record_state = False
marking_state = False
default_state = True

record_list = []

'''
TODO
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

def saveNote(path):
    # todo
    pass

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

def guide_mode(speed='Moderato'):
    notes = convertNote('./music/output.txt')
    # Moderato 보통빠르게 BPM 90 -> Quarter note per 0.666..second
    standard_time = getStandard_time(speed)

    for note in notes:
        led.guideLEDmode(note)

    global guide_state
    guide_state = False

def record_mode(pressing_keyboard_set):
    past_time = time.time()
    current_time = time.time()
    record_limit = 100

    global record_list
    while len(record_list) <= record_limit:
        # # memorry limit
        # if len(record_list) >= 1000:
        #     record_state = False

        # print(len(pressing_keyboard_set))

        # rest
        if len(pressing_keyboard_set) == 0:
            past_time = time.time()

            while True:
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

                    record_list.append(note)
                    break

# convert to MIDI file
def conver2MIDI():
    midi = MIDIFile(1)
    track = 0
    record_time = 0
    channel = 0
    volume = 100

    midi.addTrackName(track, record_time, "Track")
    # 60 : bpm -> 1beat for 1second
    midi.addTempo(track, record_time, 60)

    global record_list
    for note in record_list:
        # rest
        if note.pitch[0] == 'z':
            record_time += note.duration
        # note
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

    # clera list
    record_list = []


def marking_mode(pressing_keyboard_set, speed='Moderato'):
    past_time = None
    current_time = None
    marking_list = []
    limit_notes = 1000

    # while True: 
    while len(marking_list) < limit_notes: 

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
                    if duration <= 0.06:
                        break
                    else:
                        note = Note(pitch_list, duration)
                        marking_list.append(note)
                        break

    print("\nMarking Done\n")

# compare with compared_notes
def checkMarking():
    compared_notes = convertNote('./music/output.txt')

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


def receiveBluetooth(client_socket):
    b_data = client_socket.recv(1024)
    data = b_data.decode('utf-8')
    print(data)

    global guide_state
    global marking_state
    global record_state
    global default_state

    if data == "start default_mode":
        default_state = True
    elif data == "end default_mode":
        default_state = False

    elif data == "get the sheets":
        saveNote()

    elif data == "start guide_mode":
        guide_state = True
    elif data == "end guide_mode":
        guide_state = False

    elif data == "start marking_mode":
        marking_state = True
    elif data == "end marking_mode":
        marking_state = False

    elif data == "start record_mode":
        record_state = True
    elif data == "end record_mode":
        record_state = False


### main loop ###
def loop(client_socket):
    while True:
        receiveBluetooth(client_socket)

        if guide_state:
            T_guide_mode.start()
            T_receiveBluetooth.start()
            while True:
                pianokeyboard.piano_mode()
                if not guide_state:
                    break

        elif record_state:
            T_record_mode.start()
            T_receiveBluetooth.start()
            while True:
                pianokeyboard.piano_mode()
                led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)
                if not record_state:
                    conver2MIDI()
                    break
            T_record_mode.join()
            T_receiveBluetooth.join()

        elif marking_state:
            T_marking_mode.start()
            T_receiveBluetooth.start()
            while True:
                pianokeyboard.piano_mode()
                led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)
                if not marking_state:
                    checkMarking()
                    break
            T_marking_mode.join()
            T_receiveBluetooth.join()

        else:
            T_receiveBluetooth.start()
            while True:
                pianokeyboard.piano_mode()
                led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)
                if not default_state:
                    break
                T_receiveBluetooth.join()




if __name__ == '__main__':
    # bluetooth setting
    server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM )
    port = 1
    server_socket.bind(("",port))
    server_socket.listen(port)
    client_socket,address = server_socket.accept()
    client_socket.send("bluetooth connected!")


    # multi threading
    T_guide_mode = Thread(target = guide_mode, args=( ))
    T_record_mode = Thread(target = record_mode, args=(pianokeyboard.pressing_keyboard_set, ))
    T_marking_mode = Thread(target = marking_mode, args=(pianokeyboard.pressing_keyboard_set, ))
    T_receiveBluetooth = Thread(target = receiveBluetooth, args=(client_socket,))

    print("Setup complete")

    loop(client_socket)

    client_socket.close()
    server_socket.close()
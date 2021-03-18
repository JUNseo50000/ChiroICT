import time, os
import keyboard
from threading import Thread

import pianokeyboard
import led

# class init
pianokeyboard = pianokeyboard.PianoKeyboard('Resources/PianoSamples')

### piano mode state ###
guide_state = False
record_state = True
marking_state = False


record_list = []
# for preventing continuous press
temp_pressing_set = set()


'''
TODO
레코드모드


'''


class Note:
    def __init__(self, pitch, duration):
        self.pitch = []
        self.pitch.append(pitch)
        self.duration = duration

    def addStarttime(self, starttime):  
        self.starttime = starttime

    def addEndtime(self, endtime):    
        self.endtime = endtime

    def addPitch(self, pitch):
        self.pitch.append(pitch)


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

            # single note
            if len(temp_note) == 2:
                note = Note(temp_note[0], temp_note[1])
                notes.append(note)
            # harmony
            else:
                note = Note(temp_note[0], temp_note[-1])
                for i in range(len(temp_note) - 2):
                    note.addPitch(temp_note[i + 1])
                    i += 1
                notes.append(note)

    return notes


def guide_mode(notes, speed='Moderato'):
    # Moderato 보통빠르게 BPM 90 -> Quarter note per 0.666..second
    standard_time = None
    if speed == 'Moderato':
        standard_time = 0.666
    # 120 bpm
    elif speed == 'Allegro':
        standard_time = 0.5
    # Moderato
    else:
        standard_time = 0.666

    for note in notes:
        led.guideLEDmode(note)

    guide_state = False


def record_mode(pressing_keyboard_set):
    # memorry limit
    if len(record_list) >= 1000:
        record_state = False

    past_time = None
    current_time = None

    while True:
        if len(pressing_keyboard_set) == 0:
            past_time = time.time()

            # 이게 없으면 과부화때문인지 돌아가지 않는다..
            time.sleep(0.1)

            if len(pressing_keyboard_set) != 0:
                print(len(pressing_keyboard_set))

    #     # not deleted temp_pressing_set
    #     remain_set = temp_pressing_set - pressing_keyboard_set

    #     if len(remain_set) != 0:
    #         for ix in remain_set:
    #             temp_pressing_set.remove(ix)
    #             # duration
    #             current_time = time.time()
    #             # duration = current_time - past_time
    #             # # pitch
    #             # # todo : change
    #             # pitch = 60

    #             # note = Note(pitch, duration)
    #             # record_mode.append(note)

    # elif  len(pressing_keyboard_set) == 1:
    #     for ix in pressing_keyboard_set:
    #         if ix in temp_pressing_set:
    #             pass
    #         else:
    #             temp_pressing_set.add(ix)
    #             past_time = time.time()

    # # 여기서 화음을 넣더라도, 건반을 뗄 떼 list에 추가하기가 너무 어려워지네..
    # else:
    #     pass



def marking_mode():
    # input will be note_source
    print("MARKING MODE")

    '''
    record_mode에서 누른 건반의 정보와 시간을 기억하는
    알고리즘을 생각했다면 이는 어렵지 않다.
    시간은 무시하고 어떤 순서로 눌렀는지만 가져온다.
    그리고 누른 건반을 리스트로 저장하고 source와 비교한다.
    여기서 틀리는 것은 처리하기 쉽지만, 빼먹는 것은 또 생각을 해봐야 한다.
    일단 생각 나는건, 빼먹었으면 배열의 다음 위치로 이동해서, 비교하는 것.
    그런데 이건 그 다음것도 같았을 때 등 문제가 경우의수가 너무 많다.

    그리고 몇번째 것이 틀렸는가는 알려주기 쉽지만 그것의 악보에서의 위치는?

    아니면 그냥 틀리면 삐 처리 하는 것을 생각해볼까..
    '''



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

        elif marking_state:
            marking_mode()
        else:
            pianokeyboard.piano_mode()
            led.defaultLEDmode(pianokeyboard.pressing_keyboard_set)




if __name__ == '__main__':

    notes = convertNote('./music/output.txt')

    guide_mode = Thread(target = guide_mode, args=(notes, ))
    record_mode = Thread(target = record_mode, args=(pianokeyboard.pressing_keyboard_set, ))

    loop()
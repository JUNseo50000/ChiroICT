import time
import pianokeyboard
import constants
# import RPi.GPIO as GPIO

past_time = None
current_time = None
# -1 is initial value for comparsion : current_pin_nums[0]
current_pin_nums = [-1]
temp_pressing_set = set()

# setup
# for key in constants.LED_pin.keys():
#     GPIO.setup(constants.LED_pin[key], GPIO.OUT)




def turnonLED(index):
    # GPIO.output(constants.index2LEDpin[index], GPIO.HIGH)
    print("trun on " + str(constants.index2LEDpin[index]) + "LED")

def turnoffLED(index):
    # GPIO.output(constants.index2LEDpin[index], GPIO.LOW)
    print("trun off " + str(constants.index2LEDpin[index]) + "LED")


def defaultLEDmode(pressing_keyboard_set):
    for ix in pressing_keyboard_set:
        if ix in temp_pressing_set:
            pass
        else:
            temp_pressing_set.add(ix)
            turnonLED(ix)
    
    # pull out of keyboard but still not remove the ix in temp_pressing_set
    if len(temp_pressing_set) > len(pressing_keyboard_set):
        # set difference
        for pressoff_ix in (temp_pressing_set - pressing_keyboard_set):
            turnoffLED(pressoff_ix)
            temp_pressing_set.remove(pressoff_ix)
            break
            

def guideLEDmode(note, standard_time = 0.666):
    # single note
    if (len(note.pitch) == 1):
        pitch = (note.pitch[0]).upper()
        duration = note.duration

        # rest
        if pitch == 'z':
            time.sleep(float(duration) * float(standard_time))
        # note
        else:
            for comparing_pitch in constants.keyboard_pin:
                if pitch == comparing_pitch:
                    turnonLED(constants.pitch2index[pitch])
                    time.sleep(float(duration) * float(standard_time))
                    turnoffLED(constants.pitch2index[pitch])
                    break
    # harmonoy
    else:
        for pitch in note.pitch:
            pitch = pitch.upper()
            duration = note.duration

            for comparing_pitch in constants.keyboard_pin:
                if pitch == comparing_pitch:
                    turnonLED(constants.pitch2index[pitch])
                    break

        time.sleep(float(duration) * float(standard_time))
        for pitch in note.pitch:
            pitch = pitch.upper()
            turnoffLED(constants.pitch2index[pitch])
        


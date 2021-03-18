import time
import pianokeyboard
import constants
# import RPi.GPIO as GPIO

past_time = None
current_time = None
# -1 is initial value for comparsion : current_pin_nums[0]
current_pin_nums = [-1]

# setup
# GPIO.setup(constants.constants["LED_C4"], GPIO.OUT)
# GPIO.setup(constants.constants["LED_D4"], GPIO.OUT)


temp_pressing_set = set()

def turnonLED(pin_number):
    # GPIO.output(index2pin[pin_number], GPIO.HIGH)
    print("trun on " + str(constants.index2pin[pin_number]) + "LED")

def turnoffLED(pin_number):
    # GPIO.output(index2pin[pin_number], GPIO.LOW)
    print("trun off " + str(constants.index2pin[pin_number]) + "LED")


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
    if len(note) == 1:
        note.pitch = pitch
        note.duration = duration

        # need to multi processing
        # if pitch == pitch_C4:
        #     turnonLED(pinC4)
        #     current_pin_num = pinC4
        
        # time.sleep(duration * standard_time)
        # try:
        #     turnoffLED(current_pin_num)
        # except:
        #     pass

        # turn on LED
        if pitch == PITCH_C4:
            if current_pin_nums[0] == PIN_C4: 
                pass
            else:
                current_pin_nums[0] = PIN_C4
                past_time = time.time()
                turnonLED(PIN_C4)

        # turn off LED
        current_time = time.time()
        if (current_time - past_time >= duration * standard_time):
            try:
                turnoffLED(current_pin_nums[0])
            except:
                pass

        

    # harmonoy
    else:
        # todo after 화음저장방식 정하고 나서.
        pass


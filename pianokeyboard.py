import pygame, time, keyboard
import RPi.GPIO as GPIO


PITCH_C4 = 64
PIN_C4 = 23
PITCH_D4 = 66
PIN_D4 = 24


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(PIN_C4, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(PIN_D4, GPIO.IN, GPIO.PUD_DOWN)




class PianoKeyboard:
    def __init__(self, path):

        ### setup ###
        self.num_keyboard = 13
        pygame.init()
        pygame.mixer.set_num_channels(self.num_keyboard)
        self.channels = [pygame.mixer.Channel(i) for i in range(self.num_keyboard)]
        # keyboard pitch
        self.minValue = 60
        self.maxValue = 72
        # for continuously pressing 
        self.pressing_keyboard_set = set()

        self.sounds = []
        for i in range(self.minValue, self.maxValue + 1):
            self.sounds.append(pygame.mixer.Sound(path + "/Piano" + str(i) + ".ogg"))

    def pressKeyboard(self, value):
        if value < self.minValue or value > self.maxValue:
            return

        ix = value - self.minValue

        if self.channels[ix].get_busy():
            self.channels[ix].stop()
            self.channels[ix].play(self.sounds[ix])
        else:
            self.channels[ix].play(self.sounds[ix])

    def checkKeyboard(self, pin_number, value):
        ix = value - self.minValue
        if GPIO.input(pin_number):
        # if keyboard.is_pressed(pin_number):
            # pressing state is already true
            if ix in self.pressing_keyboard_set:
                pass
            else:
                self.pressing_keyboard_set.add(ix)
                self.pressKeyboard(value)
        else:
            # pressing state is already false
            if not ix in self.pressing_keyboard_set:
                pass
            else:
                self.pressing_keyboard_set.remove(ix)
                self.channels[ix].fadeout(300)

    # normal piano mode only sound not LED
    def piano_mode(self):
        self.checkKeyboard(PIN_C4, PITCH_C4)
        self.checkKeyboard(PIN_D4, PITCH_D4)
        # self.checkKeyboard('d', 68)        



# for test
if __name__ == "__main__":
    PianoKeyboard = PianoKeyboard('Resources/PianoSamples')
    while True:
        PianoKeyboard.piano_mode()





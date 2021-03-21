import RPi.GPIO as GPIO

# setup

LED = 
SWITCH = 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SWITCH, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)


while True:
    if GPIO.input(SWITCH):
        GPIO.output(LED, GPIO.LOW)
    else:
        GPIO.output(LED, GPIO.HIGH)

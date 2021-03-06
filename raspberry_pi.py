import RPi.GPIO as GPIO #RPi.GPIO 라이브러리를 GPIO로 사용
from time import sleep  

servoPin          = 12   # 서보 핀
SERVO_MAX_DUTY    = 12   # 서보의 최대(180도) 위치의 주기
SERVO_MIN_DUTY    = 3    # 서보의 최소(0도) 위치의 주기

GPIO.setmode(GPIO.BOARD)        # GPIO 설정
GPIO.setup(servoPin, GPIO.OUT)  # 서보핀 출력으로 설정

servo = GPIO.PWM(servoPin, 50)  # 서보핀을 PWM 모드 50Hz로 사용하기 (50Hz > 20ms)
servo.start(0)  # 서보 PWM 시작 duty = 0, duty가 0이면 서보는 동작하지 않는다.


# todo : n번쨰 모터
# degree -> duty 변환 후 서보 제어(ChangeDutyCycle)
def setServoPos(degree):
    if degree > 180:
    degree = 180

    # degree -> duty
    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
    print("Degree: {} to {}(Duty)".format(degree, duty))

    servo.ChangeDutyCycle(duty)





setServoPos(0)
sleep(1) # 1초 대기
# 90도에 위치
setServoPos(90)
sleep(1)
# 50도..
setServoPos(50)
sleep(1)

# 120도..
setServoPos(120)
sleep(1)

# 180도에 위치
setServoPos(180)
sleep(1)

# 서보 PWM 정지
servo.stop()
# GPIO 모드 초기화
GPIO.cleanup()
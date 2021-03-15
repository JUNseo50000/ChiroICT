import time, os
from threading import Thread

def funcOne():
    i = 0
    while 1:
        i += 1
        print(i)
        time.sleep(1)

def funcTwo(num):
    text = "abc"
    while 1:
        print(text + str(num))
        time.sleep(3)


# proc1 = Thread(target=funcOne, args=())
# # 변수에서 , 꽤나 중요
# proc2 = Thread(target=funcTwo, args=("3",))
# proc1.start()
# proc2.start()


print(time.time())
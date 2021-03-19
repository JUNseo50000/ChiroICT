# import random, time, keyboard
# import threading

# # # global work1_state
# # work1_state = True
# # print("First " + str(id(work1_state)))
# # lock = threading.Lock()

# class CL:
#     def __init__(self):
#         self.work1_state = True

#     def work1(self):
#         # lock.acquire()
#         # print("after lock " + str(id(work1_state)))

#         # print("first of function " + str(id(work1_state)))

#         i = 0
#         while i <= 2:
#             print(i)
#             time.sleep(1)
#             i += 1
#         # print("after global " + str(id(self.work1_state))) # 1410845104
#         print("First " + str(id(self.work1_state))) # 1410845136
#         self.work1_state = False
#         print("after false " + str(id(self.work1_state))) # 1410845136
#         self.work1_state = True
#         print("after True " + str(id(self.work1_state))) # 
        
#         # lock.release()
#         # print("after release " + str(id(work1_state)))

# def work2():
#     pass
#     # time.sleep(0.5)
#     # print(work1_state)
#     # print("OK")

# CL = CL()
# work1 = threading.Thread(target=CL.work1, args=())
# # work2 = Thread(target=work2, args=())

# while True:
#     if CL.work1_state:
#         work1.start()

#         while True:
#             work2()

#             # if keyboard.is_pressed('k'):
#             #     # print("KKK")
#             #     work1_state = False
#             print(CL.work1_state)
#             if not CL.work1_state:
#                 break

#     print("DONE")
#     time.sleep(5)


# # state = True
# # print(id(state))
# # def do():
# #     global state
# #     print(id(state)) # 1410845104
# #     state = False
# #     print(id(state)) # 1410845136

# # do()
    
    

import random, time, keyboard
import threading

# # global work1_state
# work1_state = True
# print("First " + str(id(work1_state)))
# lock = threading.Lock()

work1_state = True

def work1():
    global work1_state 

    i = 0
    while i <= 2:
        print(i)
        time.sleep(1)
        i += 1
    print("First " + str(id(work1_state))) # 1410845136
    work1_state = False


def work2():
    pass

work1 = threading.Thread(target=work1, args=())

while True:
    if work1_state:
        work1.start()

        while True:
            work2()

            if not work1_state:
                break

    print("DONE")
    time.sleep(5)
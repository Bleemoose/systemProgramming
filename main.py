import threading
import time
import queue


bacc_A, bacc_B = 100_000, 100_000

lock = threading.Lock()
def transfer5():
    global bacc_A, bacc_B,lock
    print("I am transfer 5")

    for i in range(100000):
        lock.acquire()
        bacc_A -= 5
        bacc_B +=5
        lock.release()





def transfer10():
    global bacc_A, bacc_B,lock
    print("I am transfer 10")

    for i in range(50000):
        lock.acquire()
        bacc_B -= 10
        bacc_A += 10
        lock.release()




def transfer20():
    global bacc_A, bacc_B , lock
    print("I am transfer 20")

    for i in range(100000):
        lock.acquire()
        bacc_A -= 20
        bacc_B += 20
        lock.release()



def transfer40():
    global bacc_A, bacc_B , lock
    print("I am transfer 40")
    for i in range(50000):
        lock.acquire()
        bacc_B -= 40
        bacc_A += 40
        lock.release()



def runExperiment():


    t5 = threading.Thread(target=transfer5(),args=())
    t10 = threading.Thread(target=transfer10(), args=())
    t20 = threading.Thread(target=transfer20(), args=())
    t40 = threading.Thread(target=transfer40(), args=())
    t5.start()
    t10.start()
    t20.start()
    t40.start()


def runExpirimentWithFiFo():
    t5 = threading.Thread(target=transfer5(), args=())
    t10 = threading.Thread(target=transfer10(), args=())
    t20 = threading.Thread(target=transfer20(), args=())
    t40 = threading.Thread(target=transfer40(), args=())
    FiFo = queue.Queue()
    FiFo.put(t5)
    FiFo.put(t10)
    FiFo.put(t20)
    FiFo.put(t40)
    for i in range(FiFo.qsize()):
        FiFo.get().start()

for i in range(20):
    runExpirimentWithFiFo()
    print(bacc_A,  bacc_B)
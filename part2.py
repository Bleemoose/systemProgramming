import threading
import queue
import time

global_bacc_A, global_bacc_B = 100_000, 100_000
transferTypes = ["5", "10", "20", "40"]


class Account:
    account_bacc_A, account_bacc_B = 100_000, 100_000

#a lot of params for different types of testing
def myThread(queue, bacc_A, bacc_B, uselock, useGlobals):
    while not queue.empty():

        item = queue.get()
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print("Thread :" + threading.current_thread().name + " starting with transfer type: " + str(item) + " at :"+ current_time)
        if (uselock):
            lock.acquire()
        if item is None:
            break
        if item == "5":
            transfer5(bacc_A, bacc_B, uselock, useGlobals)
        elif item == "10":
            transfer10(bacc_A, bacc_B, uselock, useGlobals)
        elif item == "20":
            transfer20(bacc_A, bacc_B, uselock, useGlobals)
        elif item == "40":
            transfer40(bacc_A, bacc_B, uselock, useGlobals)
        else:
            print("error thread: " + threading.current_thread().name + " stopping:" + str(item))


def transfer5(bacc_A, bacc_B, useLock, useGlobals):
    if (useGlobals):
        global global_bacc_A,global_bacc_B
        for i in range(100000):
            global_bacc_A -= 5
            global_bacc_B += 5
    else:
        for i in range(100000):
            bacc_A -= 5
            bacc_B += 5
    if (useLock):
        lock.release()


def transfer10(bacc_A, bacc_B, useLock, useGlobals):
    if (useGlobals):
        global global_bacc_A, global_bacc_B
        for i in range(50000):
            global_bacc_B -= 10
            global_bacc_A += 10
    else:
        for i in range(50000):
            bacc_B -= 10
            bacc_A += 10
    if (useLock):
        lock.release()


def transfer20(bacc_A, bacc_B, useLock, useGlobals):
    if (useGlobals):
        global global_bacc_A, global_bacc_B
        for i in range(100000):
            global_bacc_A -= 20
            global_bacc_B += 20
    else:
        for i in range(100000):
            bacc_A -= 20
            bacc_B += 20
    if (useLock):
     lock.release()


def transfer40(bacc_A, bacc_B, useLock, useGlobals):
    if (useGlobals):
        global global_bacc_A, global_bacc_B
        for i in range(50000):
            global_bacc_B -= 40
            global_bacc_A += 40
    else:
        for i in range(50000):
            bacc_B -= 40
            bacc_A += 40
    if (useLock):
        lock.release()


lock = threading.Lock()


def runExperimentWithFiFo():
    global global_bacc_A, global_bacc_B
    threads = []
    q = queue.Queue()
    for i in range(len(transferTypes)):
        q.put(transferTypes[i])

    for i in range(len(transferTypes)):
        thread = threading.Thread(target=myThread, args=(q, global_bacc_A, global_bacc_B, True, True),)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(global_bacc_A, global_bacc_B)

def runExperimentWithLiFo():
    threads = []
    q = queue.LifoQueue()
    for i in range(len(transferTypes)):
        q.put(transferTypes[i])

    for i in range(len(transferTypes)):
        thread = threading.Thread(target=myThread, args=(q, global_bacc_A, global_bacc_B, True,True))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(global_bacc_A, global_bacc_B)


def runExperimentWithPriorityQueue():
    threads = []
    q = queue.PriorityQueue()
    for i in range(len(transferTypes)):
        q.put(transferTypes[i])

    for i in range(len(transferTypes)):
        thread = threading.Thread(target=myThread, args=(q, global_bacc_A, global_bacc_B, True,True))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    print(global_bacc_A,global_bacc_B)


def classExp():
    account = Account()
    threads = []
    q = queue.Queue()
    for i in range(len(transferTypes)):
        q.put(transferTypes[i])

    for i in range(len(transferTypes)):
        thread = threading.Thread(target=myThread, args=(q, account.account_bacc_A, account.account_bacc_B, False,False))
        thread.start()
        threads.append(thread)
    print(account.account_bacc_A,account.account_bacc_B)

print("Class Variables Expiriment with no locks")
for i in range(5):

    classExp()
from multiprocessing import Process
from time import sleep


def func1():
    for i in range(0,5):
        print("a")
        i+=1

def func2():
     for i in range(0,5):
        sleep(1)
        print("b")
        i+=1

def func3():
    for i in range(0,5):
        sleep(2)
        print("c")
        i+=1

# 프로세스를 생성합니다
if __name__ == '__main__':  
    p1 = Process(target=func1) #함수 1을 위한 프로세스
    p2 = Process(target=func2) #함수 1을 위한 프로세스
    p3 = Process(target=func3) #함수 1을 위한 프로세스

    # start로 각 프로세스를 시작합니다. func1이 끝나지 않아도 func2가 실행됩니다.
    p1.start()
    p2.start()
    p3.start()

    # join으로 각 프로세스가 종료되길 기다립니다 p1.join()이 끝난 후 p2.join()을 수행합니다
    p1.join()
    p2.join()
    p3.join()
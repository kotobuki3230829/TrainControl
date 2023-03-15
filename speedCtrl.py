# スピード計算コントローラ
#
import threading
import time
import datetime
import sharedMem as Shm

class mon:
    def __init__(self):
        self.fspeed = 0.0
        self.speed=0
        self.__FinishFlag=False
        self.__spddict = { -5:5, -4:4, -3:3, -2:2, -1:1, 0:-1, \
                           5:-10, 4:-8, 3:-6, 2:-4, 1:-2 }
        
    def startTrd(self,shm):
        self.trd=threading.Thread(target=self.calProc,args=[shm])
        self.trd.start()
        
    def waitEndTrd(self):
        self.__FinishFlag=True
        self.trd.join()
        
    def calProc(self,shm):
        print("Start Thread")
        while True:
            if self.__FinishFlag==True:
                break
            time.sleep(0.1)
            #self.speed += self.__spddict[shm[1]]
            self.fspeed += float(self.__spddict[shm[Shm.NOTCH]]/10)
            self.speed = int(self.fspeed)
            if self.speed < 0:
                self.speed = 0
                self.fspeed = 0.0
            elif self.speed>100:
                self.speed=100
                self.fspeed = 100.0
            shm[Shm.SPEED]=self.speed
            #print("message from Thread: speed: " + str(self.speed) + "  Notch:" + str(shm[1]))
            
        print("End Thread")
        
        
if __name__ == '__main__':
     pass

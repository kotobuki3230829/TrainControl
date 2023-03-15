# Thread間通信用共有メモリ
#
from multiprocessing import  Array

SPEED  = 0
NOTCH  = 1
EMGSTP = 2
##
EMGSTP_OFF = 0
EMGSTP_ON  = 1

class mem:
    def __init__(self):
        self.val=Array('i',10)
        for v in self.val:
            v = 0

if __name__ == '__main__':
    x = mem()
    print(x.val[:])

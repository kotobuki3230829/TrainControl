#
# トレインコントローラメイン
#
import time
import datetime

import keyBd
import screenCtrl
import speedCtrl
import sharedMem as Shm

notch = 0

def notchCtrl(key):
   global notch
   if key==keyBd.DOWN:
      notch-=1
      if notch<-5:
         notch=-5
   elif key==keyBd.UP:
      notch+=1
      if notch>5:
         notch=5
   return notch
      

if __name__ == '__main__':
    
     shm = Shm.mem()          # Thread間通信用共有メモリ
     smon=speedCtrl.mon()     # スピード計算コントローラ
     smon.startTrd(shm.val)
     scrn=screenCtrl.Win()    # 計器Window表示
     scrn.startWin(shm.val)
     
     getKey=keyBd.getKey()
     while True:
         # キー入力
         key=getKey.val()
         # 非常ボタンが解除中
         if shm.val[Shm.EMGSTP]==Shm.EMGSTP_OFF:
            shm.val[Shm.NOTCH]= notchCtrl(key)
         # 非常ボタン
         if key==keyBd.BKSPC:
            if shm.val[Shm.EMGSTP]==Shm.EMGSTP_ON:
               shm.val[Shm.EMGSTP]=Shm.EMGSTP_OFF
            else:
               notch=5
               shm.val[Shm.NOTCH]=notch
               shm.val[Shm.EMGSTP]=Shm.EMGSTP_ON
         # ESCキーで終了
         if key==keyBd.ESCAPE:
             smon.waitEndTrd()
             scrn.waitEndWin()
             break
     print("xxxxxxxxxxxxxx")
    
    
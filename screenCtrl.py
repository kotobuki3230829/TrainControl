# 画面表示
#
import threading
import tkinter as tk
import math
import tkinter.font as font
import random
import sharedMem as Shm

# リフレッシュインターバル
REF_INTERVAL = 100
# キャンバスのサイズの設定
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 400
CANVAS_SIZE = CANVAS_WIDTH
# 針の色のリスト
colors = [ "blue", "red", "black" ]
# 針の太さのリスト
widths = [ 3, 3, 2 ]
# 針の長さのリスト
lengths = [ CANVAS_SIZE / 2 * 0.33, CANVAS_SIZE / 2 * 0.28, CANVAS_SIZE / 2 * 0.28 ]
# 針の中心X座標のリスト
centerx =  [ 237,462,462 ]
# 描画した針のオブジェクトを覚えておくリスト
hands = []
ihands = []
iuhands = []

class Win:
    def __init__(self):
        self.__FinishFlag=False
        
    def startWin(self,shm):
        self.trd=threading.Thread(target=self.winProc,args=[shm])
        self.trd.start()
        
    def waitEndWin(self):
        self.__FinishFlag=True
        self.trd.join()

    def drawNeedles( self, speed, press, bpress, firstFlag ,cvs):
        '''針を表現する線を描画する'''

        # 各線の傾きの角度を計算指定リストに追加
        angles = []
        angles.append(speed * 230 / 120 - 205)
        angles.append(press * 270 / 1000 - 225)
        angles.append(bpress * 270 / 1000 - 225)

        # 線の一方の座標をキャンバスの中心とする
        y1 = 200 # 針中心y座標

        # 針を描画
        if firstFlag:
          for angle, length, width, color,x1 in zip(angles, lengths, widths, colors ,centerx):

            # 針の他方の座標を計算
            x2 = x1 + length * math.cos(math.radians(angle))
            y2 = y1 + length * math.sin(math.radians(angle))

            hand = cvs.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width
            )
            # 描画した線のIDを覚えておく
            hands.append(hand)
        else:
            for hand, angle, length,x1 in zip(hands, angles, lengths,centerx):

              # 針の他方の座標を計算
              x2 = x1 + length * math.cos(math.radians(angle))
              y2 = y1 + length * math.sin(math.radians(angle))

              # coordsメソッドにより描画済みの線の座標を変更する
              hand = cvs.coords(
                hand,
                x1, y1, x2, y2
              )

    def drawInds( self, notch, firstFlag ,cvs):
        '''ノッチインジケータを描画する'''
        # ノッチ段数に対するインジケータカラー
        notchCol = [
            ["gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","green","green","green","green","green"],
            ["gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","green","green","green","green","gainsboro"],
            ["gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","green","green","green","gainsboro","gainsboro"],
            ["gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","green","green","gainsboro","gainsboro","gainsboro"],
            ["gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","green","gainsboro","gainsboro","gainsboro","gainsboro"],
            ["gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","cyan","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro"],
            ["gainsboro","gainsboro","gainsboro","gainsboro","orange","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro"],
            ["gainsboro","gainsboro","gainsboro","orange","orange","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro"],
            ["gainsboro","gainsboro","orange","orange","orange","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro"],
            ["gainsboro","orange","orange","orange","orange","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro"],
            ["orange","orange","orange","orange","orange","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro","gainsboro"]
        ]
        # 
        if firstFlag:
          x1,x2,y1,ystp = [60,80,160,12]
          id = cvs.create_rectangle(50, 150, 90, 300, fill='gray',state=tk.DISABLED)
          for i in range(11):
            ihand = cvs.create_rectangle(x1, y1+i*ystp, x2, y1+i*ystp+10, fill='gainsboro',outline='gray')
            # 描画したインジケータのIDを覚えておく
            ihands.append(ihand)
        else:
            i=0
            for hand in ihands:
              cvs.itemconfig(hand,fill=notchCol[notch+5][i])
              i+=1


    def drawUpInds( self, cvs, mkNo=0, OnOff=False):
        '''上部インジケータを描画する'''
        # ノッチ段数に対するインジケータカラー
        indCol = [
            ["dark green","green yellow","予備"],
            ["dark green","green yellow","予備"],
            ["dark green","green yellow","予備"],
            ["dark green","green yellow","予備"],
            ["IndianRed4","red","非常"]
        ]
        # 
        if mkNo==0:
          i=0
          for val in indCol:
            iuhand = cvs.create_rectangle(140+85*i, 50, 220+85*i, 75, fill=indCol[i][0], width=2,outline='gray')
            cvs.create_text(180+85*i, 60,text=indCol[i][2],fill="gray10")
            # 描画したインジケータのIDを覚えておく
            iuhands.append(iuhand)
            i+=1
        else:
            colInd=lambda flag : 0 if flag==False else 1
            cvs.itemconfig(iuhands[mkNo-1],fill=indCol[mkNo-1][colInd(OnOff)])


    def winProc(self,shm):
        # define a window
        root=tk.Tk()
        cvs=tk.Canvas(width=CANVAS_WIDTH,height=CANVAS_HEIGHT)
        cvs.pack()
        bg=tk.PhotoImage(file='meter.png')
        cvs.create_image(350,200,image=bg)

        # Top label
        bgfont = font.Font(root, family="Menlo", size=16, weight="bold")
        label_top = tk.Label(root, text='Train Controller',font=bgfont,foreground='blue',relief='ridge')
        label_top.place(x=50,y=0)
        
        # メッセージ
        #label_mess = tk.Label(root, text="*")
        #label_mess.place(x = 100,y=370)
        
        def refresh():               
            
            if shm[Shm.NOTCH] > 0:
                press=shm[Shm.NOTCH]*53+random.randint(0,3)
            else:
                press=0
            
            self.drawNeedles(shm[Shm.SPEED], press, 350+random.randint(0,5) ,False ,cvs)
            self.drawInds( shm[Shm.NOTCH], False ,cvs)
            # 非常ボタン
            if shm[Shm.EMGSTP]==Shm.EMGSTP_ON:
                self.drawUpInds( cvs, mkNo=5,OnOff=True)
            else:
                self.drawUpInds( cvs, mkNo=5,OnOff=False)
            
            if self.__FinishFlag==False:
                label_top.after(REF_INTERVAL,refresh)
            else:
                root.destroy()
            
        label_top.after(REF_INTERVAL,refresh)
        self.drawNeedles(0, 0, 0,True,cvs)
        self.drawInds( shm[Shm.NOTCH], True ,cvs)
        self.drawUpInds( cvs, mkNo=0)
        
        root.mainloop()
        
if __name__ == '__main__':
     pass

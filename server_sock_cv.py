import socket
import numpy as np
import cv2
from PIL import Image,ImageGrab,ImageTk
from msvcrt import getch
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ソケットオブジェクト作成
s.bind(("127.0.0.1", 10002))    # サーバー側PCのipと使用するポート
print("接続待機中")  
s.listen(1)                     # 接続要求を待機
soc, addr = s.accept()          # 要求が来るまでブロック
print(str(addr)+"と接続完了")  
#cam = cv2.VideoCapture(0)#カメラオブジェクト作成
cam = cv2.VideoCapture(1)#カメラオブジェクト作成
#raspberry pi
#cam = picamera.PiCamera() 
#cam.framerate = 33
#raspberry pi

while (True):
    #flag,img = cam.read()       #カメラから画像データを受け取る
    #raspberry pi
    img = getImage(cap)
    #raspberry pi
    #img = ImageGrab.grab()
    img = img.tostring()        #numpy行列からバイトデータに変換
    #img = img.tobytes()        #numpy行列からバイトデータに変換
    soc.send(img)              # ソケットにデータを送信
    #time.sleep(0.5)            #フリーズするなら#を外す。
    k = cv2.waitKey(1)         #↖ 
    if k== 27 :                #←　ENTERキーで終了
        break                  #↙

#cam.releace()                  #カメラオブジェクト破棄
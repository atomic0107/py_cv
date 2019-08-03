import sys
import socket
import numpy as np
import cv2
import requests

DATASIZE = 921633
#url = 'http://ipcheck.ieserver.net/'
url='http://inet-ip.info/ip'
res = requests.get(url)
print(res.text)

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ソケットオブジェクト作成
soc.connect(("127.0.0.1", 10002))#サーバー側のipと使用するポート(ポートはサーバーと同じにする。)
print("接続完了")

while(1):
    data = soc.recv(DATASIZE)#引数は下記注意点参照
    data_size = sys.getsizeof(data)
    if(data_size == DATASIZE):
        data = np.fromstring(data,dtype=np.uint8)#バイトデータ→ndarray変換
        data = np.reshape(data,(480,640,3))#形状復元(これがないと一次元行列になってしまう。)　reshapeの第二引数の(480,640,3)は引数は送られてくる画像の形状
        cv2.imshow("",data)
    else:
        print(data_size)

    k = cv2.waitKey(1)
    if k== 27 :
        break

cv2.destroyAllWindows() # 作成したウィンドウを破棄   
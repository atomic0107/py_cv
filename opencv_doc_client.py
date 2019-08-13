import io
import socket
import struct
from PIL import Image
import numpy as np
import cv2

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image)
    #if new_image.ndim == 2:  # モノクロ
    #    pass
    if new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
    return new_image

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.3.6', 10002))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)

        image = Image.open(image_stream)
        #data = np.fromstring(image_stream,dtype=np.uint8)#バイトデータ→ndarray変換
        #data = np.reshape(image_stream,(480,640,3))#形状復元(これがないと一次元行列になってしまう。)　reshapeの第二引数の(480,640,3)は引数は送られてくる画像の形状
        
        #cv2.imshow("",data)
        #cv_image = pil2cv(image)
        cv_image = np.asarray(image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        cv2.imshow("",cv_image)
        cv2.waitKey(1)
        k = cv2.waitKey(1)         #↖ 
        if k== 27 :                #←　ENTERキーで終了
            break                  #↙

        print('Image is %dx%d' % image.size)
        image.verify()
        print('Image is verified')
        

finally:
    cv2.destroyAllWindows()
    connection.close()
    server_socket.close()
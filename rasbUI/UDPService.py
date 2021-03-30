import cv2
import socket
import time
import struct
import threading

class UDPService():
    def __init__(self,host='localhost',port=8080):#UDP服务构造函数，在中控初始化时调用，以便先设置好套接字并开始连接
        self.host=host
        self.port=port
        self.server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#构造套接字，设置为UDP模式
        # self.server.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #设置为广播模式
        # self.server.setblocking(False)#设置为非阻塞模式
        self.server.connect((self.host,self.port))#连接到指定客户端的IP地址和端口

    def sendFrame(self,frame):#发送帧函数，请在中控循环获取每一帧的摄像头数据并解析和显示画面的函数中循环调用，传入cap.read()函数获取的frame
        def runSend():
            try:
                result,imgData=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,50])#编码为JPEG格式的二进制字符串
                self.server.sendall(imgData)#发送二进制串
            except Exception as e:
                self.server.sendall(struct.pack('b',1))
                print(e)

        t=threading.Thread(target=runSend,daemon=True)
        t.start()

    def __del__(self):
        self.server.close()#关闭套接字
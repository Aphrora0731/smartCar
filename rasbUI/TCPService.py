import cv2
import socket
import time
import struct
import multiprocessing

class TCPService():
    HOST='localhost'#服务器端IP地址
    PORT=8080#端口号

    def __init__(self):#TCP服务构造函数，在中控初始化时调用，以便先设置好套接字并开始监听是否有手机客户端接入
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#构造套接字，设置为面向网络的TCP模式
        self.server.setblocking(False)#设置为非阻塞模式，无需等待上一次的数据发送完毕
        self.server.bind((HOST,PORT))#绑定IP地址和端口号
        self.server.listen(1)#开始监听客户端的接入，因为是TCP协议，因此设置最大接入数量为1

        self.conn=None
        self.addr=None

        def link_loop():
            while True:
                if self.conn is None:
                    self.conn,self.addr = self.server.accept()
                elif not self.conn.recv(1024):
                    self.conn.close()
                    self.conn=None

        t=multiprocessing.Process(target=link_loop,daemon=True)

    def isLinked(self):#判断是否有客户端接入函数，用于发送帧前的判断，若无接入的客户端，请不要调用sendFrame()函数发送帧
        return self.conn is not None

    def sendFrame(self,frame):#发送帧函数，请在中控循环获取每一帧的摄像头数据并解析和显示画面的函数中循环调用，传入cap.read()函数获取的frame
        if not self.isLinked:
            print('客户端未连接！')
            return
        try:
            result,imgData=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,90])#编码为JPEG格式的二进制字符串
            self.conn.sendall(imgData)#发送全部二进制串
        except Exception as e:
            self.conn.sendall(struct.pack('b',1))
            print(e)

    def __del__(self):
        if self.isLinked():
            self.conn.close()#析构时关闭网络连接
        self.server.close()#关闭套接字

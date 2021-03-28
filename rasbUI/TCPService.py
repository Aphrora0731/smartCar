import cv2
import socket
import time
import struct
import threading

class TCPService():
    HOST='localhost'#服务器端IP地址
    PORT=8080#端口号

    def __init__(self):#TCP服务构造函数，在中控初始化时调用，以便先设置好套接字并开始监听是否有手机客户端接入
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#构造套接字，设置为面向网络的TCP模式
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

        t=threading.Thread(target=link_loop,daemon=True)
        t.start()

    def isLinked(self):#判断是否有客户端接入函数，用于发送帧前的判断，若无接入的客户端，请不要调用sendFrame()函数发送帧
        return self.conn is not None

    def sendMsg(self,message):#发送帧函数，请在中控循环获取每一帧的摄像头数据并解析和显示画面的函数中循环调用，传入cap.read()函数获取的frame
        if not self.isLinked:
            print('客户端未连接！')
            return
        def runSend():
            try:
                msgData=message.encode('utf-8')#将字符串转换为二进制串
                self.conn.sendall(msgData)#发送全部二进制串
            except Exception as e:
                self.conn.sendall(struct.pack('b',1))
                print(e)
        
        t=threading.Thread(target=runSend,daemon=True)
        t.start()

    def __del__(self):
        if self.isLinked():
            self.conn.close()#析构时关闭网络连接
        self.server.close()#关闭套接字

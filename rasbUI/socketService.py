import cv2
import socket
import time
import struct
import threading

class SocketService():
    def __init__(self):
        self.udpServer=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#构造套接字，设置为UDP模式
        self.udpServer.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1) #设置为广播模式
        self.udpServer.bind(('',8080))
        self.udpServer.settimeout(10)
        self.host=''
        self.tcpServer=None
        self.tcpClient=None
        self.tcpClientAddr=None
        def listen():
            while True:
                try:
                    msgData,addr=self.udpServer.recvfrom(1024)
                    message=msgData.decode('utf-8')
                    print(message,message == 'udp server')
                    if message == 'udp server':
                        self.host=addr[0]
                        print(self.host)
                        self.udpServer.close()
                        self.udpServer=None
                        # self.startTCP()
                        self.startUDP()
                        break
                    self.host=''
                except Exception as e:
                    print(e)
                    continue

        # listen()
        t=threading.Thread(target=listen,daemon=True)
        t.start()

    def startTCP(self):
        self.tcpServer=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#构造套接字，设置为面向网络的TCP模式
        self.tcpServer.bind((self.host,8000))#绑定IP地址和端口号
        self.tcpServer.listen(1)#开始监听客户端的接入，因为是TCP协议，因此设置最大接入数量为1

        def link_loop():
            while True:
                if self.tcpClient is None:
                    self.tcpClient,self.tcpClientAddr = self.tcpServer.accept()
                elif not self.tcpClient.recv(1024):
                    self.tcpClient.close()
                    self.tcpClient=None

        t=threading.Thread(target=link_loop,daemon=True)
        t.start()

    def startUDP(self):
        self.udpServer=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#构造套接字，设置为UDP模式
        self.udpServer.connect((self.host,8080))#连接到指定客户端的IP地址和端口

    def sendFrameByUDP(self,frame):#发送帧函数，请在中控循环获取每一帧的摄像头数据并解析和显示画面的函数中循环调用，传入cap.read()函数获取的frame
        if self.host=='':
            print('客户端未连接！')
            return
        def runSend():
            try:
                result,imgData=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,50])#编码为JPEG格式的二进制字符串
                self.udpServer.sendall(imgData)#发送二进制串
            except Exception as e:
                self.udpServer.sendall(struct.pack('b',1))
                print(e)

        t=threading.Thread(target=runSend,daemon=True)
        t.start()

    def sendCmdByTCP(self,command):#发送帧函数，请在中控循环获取每一帧的摄像头数据并解析和显示画面的函数中循环调用，传入cap.read()函数获取的frame
        if self.host=='':
            print('客户端未连接！')
            return
        if not self.isTCPLinked:
            print('TCP未连接！')
            return
        def runSend():
            try:
                cmdData=command.encode('utf-8')#将字符串转换为二进制串
                self.tcpClient.sendall(cmdData)#发送全部二进制串
            except Exception as e:
                self.tcpClient.sendall(struct.pack('b',1))
                print(e)
        
        t=threading.Thread(target=runSend,daemon=True)
        t.start()

    def __del__(self):
        if self.tcpClient is not None:
            self.tcpClient.close()#析构时关闭网络连接
        if self.tcpServer is not None:
            self.tcpServer.close()#关闭套接字
        if self.udpServer is not None:
            self.udpServer.close()#关闭套接字 


if __name__ =="__main__":
    socketService=SocketService()


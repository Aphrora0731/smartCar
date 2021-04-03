from win32 import win32file
from win32 import win32pipe
import cv2
import numpy as np

PIPE_NAME = r'\\.\Pipe\mypipe'
PIPE_BUFFER_SIZE = 65535

while True:
    named_pipe = win32pipe.CreateNamedPipe(PIPE_NAME,
                                           win32pipe.PIPE_ACCESS_DUPLEX,
                                           win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT | win32pipe.PIPE_READMODE_MESSAGE,
                                           win32pipe.PIPE_UNLIMITED_INSTANCES,
                                           PIPE_BUFFER_SIZE,
                                           PIPE_BUFFER_SIZE, 500, None)
    try:
        while True:
            try:
                win32pipe.ConnectNamedPipe(named_pipe, None)
                data = win32file.ReadFile(named_pipe, PIPE_BUFFER_SIZE, None)
                if data is None or len(data) < 2:
                    continue
                image = np.asarray(bytearray(data), dtype="uint8") 
                img=cv2.imdecode(image,cv2.IMREAD_COLOR)
                cv2.imshow('adasd',img)
                cv2.waitKey(0)

                print('receive msg:', data)
            except BaseException as e:
                print("exception:", e)
                break
    finally:
        try:
            win32pipe.DisconnectNamedPipe(named_pipe)
        except:
            pass
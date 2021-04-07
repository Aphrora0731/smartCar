from PyQt5.QtGui import QColor

from GUI_console import Ui_MainWindow
# from new import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, QDateTime, QRectF, Qt
from PyQt5 import QtGui

from PyQt5.Qt import QPropertyAnimation, QPoint
import PyQt5.QtWidgets
import cv2
import time
from threading import Thread
import mylib
from is_sleep import is_sleep
import detect
from socketService import SocketService


class Console(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Console, self).__init__()
        self.is_front = True   # 开启时默认开启前方摄像头
        self.is_blind_area = False  # 判断主窗口是否放映盲区检测结果
        self.is_drowsiness = False  # 睡意检测判断标志
        self.is_back = False    # 后方摄像头
        self.setupUi(self)
        self.timer = QTimer(self)  # 更新主窗口画面
        self.warning_timer = QTimer(self)  # 这好像是用来播放声音的，避免连续播放音频文件
        # self.warning_timer.start(100)
        self.warning_timer.start(100)
        self.timer.start(30)
        self.timer_2 = QTimer(self)

        
        # self.camera_front = cv2.VideoCapture(1)
        # self.camera_back = cv2.VideoCapture(2)
        # self.camera_blind = self.camera_back
        # self.camera_blind = cv2.VideoCapture(2)
        # self.camera_drowsiness = cv2.VideoCapture(0)
        
        self.test_camera = cv2.VideoCapture(0)
        
        self.init_slot()
        self.socketS=SocketService()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.effect_shadow = QGraphicsDropShadowEffect(self)
        self.btn1_shadow = QGraphicsDropShadowEffect(self)
        self.btn2_shadow = QGraphicsDropShadowEffect(self)

        self.effect_shadow.setOffset(0, 0)  # 偏移
        self.effect_shadow.setBlurRadius(100)  # 阴影半径
        self.effect_shadow.setColor(QColor(0x0099FF))  # 阴影颜色
        self.label.setGraphicsEffect(self.effect_shadow)  # 将设置套用到widget窗口中

        self.font = QtGui.QFont()
        self.font.setFamily('微软雅黑')
        self.font.setBold(True)
        self.font.setPointSize(16)
        self.font.setWeight(50)
        op = QGraphicsOpacityEffect()
        # 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op.setOpacity(0.8)
        self.pushButton_2.setFont(self.font)
        self.pushButton_3.setFont(self.font)
        self.pushButton_4.setFont(self.font)
        self.pushButton_5.setFont(self.font)

    def init_slot(self):
        # Default
        self.timer.timeout.connect(self.play_front_camera)  # 每当timer计时结束就执行槽函数
        self.timer.timeout.connect(self.play_back_camera)
        self.timer.timeout.connect(self.play_radar)
        self.timer.timeout.connect(self.play_blind)
        # 要增加新的业务代码：
        # self.timer.timeout.connect(self.your_own_function)
        self.timer.timeout.connect(self.play_detect_drowsiness)   # 睡意检测
        self.warning_timer.timeout.connect(self.update_warning_time)

    # 调用功能函数，生成画面，并放映在画布上
    # 调用前方摄像头
    def play_front_camera(self):
        if not self.is_front:
            return
        img_width = 1200
        img_height = 900
        # flag, frame = self.camera_front.read()        
        flag, frame = self.test_camera.read()

        img, is_danger = detect.brake_light(frame)  # 红灯检测
        if is_danger:
            print("danger")
        img = detect.video_object_no_line(frame)
        self.socketS.sendFrameByUDP(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        # 请不要动下面这两句神秘的代码
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))

    def play_back_camera(self):
        if not self.is_back:
            return
        img_width = 1200
        img_height = 900
        flag, frame = self.camera_back.read()
        # flag, frame = self.test_camera.read()
        img = detect.video_object(frame)
        self.socketS.sendFrameByUDP(img)
        # cv2.imshow("image",img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))

    # 播放盲区画面
    def play_blind(self):
        if not self.is_blind_area:
            return
        img_width = 1200
        img_height = 900
        # flag, frame = self.camera_blind.read()
        flag, frame = self.test_camera.read()
        img = detect.blind_object(frame)
        self.socketS.sendFrameByUDP(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))

    def play_detect_drowsiness(self):
        if not self.is_drowsiness:
            return
        img_width = 1200
        img_height = 900
        
        flag, frame = self.camera_drowsiness.read()
        # flag, frame = self.test_camera.read()

        img = is_sleep(frame)
        self.socketS.sendFrameByUDP(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))


    def play_radar(self):
        img_width = 900
        img_height = 700
        #img = detect.get_radar()
        # img = cv2.resize(img, (img_width, img_height))
        img,msg = self.socketS.getRadarFrameByUDP()
        try:
            img_h,img_w,ch = img.shape
            background = cv2.imread("../Rplidar/radar.jpg")
            background = cv2.resize(background,(img_h,img_w))
            img = cv2.addWeighted(img,1,background,1,0)
            img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
            self.label_2.setPixmap(QtGui.QPixmap.fromImage(img_to_show))
        except:
            pass

    # slider的槽函数，用来改变距离敏感程度
    def slider_moved(self, value):
        value = value / 20
        detect.change_value(value)

    def update_warning_time(self):
        detect.update_warning_time()

    def front_camera(self):
        self.is_front = True
        self.is_blind_area = False
        self.is_back = False
        self.is_drowsiness = False

    def back_camera(self):
        self.is_back = True
        self.is_front = False
        self.is_blind_area = False
        self.is_drowsiness = False

    def blind_camera(self):
        self.is_blind_area = True
        self.is_front = False
        self.is_back = False
        self.is_drowsiness = False

    def detect_is_sleep(self):
        self.is_front = False
        self.is_blind_area = False
        self.is_front = False
        self.is_drowsiness = True

    def exit_button(self):
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Console()
    win.showFullScreen()
    sys.exit(app.exec_())

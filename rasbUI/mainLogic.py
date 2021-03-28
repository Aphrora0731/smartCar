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
import detect
import time
from threading import Thread
import mylib


class Console(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Console, self).__init__()
        self.is_blind_area = False
        self.setupUi(self)
        self.timer = QTimer(self)
        self.warning_timer = QTimer(self)
        self.warning_timer.start(100)
        self.timer.start(30)
        self.timer_2 = QTimer(self)
        self.camera = cv2.VideoCapture(0)
        self.init_slot()
        self.is_front = True
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

    def init_slot(self):
        # Default
        self.timer.timeout.connect(self.play_front_camera)
        self.timer.timeout.connect(self.play_back_camera)
        self.timer.timeout.connect(self.play_radar)
        self.timer.timeout.connect(self.play_blind)
        self.warning_timer.timeout.connect(self.update_warning_time)

    def play_front_camera(self):
        if not self.is_front:
            return
        img_width = 1200
        img_height = 900
        flag, frame = self.camera.read()
        img = detect.video_object(frame)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))

    def play_back_camera(self):
        if self.is_front:
            return
        img_width = 900
        img_height = 700
        flag, frame = self.camera.read()
        print("back")
        img, is_danger = detect.brake_light(frame)
        if is_danger:
            print("danger")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))

    def play_blind(self):
        if not self.is_blind_area:
            return
        img_width = 1200
        img_height = 900
        flag, frame = self.camera.read()
        img = detect.blind_object(frame)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(img_to_show))


    def play_radar(self):
        img_width = 900
        img_height = 700
        img = detect.get_radar()
        # img = cv2.resize(img, (img_width, img_height))
        img_to_show = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(img_to_show))

    def slider_moved(self, value):
        value = value / 20
        detect.change_value(value)

    def update_warning_time(self):
        detect.update_warning_time()

    def front_camera(self):
        self.is_front = True
        self.is_blind_area = False

    def back_camera(self):
        self.is_front = False
        self.is_blind_area = False

    def blind_camera(self):
        self.is_blind_area = True
        self.is_front = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Console()
    win.showFullScreen()
    sys.exit(app.exec_())

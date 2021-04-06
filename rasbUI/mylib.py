import cv2
from playsound import playsound
import winsound
import ctypes
import time
import numpy as np


# 给物体加框
def track_object(frame, startX, startY, endX, endY, warning_line):
    if endY >= warning_line:
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 1)
    else:
        cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 1)


# 画倒车指引线
def draw_guideline(frame, window_height, alterYRed):
    # (40,40) is the recomended value
    alterYRed = int(5 + alterYRed)
    alterXRed = int(alterYRed * 3 / 4)
    alterYYellow = int(1.2 * alterXRed)
    alterXYellow = int(alterYYellow * 3 / 4)

    # 左侧标示线 横向间隔30 纵向间隔40 中间空5 （纵向）

    cv2.line(frame, (50, window_height), (50 + alterXRed, window_height - alterYRed), (0, 0, 255), 3)  # 红线
    cv2.line(frame, (50 + alterXRed + 6, window_height - alterYRed - 8),
             (50 + alterXYellow + alterXRed + 6, window_height - alterYYellow - alterYRed - 8), (0, 255, 255), 3)  # 黄线
    cv2.line(frame, (50 + alterXRed + alterXYellow + 12, window_height - alterYYellow - alterYRed - 16),
             (150, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 左侧标示线 （横向）
    cv2.line(frame, (50 + alterXRed, window_height - alterYRed), (50 + alterXRed + 20, window_height - alterYRed),
             (0, 0, 255), 3)  # 红线
    cv2.line(frame, (50 + alterXRed + alterXYellow + 6, window_height - alterYRed - alterYYellow - 8),
             (50 + alterXRed + alterXYellow + 20 + 6, window_height - alterYRed - alterYYellow - 8), (0, 255, 255),
             3)  # 黄线
    cv2.line(frame, (150, window_height - 130), (170, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 右侧标示线 （纵向）
    cv2.line(frame, (350, window_height), (350 - alterXRed, window_height - alterYRed), (0, 0, 255), 3)  # 红线
    cv2.line(frame, (350 - alterXRed - 6, window_height - alterYRed - 8),
             (350 - alterXRed - alterXYellow - 6, window_height - alterYRed - alterYYellow - 8), (0, 255, 255), 3)  # 黄线
    cv2.line(frame, (350 - alterXRed - alterXYellow - 12, window_height - alterYRed - alterYYellow - 16),
             (250, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 右侧标示线 (横向)
    cv2.line(frame, (350 - alterXRed, window_height - alterYRed), (350 - alterXRed - 20, window_height - alterYRed),
             (0, 0, 255), 3)  # 红线
    cv2.line(frame, (350 - alterXRed - alterXYellow - 6, window_height - alterYRed - alterYYellow - 8),
             (350 - alterXRed - alterXYellow - 6 - 20, window_height - alterYRed - alterYYellow - 8), (0, 255, 255),
             3)  # 黄线
    cv2.line(frame, (250, window_height - 130), (230, window_height - 130), (0, 255, 0), 3)  # 绿线
    # cv2.imshow("inside", frame)
    return frame


def sound_alarm():
    print("play sound")
    # play an alarm sound
    playsound('./alarm.wav')


def alert_soundtest(endY):
    duration = 500

    freq = endY * 4
    winsound.Beep(freq, duration)


def get_distance():
    print("get distance")


def alert_sound():
    playsound('./danger.wav')


def draw_line(frame, window_height, alterYRed):
    # (40,40) is the recomended value
    alterYRed = int(5 + alterYRed)
    alterXRed = int(alterYRed * 3 / 4)
    alterYYellow = int(1.2 * alterXRed)
    alterXYellow = int(alterYYellow * 3 / 4)

    # 左侧标示线 （横向）
    cv2.line(frame, (0, window_height - alterYRed), (1000, window_height - alterYRed),
             (0, 0, 255), 3)  # 红线
    cv2.line(frame, (0, window_height - alterYRed - alterYYellow - 8),
             (1000, window_height - alterYRed - alterYYellow - 8), (0, 255, 255),
             3)  # 黄线
    cv2.line(frame, (0, window_height - 130), (1000, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 右侧标示线 (横向)
    cv2.line(frame, (350 - alterXRed, window_height - alterYRed), (350 - alterXRed - 20, window_height - alterYRed),
             (0, 0, 255), 3)  # 红线
    cv2.line(frame, (350 - alterXRed - alterXYellow - 6, window_height - alterYRed - alterYYellow - 8),
             (350 - alterXRed - alterXYellow - 6 - 20, window_height - alterYRed - alterYYellow - 8), (0, 255, 255),
             3)  # 黄线
    cv2.line(frame, (250, window_height - 130), (230, window_height - 130), (0, 255, 0), 3)  # 绿线


# 绘制侧边摄像头识别敏感区域
def draw_box(frame, window_height, alterYRed):
    # (40,40) is the recomended value
    alterYRed = int(5 + alterYRed)
    alterXRed = int(alterYRed * 3 / 4)
    alterYYellow = int(1.2 * alterXRed)
    alterXYellow = int(alterYYellow * 3 / 4)
    mask = np.zeros((frame.shape), dtype=np.uint8)
    # 左侧标示线 （横向）
    cv2.rectangle(mask, (0, window_height), (1000, window_height - alterYRed - alterYYellow - 8),
                  (0, 0, 255), -1)  # 红线
    cv2.rectangle(mask, (0, window_height - alterYRed - alterYYellow - 8),
                  (1000, window_height - 130), (0, 255, 255),
                  -1)  # 黄线
    # cv2.rectangle(mask, (0, window_height - 130), (1000, window_height - 130), (0, 255, 0), 3)  # 绿线
    # alpha 为第一张图片的透明度
    alpha = 1
    # beta 为第二张图片的透明度
    beta = 0.5
    gamma = 0
    # cv2.addWeighted 将原始图片与 mask 融合
    frame = cv2.addWeighted(frame, alpha, mask, beta, gamma)
    return frame

# def radar_fun()

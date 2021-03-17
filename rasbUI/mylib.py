import cv2
from playsound import playsound


def track_object(frame, startX, startY, endX, endY, warning_line):
    if endY >= warning_line:
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 1)
    else:
        cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 0), 1)


def draw_guideline(frame, window_height):
    # 左侧标示线 横向间隔30 纵向间隔40 中间空5 （纵向）
    cv2.line(frame, (50, window_height), (80, window_height - 40), (0, 0, 255), 3)  # 红线
    cv2.line(frame, (85, window_height - 45), (115, window_height - 85), (0, 255, 255), 3)  # 黄线
    cv2.line(frame, (120, window_height - 90), (150, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 左侧标示线 （横向）
    cv2.line(frame, (80, window_height - 40), (100, window_height - 40), (0, 0, 255), 3)  # 红线
    cv2.line(frame, (115, window_height - 85), (135, window_height - 85), (0, 255, 255), 3)  # 黄线
    cv2.line(frame, (150, window_height - 130), (170, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 右侧标示线 （横向）
    cv2.line(frame, (350, window_height), (320, window_height - 40), (0, 0, 255), 3)  # 红线
    cv2.line(frame, (315, window_height - 45), (285, window_height - 85), (0, 255, 255), 3)  # 黄线
    cv2.line(frame, (280, window_height - 90), (250, window_height - 130), (0, 255, 0), 3)  # 绿线

    # 右侧标示线 (纵向)
    cv2.line(frame, (320, window_height - 40), (300, window_height - 40), (0, 0, 255), 3)  # 红线
    cv2.line(frame, (285, window_height - 85), (265, window_height - 85), (0, 255, 255), 3)  # 黄线
    cv2.line(frame, (250, window_height - 130), (230, window_height - 130), (0, 255, 0), 3)  # 绿线


def sound_alarm():
    print("play sound")
    # play an alarm sound
    playsound('./alarm.wav')

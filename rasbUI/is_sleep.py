# USAGE
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python detect_drowsiness.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav

# import the necessary packages
from scipy.spatial import distance as dist  # 在眼睛横纵比计算中的到眼睛之间的欧几里得距离
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2


def sound_alarm(path):
    # play an alarm sound
    playsound.playsound(path)


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio 长宽比
    return ear


# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
# 定义两个常数，一个用于指示眼睛的长宽比
#  闪烁，然后第二个常量表示连续的数量
#   眼球必须低于阈值才能引起眼睛不适
# 警报
# EYE_AR_THRESH = 0.3 最初的参数
EYE_AR_THRESH = 0.3  # 眼睛的宽和长之比
EYE_AR_CONSEC_FRAMES = 48  # 眼睛连续闭上的帧数，如果超过48帧就发出警报

# initialize the frame counter as well as a boolean used to
# indicate if the alarm is going off
COUNTER = 0
ALARM_ON = False

# initialize dlib's face detector (HOG-based) and then create 初始化dlib自带的人脸检测器，然后创建面部界标预测器
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()  # 构建人脸框位置检测器
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")  # 绘制人脸关键点检测器

# grab the indexes of the facial landmarks for the left and
# right eye, respectively  左眼和右眼的面部标志的索引
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
time.sleep(1.0)  # 使相机传感器预热


# loop over frames from the video stream  循环播放视频流的帧
def is_sleep(frame):
    # grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    global COUNTER
    global ALARM_ON
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将图片转换成灰度图像
    # detect faces in the grayscale frame
    rects = detector(gray, 0)  # 应用面部检测器来定位图中脸的位置

    # loop over the face detections
    for rect in rects:
        # determine the facial landmarks for the face region, then
        # convert the facial landmark (x, y)-coordinates to a NumPy
        # array
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)  # 确定面部区域的面部标志，将面部界面的坐标转换成numpy

        # extract the left and right eye coordinates, then use the
        # coordinates to compute the eye aspect ratio for both eyes
        leftEye = shape[lStart:lEnd]  # 计算左眼和右眼的坐标，计算横纵比
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)

        # average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # compute the convex hull for the left and right eye, then
        # visualize each of the eyes   计算左眼和右眼的凸包，然后可视化每一只眼睛
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)  # 第一个参数是图像 2、轮廓 3、对轮廓的索引 -1表示全部绘制
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)  # 4、颜色  5、 厚度
        # check to see if the eye aspect ratio is below the blink  开始检测
        # threshold, and if so, increment the blink frame counter
        if ear < EYE_AR_THRESH:  # 如果宽长比小于设定的值，就开始计算帧数
            COUNTER += 1

            # if the eyes were closed for a sufficient number of
            # then sound the alarm
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                # if the alarm is not on, turn it on
                if not ALARM_ON:
                    ALARM_ON = True
                    # check to see if an alarm file was supplied,
                    # and if so, start a thread to have the alarm
                    # sound played in the background
                    if True:
                        t = Thread(target=sound_alarm,
                                   args=("./alarm.wav",))
                        t.deamon = True  # 守护进程
                        t.start()

                # draw an alarm on the frame
                cv2.putText(frame, "WARNING!", (10, 30),  # 1、图片  2、 显示的字符串 3、第一个字符左下角的坐标 4、字体结构初始化
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)  # 5、字体的颜色  6、 字体宽度

        # otherwise, the eye aspect ratio is not below the blink
        # threshold, so reset the counter and alarm
        else:
            COUNTER = 0
            ALARM_ON = False

        # draw the computed eye aspect ratio on the frame to help
        # with debugging and setting the correct eye aspect ratio
        # thresholds and frame counters
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),  # 在屏幕上显示当前眼睛的横纵比
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # show the frame
    return frame
# do a bit of cleanup

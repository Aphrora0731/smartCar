# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
# python3 real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# To detect object,just enter following command in terminal
# python my_object_detect.py

from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
from skimage import measure
from imutils import contours
import mylib
import dlib
from imutils import face_utils
from threading import Thread
import winsound
import socketService

# set constant
size = 400
window_width = 1080
window_height = 960

usr_input = 40
end = 0


def change_value(input):
    global usr_input
    usr_input = input


CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("./MobileNetSSD_deploy.prototxt.txt", "./MobileNetSSD_deploy.caffemodel")

print("[INFO] starting video stream...")
vs = None
time.sleep(2.0)
start = 0
ALARM_ON = False


# 将RGB转化成HSV，只保留红色的像素点
def find_red(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 127, 128])
    upper_red = np.array([10, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    return mask_red


def draw_line(image):
    mylib.draw_guideline(image, window_height, usr_input)    # 画距离线
    return image


# 获取读到的视频帧
# 好像不用了
def get_video():
    frame = vs.read()
    return frame

# 从参数frame中识别物体并返回加了框的图像
# loop over the frames from the video stream
def video_object(frame,socket):
    global usr_input, end, ALARM_ON
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = imutils.resize(frame, width=400)
    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    window_height = h
    window_width = w
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            if end - start > 1:
                # 用object下沿距离画框底部的垂直距离判定车与物体的水平距离
                if endY >= window_height - 5 - usr_input:
                    if not ALARM_ON:
                        ALARM_ON = True
                        t = Thread(target=mylib.alert_soundtest, args=[endY])
                        t.start()
                        socket.sendFrameByTCP(frame)
                    end = start
                    update_warning_time()
            ALARM_ON = False
            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            mylib.track_object(frame, startX, startY, endX, endY, window_height - 5 - usr_input)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 1)

    mylib.draw_guideline(frame, window_height, usr_input)
    frame = cv2.resize(frame, (540, 480))
    return frame


def video_object_no_line(frame):   # 前方摄像头调用
    global usr_input, end, ALARM_ON
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = imutils.resize(frame, width=400)
    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    window_height = h
    window_width = w
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            mylib.track_object(frame, startX, startY, endX, endY, window_height - 5 - usr_input)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 1)

    # mylib.draw_guideline(frame, window_height, usr_input)
    frame = cv2.resize(frame, (540, 480))
    return frame


def draw_lines(image):
    mylib.draw_line(image, window_height, usr_input)
    return image


# 检测红灯
def brake_light(image):
    # mylib.draw_guideline(image, window_height, usr_input)
    is_danger = False
    light_on = False
    # extract red
    gray = find_red(image)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]

    # remove small noise point
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    labels = measure.label(thresh, connectivity=1, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")
    # loop over the unique components
    for label in np.unique(labels):
        # if this is the background label, ignore it
        if label == 0:
            continue
        # otherwise, construct the label mask and count the
        # number of pixels
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255
        numPixels = cv2.countNonZero(labelMask)
        # if the number of pixels in the component is sufficiently
        # large, then add it to our mask of "large blobs"
        if 10 < numPixels:
            mask = cv2.add(mask, labelMask)
            # frame,is_close = getRadarFrameByUDP()
            # if is_close =='y':
            light_on = True

    # No brake light detected
    if not light_on:
        return image, is_danger

    if end - start > 1.9:
        t = Thread(target=mylib.alert_sound)
        t.start()
        update_warning_time()
        #t.desdroy()
    ALARM_ON = False
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = contours.sort_contours(cnts)[0]
    # loop over the contours
    for (i, c) in enumerate(cnts):
        # draw the bright spot on the image
        (x, y, w, h) = cv2.boundingRect(c)
        ((cX, cY), radius) = cv2.minEnclosingCircle(c)
        if 160 < cX < 320:
            is_danger = True
        cv2.circle(image, (int(cX), int(cY)), int(radius), (0, 0, 255), 3)
        cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        # show the output image
    return image, is_danger


# 更新报警时间，避免连续播放告警音频
def update_warning_time():
    global start, end
    end += 0.1
    if end - start > 2:
        start = end


# 盲区检测
def blind_object(frame,socket):
    global usr_input, end, ALARM_ON
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = imutils.resize(frame, width=400)
    # grab the frame dimensions and convert it to a blob
    (h, w) = frame.shape[:2]
    window_height = h
    window_width = w
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    # pass the blob through the network and obtain the detections and
    # predictions
    net.setInput(blob)
    detections = net.forward()

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > 0.2:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            if end - start > 0.6:
                if endY >= window_height - 5 - usr_input:
                    if not ALARM_ON:
                        ALARM_ON = True
                        t = Thread(target=mylib.alert_soundtest, args=[endY])
                        t.start()
                        socket.sendFrameByTCP(frame)
                    update_warning_time()
            ALARM_ON = False
            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            mylib.track_object(frame, startX, startY, endX, endY, window_height - 5 - usr_input)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 1)

    frame = mylib.draw_box(frame, window_height, usr_input)
    frame = cv2.resize(frame, (540, 480))
    return frame


# def get_radar():
 #   return mylib.radar_fun()
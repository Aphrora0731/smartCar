import numpy as np
from PIL import Image
import cv2


def RGB(r, g, b): return (r, g, b)


def Make_img_data(width, height, rgb):
    '''Make image data'''
    result = np.zeros((height, width, 3), dtype=np.uint8)
    for i, v in enumerate(rgb):
        result[:, :, i] = np.tile(np.linspace(v, v, width), (height, 1))

    return result


def Make_gradation_img_data(width, height, rgb_start, rgb_stop, horizontal=(True, True, True)):
    '''Make gradation image data'''
    result = np.zeros((height, width, 3), dtype=np.uint8)
    for i, (m, n, o) in enumerate(zip(rgb_start, rgb_stop, horizontal)):
        if o:
            result[:, :, i] = np.tile(np.linspace(m, n, width), (height, 1))
        else:
            result[:, :, i] = np.tile(np.linspace(m, n, width), (height, 1)).T

    return result


MakeImg = lambda width, height, rgb: Image.fromarray(Make_img_data(width, height, rgb))

MakeGradationImg = lambda width, height, rgb_start, rgb_stop, horizontal=(True, True, True): \
    Image.fromarray(Make_gradation_img_data(width, height, rgb_start, rgb_stop, horizontal))


def makeWarning():
    return MakeGradationImg(100, 648, RGB(255, 255,255), RGB(255, 0, 0), (True, True, True))

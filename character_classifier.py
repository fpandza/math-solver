# -*- coding: utf-8 -*-

import tensorflow as tf
import cv2 as cv
import numpy as np

model = tf.keras.models.load_model('math_symbols.h5')


def symbol(ind):
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7',
               '8', '9', '+', '-', ')', '(', 'x', '/']
    symb = symbols[ind.argmax()]
    return symb


def classify(img):
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.resize(img, (45, 45), interpolation=cv.INTER_AREA)
    norm_image = cv.normalize(
        img, None, alpha=0, beta=1, norm_type=cv.NORM_MINMAX, dtype=cv.CV_32F)
    norm_image = norm_image.reshape(
        (norm_image.shape[0], norm_image.shape[1], 1))
    case = np.asarray([norm_image])

    # Run inference on CPU
    with tf.device('/cpu:0'):
        pred = model.predict([case])

    return symbol(pred)

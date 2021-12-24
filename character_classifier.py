# -*- coding: utf-8 -*-

import tensorflow as tf
import cv2
import numpy as np


class Classifier:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        self.symbols = ['0', '1', '2', '3', '4', '5', '6', '7',
                        '8', '9', '+', '-', ')', '(', 'x', '/']

    def classify(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (45, 45), interpolation=cv2.INTER_AREA)
        norm_image = cv2.normalize(
            img, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_image = norm_image.reshape(
            (norm_image.shape[0], norm_image.shape[1], 1))
        case = np.asarray([norm_image])

        # Run inference on CPU
        with tf.device('/cpu:0'):
            pred = self.model.predict([case])

        return self.symbols[pred.argmax()]

    def prepare_images(self, img_list):
        img_list = self._remove_outliers(img_list)
        max_dim = 0

        for img in img_list:
            (H, W) = img.shape[:2]
            max_dim = max(max_dim, max(H, W))

        prepared_img_list = []
        for img in img_list:
            img = self._add_border(img, max_dim)
            img = self._resize_and_pad(img)
            prepared_img_list.append(img)

        return prepared_img_list

    def _remove_outliers(self, img_list):
        img_max_dims = np.array([max(img.shape[:2]) for img in img_list])
        median = np.median(img_max_dims)
        cleaned_imgs = [img for img in img_list if max(
            img.shape[:2]) > median / 5]

        return cleaned_imgs

    def _add_border(self, img, max_dim):
        """
        Add white border based on the difference between largest dimension found in all images
        and the largest dimension of the individual image. Normalizes image sizes for 
        better classification performance.
        """
        (H, W) = img.shape[:2]
        bordersize = int((max_dim - max(H, W)) / 10)
        img = cv2.copyMakeBorder(
            img,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=[255, 255, 255]
        )

        return img

    def _resize_and_pad(self, img, size=(45, 45), padColor=255):

        h, w = img.shape[:2]
        sh, sw = size

        # interpolation method
        if h > sh or w > sw:  # shrinking image
            interp = cv2.INTER_AREA
        else:  # stretching image
            interp = cv2.INTER_CUBIC

        aspect = w/h

        if aspect > 1:  # horizontal image
            new_w = sw
            new_h = np.round(new_w/aspect).astype(int)
            pad_vert = (sh-new_h)/2
            pad_top, pad_bot = np.floor(pad_vert).astype(
                int), np.ceil(pad_vert).astype(int)
            pad_left, pad_right = 0, 0
        elif aspect < 1:  # vertical image
            new_h = sh
            new_w = np.round(new_h*aspect).astype(int)
            pad_horz = (sw-new_w)/2
            pad_left, pad_right = np.floor(pad_horz).astype(
                int), np.ceil(pad_horz).astype(int)
            pad_top, pad_bot = 0, 0
        else:  # square image
            new_h, new_w = sh, sw
            pad_left, pad_right, pad_top, pad_bot = 0, 0, 0, 0

        # color image but only one color provided
        if len(img.shape) == 3 and not isinstance(padColor, (list, tuple, np.ndarray)):
            padColor = [padColor]*3

        # scale and pad
        scaled_img = cv2.resize(img, (new_w, new_h), interpolation=interp)
        scaled_img = cv2.copyMakeBorder(
            scaled_img, pad_top, pad_bot, pad_left, pad_right, borderType=cv2.BORDER_CONSTANT, value=padColor)

        return scaled_img

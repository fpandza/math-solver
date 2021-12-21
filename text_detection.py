# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 22:45:16 2021

@author: Filip
"""


import numpy as np
import cv2


def get_boxes(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (_, blackAndWhiteImage) = cv2.threshold(
        grayImage, 135, 255, cv2.THRESH_BINARY)

    H, W = blackAndWhiteImage.shape[:2]
    reverse_image = cv2.bitwise_not(blackAndWhiteImage)

    horizontal_regions = separateHorizontal(reverse_image)

    char_crops = []

    for region in horizontal_regions:
        x_0 = region[0]
        x_1 = region[1]
        vertical_regions = separateVertical(reverse_image[:, x_0:x_1])

        for region in vertical_regions:
            y_0 = region[0]
            y_1 = region[1]
            char_crops.append((x_0, x_1, y_0, y_1))

    return char_crops


def separateHorizontal(reverse_image):
    empty_vert_lines = []
    (H, W) = reverse_image.shape[:2]

    for vertical_line_index in range(W):
        sum_line = np.sum(reverse_image[:, vertical_line_index])
        if sum_line != 0:
            empty_vert_lines.append(vertical_line_index)

    horizontal_regions = []

    current_region_start = 0
    last_index = -2
    last_line = empty_vert_lines[-1:][0]

    for i in empty_vert_lines:
        if i > last_index+1:
            if last_index != -2:
                horizontal_regions.append((current_region_start, last_index))
            current_region_start = i
        elif i == last_line:
            if current_region_start != last_line-2:
                horizontal_regions.append((current_region_start, i))
        last_index = i

    return horizontal_regions


def separateVertical(reverse_image):
    empty_hor_lines = []
    (H, W) = reverse_image.shape[:2]

    for horizontal_line_index in range(H):
        sum_line = np.sum(reverse_image[horizontal_line_index])
        if sum_line != 0:
            empty_hor_lines.append(horizontal_line_index)

    vertical_regions = []

    current_region_start = 0
    last_index = -2
    last_line = empty_hor_lines[-1:][0]

    for i in empty_hor_lines:
        if i > last_index+1:
            if last_index != -2:
                vertical_regions.append((current_region_start, last_index))
            current_region_start = i
        elif i == last_line:
            if current_region_start != last_line-2:
                vertical_regions.append((current_region_start, i))
        last_index = i

    return vertical_regions

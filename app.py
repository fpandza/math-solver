# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 20:15:43 2021

@author: Filip
"""

import cv2
from text_detection import get_boxes
from math_solver import solve
from character_classifier import classify
import argparse
import sys

# Instantiate the parser
parser = argparse.ArgumentParser(description='Second best math solver app')
parser.add_argument('--image_path', help='Path to input image',
                    default='imgs/twoplustwo.jpg')
parser.add_argument('--direct_equation',
                    help='Optional argument that lets you directly test math \
                    solver functionality by providing the input string of \
                    the equation you wish to test. If provided, no image \
                    is read and character detection and classification are skipped')

args = parser.parse_args()

if args.direct_equation is not None:
    solved_equation = solve(args.direct_equation)
    print(f'{args.direct_equation} = {solved_equation}')
    sys.exit()


image = cv2.imread(args.image_path)
orig = image.copy()

char_crop_boxes = get_boxes(image)
print('Number of detected characters: ', len(char_crop_boxes))

output_string = ''

for box in char_crop_boxes:
    x_0 = box[0]
    x_1 = box[1]
    y_0 = box[2]
    y_1 = box[3]
    cropped_img = image[y_0:y_1, x_0:x_1]
    new_char = classify(cropped_img)
    output_string = output_string + new_char

print("Detected equation: ", output_string)

solved_equation = solve(output_string)
print(f'{output_string} = {solved_equation}')

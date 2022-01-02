# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 20:15:43 2021

@author: Filip
"""

import cv2
from text_detection import get_boxes
from math_solver import solve
from character_classifier import Classifier
import argparse
import sys

# Instantiate the parser
parser = argparse.ArgumentParser(description='Second best math solver app')
parser.add_argument('--image_path', help='Path to input image',
                    default='imgs/big_equation.jpg')
parser.add_argument('--model_path', help='Path to trained model file',
                    default='math_symbols.h5')
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


img_list = []
for box in char_crop_boxes:
    x_0 = box[0]
    x_1 = box[1]
    y_0 = box[2]
    y_1 = box[3]
    cropped_img = image[y_0:y_1, x_0:x_1]
    img_list.append(cropped_img)


classifier = Classifier(args.model_path)
img_list = classifier.prepare_images(img_list)

print('Number of characters after removing noise: ', len(img_list))

output_string = ''

for img in img_list:
    new_char = classifier.classify(img)
    output_string = output_string + new_char

print("Detected equation: ", output_string)

solved_equation = round(float(solve(output_string)), 3)
print('\n###### OUTPUT ######\n')
print(f'{output_string} = {solved_equation}')

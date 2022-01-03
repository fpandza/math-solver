# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 01:21:59 2021

@author: Filip
"""

import re


def split_numbers_and_operations(input_string):

    DELIMITERS = ['+', '-', '/', 'x', '(', ')']
    groups = [input_string]

    for delimiter in DELIMITERS:
        new_groups = []
        for group in groups:
            reg_pattern = re.escape(delimiter)
            split_groups = re.split(f'({reg_pattern})', group)
            if delimiter in ['(', ')']:
                split_groups = [i for i in split_groups if i != '']

            new_groups.extend(split_groups)
        groups = new_groups.copy()

    for group in groups:
        if group == '' or not (group.isdigit() or group in DELIMITERS):
            print(f"Duplicate sign or not (fully) numeric: '{group}'")

    return groups


def multiply_and_divide(expression_numbers):

    resulting_numbers = expression_numbers.copy()

    for i in range(1, len(resulting_numbers), 2):
        try:
            if resulting_numbers[i] == 'x':
                mult_result = float(
                    resulting_numbers[i-1]) * float(resulting_numbers[i+1])
                resulting_numbers = [*resulting_numbers[:i-1],
                                     mult_result, *resulting_numbers[i+2:]]
                return multiply_and_divide(resulting_numbers)
            elif resulting_numbers[i] == '/':
                divide_result = float(
                    resulting_numbers[i-1]) / float(resulting_numbers[i+1])
                resulting_numbers = [*resulting_numbers[:i-1],
                                     divide_result, *resulting_numbers[i+2:]]
                return multiply_and_divide(resulting_numbers)
        except (ValueError, IndexError) as e:
            print(e)
    return resulting_numbers


def add_and_subtract(expression_numbers):

    resulting_numbers = expression_numbers.copy()

    for i in range(1, len(resulting_numbers), 2):
        try:
            if resulting_numbers[i] == '+':
                mult_result = float(
                    resulting_numbers[i-1]) + float(resulting_numbers[i+1])
                resulting_numbers = [*resulting_numbers[:i-1],
                                     mult_result, *resulting_numbers[i+2:]]
                return add_and_subtract(resulting_numbers)
            elif resulting_numbers[i] == '-':
                divide_result = float(
                    resulting_numbers[i-1]) - float(resulting_numbers[i+1])
                resulting_numbers = [*resulting_numbers[:i-1],
                                     divide_result, *resulting_numbers[i+2:]]
                return add_and_subtract(resulting_numbers)
        except (ValueError, IndexError) as e:
            print(e)
    return resulting_numbers


def calculate(expression_numbers):
    resulting_numbers = expression_numbers.copy()
    if resulting_numbers[0] == '-':
        resulting_numbers[0] = resulting_numbers[0] + resulting_numbers[1]
        resulting_numbers.pop(1)

    return add_and_subtract(multiply_and_divide(resulting_numbers))[0]


def parse_brackets_and_calculate(expression_numbers):
    resulting_numbers = expression_numbers.copy()
    bracket_start = -1
    bracket_open = False

    for i, group in enumerate(resulting_numbers):
        if group == '(':
            bracket_open = True
            bracket_start = i
        elif group == ')' and bracket_open is True:
            bracket_open = False
            bracket_calculation = calculate(
                resulting_numbers[bracket_start+1:i])
            resulting_numbers = [*resulting_numbers[:bracket_start],
                                 bracket_calculation, *resulting_numbers[i+1:]]
            return parse_brackets_and_calculate(resulting_numbers)

    return calculate(resulting_numbers)


def solve(input_string):
    return parse_brackets_and_calculate(split_numbers_and_operations(input_string))

# print(solve('(-2+3)x8/((4+223)/155)'))

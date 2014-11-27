#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Simple password generator based on string input

"""

__author__ = "Kristofer Borgström"

import argparse
import copy


def add(pw):
    generated.add(pw)
    print pw


def shift(str, shift_len, right=True):
    if right:
        return str[shift_len:len(str)] + str[0:shift_len]


def flip_case(input_string):
    temp_list = list(input_string)
    for index, character in enumerate(temp_list):
        if character.islower():
            temp_list[index] = character.upper()
        else:
            temp_list[index] = character.lower()
    output_string = ''.join(temp_list)
    return output_string


parser = argparse.ArgumentParser()
parser.add_argument("seed", type=str,
                    help="password seed string")
args = parser.parse_args()


seed = args.seed
generated = set()


#Unaltered
add(seed)

#Inverted
inverted = seed[::-1]
add(inverted)

#Shift standard and inverse
for i in range(len(seed)):
    add(shift(seed, i))
    add(shift(inverted, i))

#Invert case
for existing in copy.copy(generated):
    add(flip_case(existing))

#Increase any number sequences

#Shift char subsets

#change case on subsets

#perform common vowel replacement: o -> 0, a -> 4 etc.










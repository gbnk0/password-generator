#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Simple password generator based on string input

#TODO: Verify functionality of splitting seed into pieces and running algorithms on each piece & clean it up
#TODO: Support combining algorithms
#TODO: Add algorithm: append common words: i.e. "123"
#TODO: Add algorithm: append number sequences
#TODO: Add algorithm: increase existing number sequences
#TODO: Support multiple words
#TODO: language patch: dumb down characters and extend leetspeek

Example default output:

$ ./password-generator.py ro
ro
or
RO
r0
r¤
r()
Ro
rO

"""

__author__ = "Kristofer Borgström"

import argparse
import copy

#TODO: Move to conf file
############ SETTINGS ###############

#If splitting seed into pieces, this is the maximum amount of pieces to split into
MAX_PARTIAL_PIECES = 3

#Mapping table for leetspeak replacement algorithm
leet_mappings = \
    {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['!', '1', '|'],
        'o': ['0', '¤', '()']

    }

############ ALGORITHMS ###############
# Base Rules:
## algorithm performs an action on a supplied string
## algorithm returns a list of string results, even if the result is only one string

"""
Reverse the string

"root" -> ["toor"]
"""


def alg_reverse(str):
    return [str[::-1]]


"""
Cyclically shift characters around

root -> ["ootr", "otro", "troo"]
"""


def alg_shift(str):
    l = []
    for j in range(len(str)):
        l.append(str[j:len(str)] + str[0:j])
    return l

"""
Flips case of the string

"rOot" -> ["RoOT"]
"""


def alg_flip_case(str):
    temp_list = list(str)
    for index, character in enumerate(temp_list):
        if character.islower():
            temp_list[index] = character.upper()
        else:
            temp_list[index] = character.lower()
    output_string = ''.join(temp_list)
    return [output_string]


"""
Replaces configured (in leet_mappings) characters with their leetspeak counterpart(s)

leet_mappings = \
    {
        'a': ['4', '@'],
        'e': ['3']
    }
gives:

"kea" -> ["k34", "k3@"]
"""


def alg_leet_replace(str):

    results = ['']

    for char in str:
        wip = []
        for partial in results:
            if char.lower() in leet_mappings:
                for translated in leet_mappings[char.lower()]:
                    wip.append(partial + translated)
            else:
                wip.append(partial + char)

        results = copy.copy(wip)

    return results

############ Helper functions ###############

"""
Prints new password or list of passwords to system.outvowels
unless the password was already printed
"""


def add(pw):
    if isinstance(pw, basestring):
        if pw not in generated:
            generated.append(pw)
            print pw
    else:
        for p in pw:
            add(p)

"""
Split a string in two pieces, return all possible results as a list of lists.

"root" -> [["r", "oot"], ["ro", "ot"], ["roo", "t"]]
"""

def split_in_two(str):
    results =[]
    l = len(str)
    for i in range(1, l):
        results.append([str[:i], str[i:l]])

    return results


"""
Split strings into all possible pieces as a list of lists without affecting the order of characters.

if MAX_PARTIAL_PIECES is set, this is the maximum amount of pieces returned

if
    MAX_PARTIAL_PIECES = 2

"root" -> [["r", "oot"], ["ro", "ot"], ["roo", "t"]]
"""


def get_pieces(str):
    results = []
    prev_iter = [[str]]
    for i in range(2, min(MAX_PARTIAL_PIECES, len(str)) + 1):
        curr_iter = []
        for prev in prev_iter:

            #Split last word in two pieces if its length is more than 1
            if len(prev[-1]) > 1:

                new_pieces = split_in_two(prev[-1])
                for new_piece_pair in new_pieces:
                    if len(prev) == 1:
                        curr_iter.append(new_piece_pair)
                    elif len(prev) > 1:
                        existing = prev[:-1]
                        new = existing + new_piece_pair
                        curr_iter.append(new)

        prev_iter = copy.copy(curr_iter)
        results.extend(curr_iter)

    return results


"""
Run all of the specified algorithms on the specified str, list order is respected.
"""


def run_algorithms(str, algorithms):
    results = []
    for algorithm in algorithms:
        #Add to results unless this result already exists
        for output in algorithm(str):
            if output not in results:
                results.append(output)

    return results

########### ARGUMENT PARSING #############

parser = argparse.ArgumentParser()
parser.add_argument("seed", type=str,
                    help="password seed string")
args = parser.parse_args()

seed = args.seed

########### SCRIPT LOGIC #########

generated = [] #Keep track of generated passwords to avoid printing dupes
algorithms = [alg_reverse, alg_shift, alg_flip_case, alg_leet_replace]

#Unaltered
add(seed)

#Run all algorithms on the seed
add(run_algorithms(seed, algorithms))

#Split into pieces and run each algorithm on the different pieces selectively
results = []
for partial_list in get_pieces(seed):
    candidates = partial_list

    for i in range(0, len(candidates)):
        #Run algorithm on part i
        candidate = candidates[i]
        outputs = run_algorithms(candidate, algorithms)
        prefix = []
        if i > 0:
            prefix = candidates[:i]

        suffix = []
        if i < len(candidates):
            suffix = candidates[i+1:len(candidates)]

        for output in outputs:
            results.append(prefix + [output] + suffix)


for result in results:
    add("".join(result))









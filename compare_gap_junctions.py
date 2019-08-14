#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:24:02 2019

@author: zhenlab
"""

# Get the gap junctions from project 129 (Christine) and compare them to the White datasets
from config import token, project_id, stack_id

from neuron_info import nclass
from catmaid_api import get_gap_junctions_from_catmaid
from durbin_file_api import get_gap_junctions_from_durbin

import pprint
pp = pprint.PrettyPrinter(indent=4)

# get the gap junctions and set of gap junctions from the catmaid project
cgj, cgj_set = get_gap_junctions_from_catmaid(token, project_id, stack_id)
# get the gap junctions and set of gap junctions from the durbin dataset
dgj, dgj_set = get_gap_junctions_from_durbin()


# compute intersection, difference, of gap junctions for christines project and durbins dataset
gj_intersection = cgj_set & dgj_set
durbin_unique = dgj_set - cgj_set
christine_unique = cgj_set - dgj_set


# write the results to csv file
SEM_UNIQUE_OUTPUT_FILE = open('./output/christine_unique.csv', 'w+')
DURBIN_UNIQUE_OUTPUT_FILE = open('./output/durbin_unique.csv', 'w+')

SEM_UNIQUE_OUTPUT_FILE.write("{},{}\n".format('Unique class pairs', len(christine_unique)))
SEM_UNIQUE_OUTPUT_FILE.write(',,,,,,\n')
SEM_UNIQUE_OUTPUT_FILE.write(',,,,,,\n')
SEM_UNIQUE_OUTPUT_FILE.write("{},{},{},{}\n".format('neuron 1', 'neuron 2', 'weight', 'link'))
for gj_tuple in sorted(christine_unique, key=lambda tup: tup[0] + tup[1]):

    lines = []
    for gj_info in sorted(cgj, key= lambda o: o['class_set'][0]):
        if gj_info['class_set'] == gj_tuple:
            neurons = sorted([gj_info['n1_name'], gj_info['n2_name']])

            pre = neurons[0]
            post = neurons[1]
            link = gj_info['link']
            lines.append([pre, post, link])

    SEM_UNIQUE_OUTPUT_FILE.write("{},{},{}\n".format(gj_tuple[0], gj_tuple[1], len(lines)))

    for line in lines:
        SEM_UNIQUE_OUTPUT_FILE.write("{},{}, ,{}\n".format(line[0], line[1], line[2]))

    SEM_UNIQUE_OUTPUT_FILE.write(',,,,,,\n')


DURBIN_UNIQUE_OUTPUT_FILE.write("{},{}\n".format('Unique class pairs', len(durbin_unique)))
DURBIN_UNIQUE_OUTPUT_FILE.write(',,,,,,\n')
DURBIN_UNIQUE_OUTPUT_FILE.write(',,,,,,\n')
DURBIN_UNIQUE_OUTPUT_FILE.write("{},{},{},{}\n".format('neuron 1', 'neuron 2', 'weight', 'link'))
for gj_tuple in sorted(durbin_unique, key=lambda tup: tup[0] + tup[1]):

    lines = []
    for gj_info in sorted(dgj, key = lambda o: o['class_set'][0]):
        if gj_info['class_set'] == gj_tuple:
            neurons = sorted([gj_info['n1_name'], gj_info['n2_name']])

            pre = neurons[0]
            post = neurons[1]
            link = gj_info['link']
            lines.append([pre, post, link])

    DURBIN_UNIQUE_OUTPUT_FILE.write("{},{},{}\n".format(gj_tuple[0], gj_tuple[1], len(lines)))

    for line in lines:
        DURBIN_UNIQUE_OUTPUT_FILE.write("{},{}, ,{}\n".format(line[0], line[1], line[2]))

    DURBIN_UNIQUE_OUTPUT_FILE.write(',,,,,,\n')

DURBIN_UNIQUE_OUTPUT_FILE.close()
SEM_UNIQUE_OUTPUT_FILE.close()
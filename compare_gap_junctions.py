#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:24:02 2019

@author: zhenlab
"""

# Get the gap junctions from project 129 (Christine) and compare them to the White datasets

from neuron_info import nclass
from catmaid_api import get_gap_junctions_from_catmaid
from durbin_file_api import get_gap_junctions_from_durbin

import pprint
pp = pprint.PrettyPrinter(indent=4)

# get the gap junctions and set of gap junctions from the catmaid project
cgj, cgj_set = get_gap_junctions_from_catmaid()
# get the gap junctions and set of gap junctions from the durbin dataset
dgj, dgj_set = get_gap_junctions_from_durbin()


# compute intersection, difference, of gap junctions for christines project and durbins dataset
gj_intersection = cgj_set & dgj_set
durbin_unique = dgj_set - cgj_set
christine_unique = cgj_set - dgj_set

pp.pprint(sorted(cgj, key= lambda o: o['class_set'])[:20])

# write the results to csv file
SEM_UNIQUE_OUTPUT_FILE = open('./output/sem_unique.csv', 'w+')
DURBIN_UNIQUE_OUTPUT_FILE = open('./output/durbin_unique.csv', 'w+')
INTERSECTION_OUTPUT_FILE = open('./output/intersection.csv', 'w+')


for gj_info in sorted(cgj, key= lambda o: o['class_set']):
    class_set = gj_info['class_set']

    pre = gj_info['n1_name']
    post = gj_info['n2_name']
    link = gj_info['link']
    if class_set in gj_intersection:
        INTERSECTION_OUTPUT_FILE.write("{},{},{}\n".format(pre, post, link))
    elif class_set in christine_unique:
        SEM_UNIQUE_OUTPUT_FILE.write("{},{},{}\n".format(pre, post, link))


for gj_tuple in sorted(durbin_unique, key=lambda tup: tup[0] + tup[1]):
    for gj_info in sorted(dgj, key = lambda o: o['class_set'][0]):
        if gj_info['class_set'] == gj_tuple:
            pre = gj_info['n1_name']
            post = gj_info['n2_name']
            link = gj_info['link']
            DURBIN_UNIQUE_OUTPUT_FILE.write("{},{},{}\n".format(pre, post, link))



# for gj_tuple in sorted(christine_unique, key=lambda tup: tup[0] + tup[1]):
#     for gj_info in sorted(cgj, key= lambda o: o['class_set'][0]):
#         if gj_info['class_set'] == gj_tuple:
#             pre = gj_info['n1_name']
#             post = gj_info['n2_name']
#             link = gj_info['link']
#             SEM_UNIQUE_OUTPUT_FILE.write("{},{},{}\n".format(pre, post, link))

# for gj_tuple in sorted(gj_intersection, key=lambda tup: tup[0] + tup[1]):
    # for gj_info in sorted(cgj, key= lambda o: o['class_set'][0]):
    #     if gj_info['class_set'] == gj_tuple:
    #         pre = gj_info['n1_name']
    #         post = gj_info['n2_name']
    #         link = gj_info['link']
    #         INTERSECTION_OUTPUT_FILE.write("{},{},{}\n".format(pre, post, link))

DURBIN_UNIQUE_OUTPUT_FILE.close()
SEM_UNIQUE_OUTPUT_FILE.close()
INTERSECTION_OUTPUT_FILE.close()
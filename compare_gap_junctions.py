#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:24:02 2019

@author: zhenlab
"""

# Get the gap junctions from project 129 (Christine) and compare them to the White datasets
from config import token, project_id, stack_id, jsh_project_id, jsh_stack_id, n2u_project_id, n2u_stack_id

from neuron_info import get_neuron_class
from catmaid_api import get_gap_junctions_from_catmaid
from durbin_file_api import get_gap_junctions_from_durbin

import pprint
pp = pprint.PrettyPrinter(indent=4)

# get the gap junctions and set of gap junctions from the catmaid project
cgj, cgj_set = get_gap_junctions_from_catmaid(token, project_id, stack_id)

# catmaid has some links to some gap junctions in the durbin datasets
jshgj, _ = get_gap_junctions_from_catmaid(token, jsh_project_id, jsh_stack_id)
n2ugj, _ = get_gap_junctions_from_catmaid(token, n2u_project_id, n2u_stack_id)

# get the gap junctions and set of gap junctions from the durbin dataset file
dgj, dgj_set = get_gap_junctions_from_durbin()

for gj_info in jshgj:
    class_info = gj_info['class_set']

    for dgj_info in dgj:
        if dgj_info['class_set'] == class_info:
            gj_info['dataset'] = dgj_info['dataset']

for gj_info in n2ugj:
    class_info = gj_info['class_set']

    for dgj_info in dgj:
        if dgj_info['class_set'] == class_info:
            gj_info['dataset'] = dgj_info['dataset']



# compute intersection, difference, of gap junctions for christines project and durbins dataset
gj_intersection = cgj_set & dgj_set
durbin_unique = dgj_set - cgj_set
christine_unique = cgj_set - dgj_set

def write_results_to_file(f_path, gj_set, gj_info, durbin_unique=False):
    f = open(f_path, 'w+')

    # write general info such as unique class pairs, table column names
    f.write("{},{}\n".format('Unique class pairs', len(gj_set)))
    f.write(',,,,,,\n')
    f.write(',,,,,,\n')
    f.write("{},{},{},{}\n".format('neuron 1', 'neuron 2', 'weight', 'link'))

    # write main bulk data
    for gj_tuple in sorted(gj_set, key=lambda tup: tup[0] + tup[1]):

        gap_junctions_matching_classes = []
        for gj in sorted(gj_info, key= lambda o: o['class_set'][0]):
            if gj['class_set'] == gj_tuple:
                neurons = sorted([gj['n1_name'], gj['n2_name']])

                pre = neurons[0]
                post = neurons[1]
                link = gj['link']
                dataset = gj.get('dataset', '')
                content = ', '.join([pre, post, '', link, dataset]) + '\n'
                gap_junctions_matching_classes.append(content)

        gj_class_header = [gj_tuple[0], gj_tuple[1], len(gap_junctions_matching_classes)]
        dataset = ''
        for gj_i in dgj:
            if gj_i['class_set'] == gj_tuple:
                dataset = gj_i['dataset']
        gj_class_header.append(dataset)

        # write the neuron classes and the weight between them
        class_header_content = ', '.join(str(x) for x in gj_class_header) + '\n'
        f.write(class_header_content)

        # write all gap junctions that match the class pair
        for line in gap_junctions_matching_classes:
            f.write(line)

        f.write(',,,,,,\n')

    f.close()

# write results to file
write_results_to_file('./output/christine_unique.csv', christine_unique, cgj)
write_results_to_file('./output/durbin_unique.csv', durbin_unique, jshgj + n2ugj, True)
write_results_to_file('./output/intersection.csv', gj_intersection, cgj)
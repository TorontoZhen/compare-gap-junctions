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

pp.pprint(cgj_set)
pp.pprint(dgj_set)

print 'INTERSECTION #################################################'
gj_intersection = cgj_set & dgj_set
print gj_intersection
print len(gj_intersection)
print 'UNIQUE TO DURBIN #################################################'
durbin_unique = dgj_set - cgj_set
print durbin_unique
print len(durbin_unique)
print 'UNIQUE TO CHRISTINE ##############################################'
christine_unique = cgj_set - dgj_set
print christine_unique
print len(christine_unique)

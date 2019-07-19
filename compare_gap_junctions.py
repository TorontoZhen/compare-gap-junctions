#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:24:02 2019

@author: zhenlab
"""

# Get the gap junctions from project 129 (Christine) and compare them to the White datasets

import requests
from collections import defaultdict

from requests.auth import HTTPBasicAuth
from neuron_info import nclass
import networkx as nx

from networkx.algorithms.operators import binary


from config import token, project_id, stack_id


class CatmaidApiTokenAuth(HTTPBasicAuth):
    def __init__(self, token, username=None, password=None):
        super(CatmaidApiTokenAuth, self).__init__(username, password)
        self.token = token
    def __call__(self, r):
        r.headers['X-Authorization'] = 'Token {}'.format(self.token)
        if self.username and self.password:
            super(CatmaidApiTokenAuth, self).__call__(r)
        return r


def get_gap_junctions_from_catmaid():
    annotation_response = requests.post(
        'https://catmaid.nemanode.org/' + str(project_id) + '/annotations/query-targets',
        auth=CatmaidApiTokenAuth(token)
    ).json()

    skeleton_list = [s for s in annotation_response['entities']]

    skid_to_name = {}
    for skeleton in skeleton_list:

        if skeleton['type'] != 'neuron':
            continue

        skid = skeleton['skeleton_ids'][0]
        name = skeleton['name']

        skid_to_name[skid] = name

    # Get all synapses.
    connector_response = requests.post(
        'https://catmaid.nemanode.org/' + str(project_id) + '/connectors/',
        data={
            'with_partners': True,
            'relation_type': 'gapjunction_with'
        },
        auth=CatmaidApiTokenAuth(token)
    ).json()

    synapses = set()

    for synapse_id, partners in connector_response['partners'].items():

       if len(partners) != 2:
           print('Warning: something is wrong with synapse'), synapse_id
           continue


       neuron1_id = partners[0][2]
       neuron2_id = partners[1][2]

       neuron1_name = skid_to_name[neuron1_id].replace('[', '').replace(']', '')
       neuron2_name = skid_to_name[neuron2_id].replace('[', '').replace(']', '')

       n_classes = [nclass(neuron1_name), nclass(neuron2_name)]
       n_classes.sort()

       processed_synapse = (n_classes[0], n_classes[1])
       synapses.add(processed_synapse)

    return synapses


# Load Durbin datasets.
# file is directly from wormatlas.
# - No duplicate connections are present.
# - PVT is replaced by DVB.
# - There are 48 connections between neurons that are inconstistent
#   when comparing Send(_joint) with Receive(_joint) and when
#   comparing gap junctions. These connections were either missed in
#   one direction (35) or deviate by one or two synapses (13). Taking
#   the max should resolve both issues.

# Load txt file and make connections constistent with themselves.

durbin_data_path = './data/edgelist_durbin.txt'
def get_gap_junctions_from_durbin(path):
    edges = defaultdict(int)


    edges_done = []
    with open(path) as f:
        for l in f:
            pre, post, typ, dataset, synapses = l.strip().split('\t')

            # Skip muscles as they were reannotated.
            if post == 'mu_bod':
                continue

            synapses = int(synapses)
            pre = pre.replace('DVB', 'PVT')
            post = post.replace('DVB', 'PVT')

            rev_type = {'Gap_junction': 'Gap_junction',
                        'Send': 'Receive',
                        'Receive': 'Send',
                        'Send_joint': 'Receive_joint',
                        'Receive_joint': 'Send_joint'}

            key = (dataset, typ, pre, post)
            rev_key = (dataset, rev_type[typ], post, pre)

            edges[key] = max(edges[key], synapses)
            edges[rev_key] = max(edges[rev_key], synapses)

        # AIA -> ASK was very clearly missed in JSH.
        edges[('JSH', 'Send', 'AIAL', 'ASKL')] = 1
        edges[('JSH', 'Send', 'AIAR', 'ASKR')] = 1
        # DVA -> ASK was very clearly missed in JSH.
        edges[('JSH', 'Send', 'DVA', 'AIZL')] = 1
        edges[('JSH', 'Send', 'DVA', 'AIZR')] = 1
        # ADLL -> ASHL was very clearly missed in JSH
        edges[('JSH', 'Send', 'ADLL', 'ASHL')] = 3
        # ADE -> RMG is present in the MoW drawings, but missed by Durbin.
        edges[('N2U', 'Send', 'ADEL', 'RMGL')] = 3
        edges[('N2U', 'Send', 'ADER', 'RMGR')] = 2

        edges_done = set()

        for edge, synapses in edges.items():

            dataset, typ, pre, post = edge

            dataset = {'N2U': 'white_adult', 'JSH': 'white_l4'}[dataset]

            if typ == 'Gap_junction' and (post, pre, dataset) not in edges_done:
                n_classes = [nclass(pre), nclass(post)]
                n_classes.sort()
                edges_done.add((n_classes[0], n_classes[1]))

    return edges_done

def gj_in_dataset(gj, dataset):
    gj_found = False

    for gjds in dataset:
        gjds_0 = gjds[0]
        gjds_1 = gjds[1]

        gj_0 = gj[0]
        gj_1 = gj[1]

        found0 = gj_0 == gjds_0 and gj_1 == gjds_1
        found1 = gj_1 == gjds_0 and gj_0 == gjds_1
        if found0 or found1:
            gj_found = True

    return gj_found



# Get the gap junctions and replace neuron names with their classes
# also translate the data into a common format: tuples of (neuronClass1, neuronClass2, datasetName)
christine_gap_junctions = get_gap_junctions_from_catmaid()
durbin_gap_junctions = get_gap_junctions_from_durbin(durbin_data_path)


gj_in_both = []
gj_in_christine_dataset_only = []
gj_in_durbin_dataset_only = []

for gj in christine_gap_junctions:

    if gj_in_dataset(gj, durbin_gap_junctions):
        gj_in_both.append(gj)
    else:
        gj_in_christine_dataset_only.append(gj)


for gj in durbin_gap_junctions:

    if gj_in_dataset(gj, christine_gap_junctions):
        gj_in_both.append(gj)
    else:
        gj_in_durbin_dataset_only.append(gj)

print(len(christine_gap_junctions))
print(len(durbin_gap_junctions))
print(christine_gap_junctions)
print(durbin_gap_junctions)
print('INTERSECTION #################################################')
print(len(christine_gap_junctions & durbin_gap_junctions))
print('UNIQUE TO DURBIN #################################################')
print(len(durbin_gap_junctions - christine_gap_junctions))
print('UNIQUE TO CHRISTINE ##############################################')
print(len(christine_gap_junctions - durbin_gap_junctions))
#print len(gj_in_both)
#print len(gj_in_christine_dataset_only)
#print len(gj_in_durbin_dataset_only)

from requests.auth import HTTPBasicAuth
import requests

import pprint
pp = pprint.PrettyPrinter(indent=4)

from neuron_info import is_neuron, is_neuron_class, get_neuron_class


class CatmaidApiTokenAuth(HTTPBasicAuth):
    def __init__(self, token, username=None, password=None):
        super(CatmaidApiTokenAuth, self).__init__(username, password)
        self.token = token
    def __call__(self, r):
        r.headers['X-Authorization'] = 'Token {}'.format(self.token)
        if self.username and self.password:
            super(CatmaidApiTokenAuth, self).__call__(r)
        return r


def get_catmaid_link(coordinates, project_id, stack_id):
  x, y, z = coordinates
  return 'https://catmaid.nemanode.org/?pid={}&zp={}&yp={}&xp={}&tool=tracingtool&sid0={}&s0=0'.format(project_id, z, y, x, stack_id)

def get_skeleton_id_to_neuron_name_map(token, project_id):
  annotation_response = requests.post(
    'https://catmaid.nemanode.org/' + str(project_id) + '/annotations/query-targets',
    auth=CatmaidApiTokenAuth(token)
  ).json()


  skeleton_id_to_neuron_name_map = {}

  for entity in annotation_response['entities']:

    # sometimes entity name is a string formatted like: ['AVAR'] or 'AVAR?'
    # remove brackets and '?' to get something like 'AVAR'
    name = entity['name'].replace('[', '').replace(']', '').replace('?', '')

    if entity['type'] != 'neuron':
      continue

    # discard if not a neuron name and not a neuron class
    if not (is_neuron(name) or is_neuron_class(name) ):
      continue

    skid = entity['skeleton_ids'][0]

    skeleton_id_to_neuron_name_map[skid] = name

  return skeleton_id_to_neuron_name_map


def get_gap_junctions_from_catmaid(token, project_id, stack_id):
  skid_to_name = get_skeleton_id_to_neuron_name_map(token, project_id)

  connector_response = requests.post(
    'https://catmaid.nemanode.org/' + str(project_id) + '/connectors/',
    data={
        'with_partners': True,
        'relation_type': 'gapjunction_with'
    },
    auth=CatmaidApiTokenAuth(token)
  ).json()


  gap_junction_ids = {}
  for connector in connector_response['connectors']:
    gj_id, x, y, z, _, _, _, _, _ = connector

    gap_junction_ids[gj_id] = {
      'coordinates': (x, y, z)
    }

  gap_junctions = []
  gap_junctions_set = set()
  for gj_id, partners in connector_response['partners'].items():
    neuron1_id = partners[0][2]
    neuron2_id = partners[1][2]
    gj_id = int(gj_id)

    if neuron1_id not in skid_to_name or neuron2_id not in skid_to_name:
      continue

    neuron1_name = skid_to_name[neuron1_id]
    neuron2_name = skid_to_name[neuron2_id]

    nc1 = get_neuron_class(neuron1_name)
    nc2 = get_neuron_class(neuron2_name)

    n_classes = [nc1, nc2]
    n_classes.sort()

    if gj_id not in gap_junction_ids:
      continue

    coordinates = gap_junction_ids[gj_id]['coordinates']
    gj = {}
    gj['gj_id'] = gj_id
    gj['n1_name'] = neuron1_name
    gj['n2_name'] = neuron2_name
    gj['n1_class'] = nc1
    gj['n2_class'] = nc2
    gj['class_set'] = (n_classes[0], n_classes[1])
    gj['link'] = get_catmaid_link(coordinates, project_id, stack_id)

    gap_junctions_set.add(gj['class_set'])
    gap_junctions.append(gj)

  return gap_junctions, gap_junctions_set
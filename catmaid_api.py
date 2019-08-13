from config import token
from requests.auth import HTTPBasicAuth
import requests

from neuron_info import is_neuron, is_neuron_class, nclass


class CatmaidApiTokenAuth(HTTPBasicAuth):
    def __init__(self, token, username=None, password=None):
        super(CatmaidApiTokenAuth, self).__init__(username, password)
        self.token = token
    def __call__(self, r):
        r.headers['X-Authorization'] = 'Token {}'.format(self.token)
        if self.username and self.password:
            super(CatmaidApiTokenAuth, self).__call__(r)
        return r


class CatmaidApi:
  def __init__(self, token):
    self.auth = CatmaidApiTokenAuth(token)

  def get_skeleton_id_to_neuron_name_map(self, project_id):
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

  def get_gap_junctions(self, project_id):

    skid_to_name = self.get_skeleton_id_to_neuron_name_map(project_id)
    connector_response = requests.post(
      'https://catmaid.nemanode.org/' + str(project_id) + '/connectors/',
      data={
          'with_partners': True,
          'relation_type': 'gapjunction_with'
      },
      auth=CatmaidApiTokenAuth(token)
    ).json()

    gap_junctions = set()

    for synapse_id, partners in connector_response['partners'].items():
      neuron1_id = partners[0][2]
      neuron2_id = partners[1][2]


      if neuron1_id not in skid_to_name or neuron2_id not in skid_to_name:
        continue

      neuron1_name = skid_to_name[neuron1_id]
      neuron2_name = skid_to_name[neuron2_id]

      nc1, _ = nclass(neuron1_name)
      nc2, _ = nclass(neuron2_name)

      n_classes = [nc1, nc2]
      n_classes.sort()

      gap_junctions.add((n_classes[0], n_classes[1]))

    return gap_junctions



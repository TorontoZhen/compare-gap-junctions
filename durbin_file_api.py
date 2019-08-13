from collections import defaultdict
from neuron_info import nclass

import pprint
pp = pprint.PrettyPrinter(indent=4)


durbin_data_path = './data/edgelist_durbin.txt'

def get_gap_junctions_from_durbin():
  edges = defaultdict(int)


  gap_junctions = []
  gap_junctions_set = set()
  with open(durbin_data_path) as f:
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

      for edge, synapses in edges.items():

          dataset, typ, pre, post = edge

          dataset = {'N2U': 'white_adult', 'JSH': 'white_l4'}[dataset]

          if typ == 'Gap_junction':
            nc1, _ = nclass(pre)
            nc2, _ = nclass(post)
            n_classes = [nc1, nc2]
            n_classes.sort()

            gj = {}
            gj['gj_id'] = ''
            gj['n1_name'] = pre
            gj['n2_name'] = post
            gj['n1_class'] = nc1
            gj['n2_class'] = nc2
            gj['class_set'] = (n_classes[0], n_classes[1])
            gj['link'] = 'N/A'

            gap_junctions_set.add(gj['class_set'])
            gap_junctions.append(gj)

  return gap_junctions, gap_junctions_set
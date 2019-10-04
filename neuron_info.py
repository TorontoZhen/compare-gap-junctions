import re

import json

neurons_data_path = './data/neurons.json'

data = None

with open(neurons_data_path) as json_file:
    data = json.load(json_file)



def is_neuron(neuron_name):
    found = False

    for neuron in data:
        if neuron['name'] == neuron_name:
            found = True
            break

    return found

def is_neuron_class(neuron_class):
    found = False

    for neuron in data:
        if neuron['classes'] == neuron_class:
            found = True
            break

    return found


def get_neuron_class(neuron_name):
    neuron_class = ''
    for neuron in data:
        if neuron['name'] == neuron_name:
            neuron_class = neuron['classes']
            break

    return neuron_class

def class_members(cls):
    pass


def ntype(n):
    pass


def is_postemb(n):
    pass

def in_nervering(n):
    pass

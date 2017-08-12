import numpy
import simplejson

def ids(synname):
    #Function:  ids
    #Input:     synapse file name
    #Process:   create list of neuron ID
    #Output:    neuron ID list

    synlist = []

    open_file = open(synname,'r')
    syndata = simplejson.load(open_file)['data']

    checklist = []

    for i in range(len(syndata)):
        if len(syndata[i]['partners']) > 0:
            synlist.append(syndata[i]['T-bar']['body ID'])

    synlist = list(set(synlist))

    return synlist

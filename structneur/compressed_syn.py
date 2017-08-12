import numpy
from scipy.spatial import distance
from neuron import h

def synapse(sender,receiver,synloc,e=0):
    #Function:  synapse
    #Input:     presynaptic neuron class, postsynaptic neuron class
    #Process:   connect neurons
    #Output:    synapse of neurons

    sdistances = []
    rdistances = []

    for sd in sender.dendgraph.keys():

        sdistances.append([sd,distance.euclidean(sender.dendgraph[sd],synloc)])

    for rd in receiver.dendgraph.keys():

        rdistances.append([rd,distance.euclidean(receiver.dendgraph[rd],synloc)])

    sdistances = numpy.array(sdistances)
    rdistances = numpy.array(rdistances)

    senderdend      = sdistances[numpy.argmin(sdistances[:,1])][0]
    receiverdend    = rdistances[numpy.argmin(rdistances[:,1])][0]

    syn = h.AlphaConvol(0.5, sec=receiver.compartmentdict[receiverdend][1])
    syn.e = e
    if syn.e == -80:
        syn.k = 2.81e-4
    h.setpointer(sender.compartmentdict[senderdend][1](0.5)._ref_v,'Vpre', syn)

    return syn

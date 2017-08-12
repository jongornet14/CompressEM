from neuron import h

def synapse(sender,receiver,e=0):
    #Function:  synapse
    #Input:     presynaptic and postsynaptic neuron classes
    #Process:   create synapse
    #Output:    synapse

    syn = h.AlphaConvol(0.5, sec=receiver.soma)
    syn.e = e
    if syn.e == -80:
        syn.k = 2.81e-4
    h.setpointer(sender.soma(0.5)._ref_v,'Vpre', syn)

    return syn

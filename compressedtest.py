from structneur import compressed_neur
import pickle
from neuron import h, gui
from matplotlib import pyplot
import numpy
from sys import argv
from scipy.spatial import distance
import simplejson

fileloc = open('locationdic.json', 'r')
datadict = simplejson.load(fileloc)
fileloc.close()


def Compartment(stimdir):

    """This is the program for the compartment model in the paper _.
    When using this program use the following command:

        ./x86_64/special -python compartmenttest.py (number)

    Where the numbers are for the direction of the signal:

    (number)
    0: 'rl'
    1: 'du'
    2: 'lr'
    3: 'ud'
    4: 'full' (forward direction)

    The data will be saved in the ./data/compartment directory."""

    #--------------------------------------------------------------------------------------------------------------------------------------------

    datafile = open(datadict['L1data'],'r')
    L1list = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['Mi1data'],'r')
    Mi1list = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['Tm3data'],'r')
    Tm3list = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['Mi4data'],'r')
    Mi4list = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['Mi9data'],'r')
    Mi9list = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['T4data'],'r')
    T4list = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['T4adata'],'r')
    T4alist = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['T4bdata'],'r')
    T4blist = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['T4cdata'],'r')
    T4clist = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['T4ddata'],'r')
    T4dlist = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict[stimdir],'r')
    stimdata = pickle.load(datafile)
    datafile.close()

    datafile = open(datadict['totaldata'],'r')
    fulldata = pickle.load(datafile)
    datafile.close()

    #--------------------------------------------------------------------------------------------------------------------------------------------

    area = {}

    neurdic = {}

    print('Creating cells...')

    count = 0

    #--------------------------------------------------------------------------------------------------------------------------------------------

    for f in range(len(fulldata)):

        if fulldata[f] == None:

            continue

        else:

            #--------------------------------------------------------------------------------------------------------------------------------------------

            if fulldata[f].cellID in L1list:

                neurdic[fulldata[f].cellID] = compressed_neur.cell(fulldata[f])
                area[fulldata[f].cellID] = neurdic[fulldata[f].cellID].totalarea

                print(area[fulldata[f].cellID])
                count += len(neurdic[fulldata[f].cellID].compartmentdict)
                break
                
    #--------------------------------------------------------------------------------------------------------------------------------------------

    print('Compartments: ' + str(count))

    datadict['areas'] = datadict['dataloc'] + 'areas.json'

    datafile = open(datadict['areas'],'w')
    simplejson.dump(area,datafile)
    datafile.close()

    fileloc = open('locationdic.json', 'w')
    simplejson.dump(datadict,fileloc)
    fileloc.close()

    #--------------------------------------------------------------------------------------------------------------------------------------------

    print('Connecting cells..')

    #--------------------------------------------------------------------------------------------------------------------------------------------

    from structneur import compressed_syn

    connections = {
    #L1
    'L1_L1'     :[L1list,L1list],
    'L1_Mi1'    :[L1list,Mi1list],
    'L1_Mi4'    :[L1list,Mi4list],
    'L1_Mi9'    :[L1list,Mi9list],
    'L1_Tm3'    :[L1list,Tm3list],
    'L1_T4'     :[L1list,T4list],

    #Mi1
    'Mi1_Mi1'   :[Mi1list,Mi1list],
    'Mi1_L1'    :[Mi1list,L1list],
    'Mi1_Tm3'   :[Mi1list,Tm3list],
    'Mi1_Mi4'   :[Mi1list,Mi4list],
    'Mi1_Mi9'   :[Mi1list,Mi9list],
    'Mi1_T4'    :[Mi1list,T4list],

    #Tm3
    'Tm3_Tm3'   :[Tm3list,Tm3list],
    'Tm3_L1'    :[Tm3list,L1list],
    'Tm3_Mi1'   :[Tm3list,Mi1list],
    'Tm3_Mi4'   :[Tm3list,Mi4list],
    'Tm3_Mi9'   :[Tm3list,Mi9list],
    'Tm3_T4'    :[Tm3list,T4list],

    #Mi4
    'Mi4_Mi4'   :[Mi4list,Mi4list],
    'Mi4_L1'    :[Mi4list,L1list],
    'Mi4_Mi1'   :[Mi4list,Mi1list],
    'Mi4_Tm3'   :[Mi4list,Tm3list],
    'Mi4_Mi9'   :[Mi4list,Mi9list],
    'Mi4_T4'    :[Mi4list,T4list],

    #Mi9
    'Mi9_Mi9'   :[Mi9list,Mi9list],
    'Mi9_L1'    :[Mi9list,L1list],
    'Mi9_Mi1'   :[Mi9list,Mi1list],
    'Mi9_Tm3'   :[Mi9list,Tm3list],
    'Mi9_Mi4'   :[Mi9list,Mi4list],
    'Mi9_T4'    :[Mi9list,T4list],

    #T4
    'T4_T4'     :[T4list,T4list],
    'T4_L1'     :[T4list,L1list],
    'T4_Mi1'    :[T4list,Mi1list],
    'T4_Tm3'    :[T4list,Tm3list],
    'T4_Mi4'    :[T4list,Mi4list],
    'T4_Mi9'    :[T4list,Mi9list],
    }

    #--------------------------------------------------------------------------------------------------------------------------------------------

    datadict['connections'] = datadict['dataloc'] + 'connections.json'

    datafile = open(datadict['connections'],'w')
    simplejson.dump(connections,datafile)
    datafile.close()

    fileloc = open('locationdic.json', 'w')
    simplejson.dump(datadict,fileloc)
    fileloc.close()

    synlist = []

    #--------------------------------------------------------------------------------------------------------------------------------------------

    for key in neurdic.keys():

        neurdic[key].create_stim(55)

        #Stimuli-----------------------------------------------------------------------------------------------
        if str(stimdir) == 'full':
            if key in stimdata:
                neurdic[key].create_stim(55)
        else:
            if key in stimdata[0]:
                neurdic[key].create_stim(55)
            if key in stimdata[1]:
                neurdic[key].create_stim(155)
            if key in stimdata[2]:
                neurdic[key].create_stim(255)
            if key in stimdata[3]:
                neurdic[key].create_stim(355)
            if key in stimdata[4]:
                neurdic[key].create_stim(455)

        for p in neurdic[key].partners:

            pID  = p[0]
            ploc = p[1]

            sdistances = []
            rdistances = []

            if pID in neurdic.keys():

                receiver = neurdic[pID]
                sender   = neurdic[key]
                synloc   = ploc

                #L1-----------------------------------------------------------------------------------------------
                """if key in connections['L1_L1'][0] and pID in connections['L1_L1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,tau=50)

                    synlist.append(info)"""

                if key in connections['L1_Mi1'][0] and pID in connections['L1_Mi1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['L1_Tm3'][0] and pID in connections['L1_Tm3'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                #Mi1-----------------------------------------------------------------------------------------------
                """if key in connections['Mi1_Mi1'][0] and pID in connections['Mi1_Mi1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)"""

                """if key in connections['Mi1_L1'][0] and pID in connections['Mi1_L1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)"""

                if key in connections['Mi1_Tm3'][0] and pID in connections['Mi1_Tm3'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['Mi1_Mi4'][0] and pID in connections['Mi1_Mi4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['Mi1_Mi9'][0] and pID in connections['Mi1_Mi9'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['Mi1_T4'][0] and pID in connections['Mi1_T4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                #Tm3-----------------------------------------------------------------------------------------------
                """if key in connections['Tm3_Tm3'][0] and pID in connections['Tm3_Tm3'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)"""

                """if key in connections['Tm3_L1'][0] and pID in connections['Tm3_L1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)"""

                if key in connections['Tm3_Mi1'][0] and pID in connections['Tm3_Mi1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['Tm3_Mi4'][0] and pID in connections['Tm3_Mi4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['Tm3_Mi9'][0] and pID in connections['Tm3_Mi9'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                if key in connections['Tm3_T4'][0] and pID in connections['Tm3_T4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc)

                    synlist.append(info)

                #Mi4-----------------------------------------------------------------------------------------------
                """if key in connections['Mi4_Mi4'][0] and pID in connections['Mi4_Mi4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi4_Mi1'][0] and pID in connections['Mi4_Mi1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi4_Tm3'][0] and pID in connections['Mi4_Tm3'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)"""

                if key in connections['Mi4_Mi9'][0] and pID in connections['Mi4_Mi9'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)

                if key in connections['Mi4_T4'][0] and pID in connections['Mi4_T4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)

                #Mi9-----------------------------------------------------------------------------------------------
                """if key in connections['Mi9_Mi9'][0] and pID in connections['Mi9_Mi9'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi9_Mi1'][0] and pID in connections['Mi9_Mi1'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi9_Tm3'][0] and pID in connections['Mi9_Tm3'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)"""

                if key in connections['Mi9_Mi4'][0] and pID in connections['Mi9_Mi4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)

                if key in connections['Mi9_T4'][0] and pID in connections['Mi9_T4'][1]:
                    info = compressed_syn.synapse(sender,receiver,synloc,e=-80)

                    synlist.append(info)

    print('Synapses: ' + str(len(synlist)))

    #--------------------------------------------------------------------------------------------------------------------------------------------

    tlist = []
    Mi1simlist = []
    L1simlist = []
    Tm3simlist = []
    Mi4simlist = []
    Mi9simlist = []
    T4simlist = []

    T4asimlist = []
    T4bsimlist = []
    T4csimlist = []
    T4dsimlist = []

    Mi1data = []
    L1data = []
    Tm3data = []
    Mi4data = []
    Mi9data = []
    T4data = []

    T4adata = []
    T4bdata = []
    T4cdata = []
    T4ddata = []

    heatmap = []

    #------------------------------------------------------------------------------------------------------------

    for val in neurdic.values():

        heat_vec = h.Vector()
        t_vec = h.Vector()

        heat_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
        heatmap.append(heat_vec)
        t_vec.record(h._ref_t)

        if val.cellID in Mi1list:

            Mi1soma_v_vec = h.Vector()
            Mi1t_vec = h.Vector()

            Mi1soma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            Mi1t_vec.record(h._ref_t)

            Mi1sim = (Mi1t_vec,Mi1soma_v_vec)
            Mi1simlist.append(Mi1sim)

            Mi1data.append(Mi1soma_v_vec)

        if val.cellID in L1list:

            L1soma_v_vec = h.Vector()
            L1t_vec = h.Vector()

            L1soma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            L1t_vec.record(h._ref_t)

            L1sim = (L1t_vec,L1soma_v_vec)
            L1simlist.append(L1sim)

            L1data.append(L1soma_v_vec)

        if val.cellID in Tm3list:

            Tm3soma_v_vec = h.Vector()
            Tm3t_vec = h.Vector()

            Tm3soma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            Tm3t_vec.record(h._ref_t)

            Tm3sim = (Tm3t_vec,Tm3soma_v_vec)
            Tm3simlist.append(Tm3sim)

            Tm3data.append(Tm3soma_v_vec)

        if val.cellID in Mi4list:

            Mi4soma_v_vec = h.Vector()
            Mi4t_vec = h.Vector()

            Mi4soma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            Mi4t_vec.record(h._ref_t)

            Mi4sim = (Mi4t_vec,Mi4soma_v_vec)
            Mi4simlist.append(Mi4sim)

            Mi4data.append(Mi4soma_v_vec)

        if val.cellID in Mi4list:

            Mi9soma_v_vec = h.Vector()
            Mi9t_vec = h.Vector()

            Mi9soma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            Mi9t_vec.record(h._ref_t)

            Mi9sim = (Mi9t_vec,Mi9soma_v_vec)
            Mi9simlist.append(Mi9sim)

            Mi9data.append(Mi9soma_v_vec)

        if val.cellID in T4list:

            T4soma_v_vec = h.Vector()
            T4t_vec = h.Vector()

            T4soma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            T4t_vec.record(h._ref_t)

            T4sim = (T4t_vec,T4soma_v_vec)
            T4simlist.append(T4sim)

            T4data.append(T4soma_v_vec)

        if val.cellID in T4alist:

            T4asoma_v_vec = h.Vector()
            T4at_vec = h.Vector()

            T4asoma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            T4at_vec.record(h._ref_t)

            T4asim = (T4at_vec,T4asoma_v_vec)
            T4asimlist.append(T4asim)

            T4adata.append(T4asoma_v_vec)

        if val.cellID in T4blist:

            T4bsoma_v_vec = h.Vector()
            T4bt_vec = h.Vector()

            T4bsoma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            T4bt_vec.record(h._ref_t)

            T4bsim = (T4bt_vec,T4bsoma_v_vec)
            T4bsimlist.append(T4bsim)

            T4bdata.append(T4bsoma_v_vec)

        if val.cellID in T4clist:

            T4csoma_v_vec = h.Vector()
            T4ct_vec = h.Vector()

            T4csoma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            T4ct_vec.record(h._ref_t)

            T4csim = (T4ct_vec,T4csoma_v_vec)
            T4csimlist.append(T4csim)

            T4cdata.append(T4csoma_v_vec)

        if val.cellID in T4dlist:

            T4dsoma_v_vec = h.Vector()
            T4dt_vec = h.Vector()

            T4dsoma_v_vec.record(val.compartmentdict[val.compartmentdict.keys()[0]][1](0.5)._ref_v)
            T4dt_vec.record(h._ref_t)

            T4dsim = (T4dt_vec,T4dsoma_v_vec)
            T4dsimlist.append(T4dsim)

            T4ddata.append(T4dsoma_v_vec)

    #--------------------------------------------------------------------------------------------------------------------------------------------

    Mi1data = numpy.array(Mi1data, dtype=list)

    print('Starting simulation...')

    h.tstop = 1000

    print('Running simulation...')

    import time
    start_time = time.time()

    h.run()

    print("--- %s seconds ---" % (time.time() - start_time))

    print('Done!')

    #--------------------------------------------------------------------------------------------------------------------------------------------

    pyplot.figure(str(stimdir))
    pyplot.subplot(2,3,1)
    for token in Mi1simlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('Mi1')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,3,2)
    for token in L1simlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('L1')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,3,3)
    for token in Tm3simlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('Tm3')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,3,4)
    for token in Mi4simlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('Mi4')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,3,5)
    for token in Mi9simlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('Mi9')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,3,6)
    for token in T4simlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('T4')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    #--------------------------------------------------------------------------------------------------------------------------------------------

    pyplot.figure('T4: '+ str(stimdir))

    pyplot.subplot(2,2,1)
    for token in T4asimlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('T4a')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,2,2)
    for token in T4bsimlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('T4b')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,2,3)
    for token in T4csimlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('T4c')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    pyplot.subplot(2,2,4)
    for token in T4dsimlist:
        pyplot.plot(token[0],token[1])

    pyplot.title('T4d')
    pyplot.xlabel('time (ms)')
    pyplot.ylabel('mV')

    #--------------------------------------------------------------------------------------------------------------------------------------------

    pyplot.show()

    #--------------------------------------------------------------------------------------------------------------------------------------------

    import os

    datafolder = datadict['dataloc'] + 'compressed/' + str(stimdir)

    filename = datafolder + 'Mi1simlist' + '.csv'
    numpy.savetxt(filename,Mi1data,delimiter=',')

    filename = datafolder + 'L1simlist' + '.csv'
    numpy.savetxt(filename,L1data,delimiter=',')

    filename = datafolder + 'Tm3simlist' + '.csv'
    numpy.savetxt(filename,Tm3data,delimiter=',')

    filename = datafolder + 'Mi4simlist' + '.csv'
    numpy.savetxt(filename,Mi4data,delimiter=',')

    filename = datafolder + 'Mi9simlist' + '.csv'
    numpy.savetxt(filename,Mi9data,delimiter=',')

    filename = datafolder + 'T4simlist' + '.csv'
    numpy.savetxt(filename,T4data,delimiter=',')

    filename = datafolder + 'T4asimlist' + '.csv'
    numpy.savetxt(filename,T4adata,delimiter=',')

    filename = datafolder + 'T4bsimlist' + '.csv'
    numpy.savetxt(filename,T4bdata,delimiter=',')

    filename = datafolder + 'T4csimlist' + '.csv'
    numpy.savetxt(filename,T4cdata,delimiter=',')

    filename = datafolder + 'T4dsimlist' + '.csv'
    numpy.savetxt(filename,T4ddata,delimiter=',')

    h.quit()

if __name__ == '__main__':

    stimlist = ['rl','du','lr','ud','full']

    s0 = stimlist[int(argv[-1])]

    Compartment(s0)

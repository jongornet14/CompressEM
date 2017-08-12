from structneur import node_neur
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

def Node(stimdir):

    """This is the program for the node model in the paper _.
    When using this program use the following command:

        ./x86_64/special -python nodetest.py (number)

    Where the numbers are for the direction of the signal:

    (number)
    0: 'rl'
    1: 'du'
    2: 'lr'
    3: 'ud'
    4: 'full' (forward direction)

    The data will be saved in the ./data/node directory."""

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

    datafile = open(datadict['areas'],'r')
    area = simplejson.load(datafile)
    datafile.close()

    #--------------------------------------------------------------------------------------------------------------------------------------------

    neurdic = {}

    print('Creating cells...')

    count = 0

    #--------------------------------------------------------------------------------------------------------------------------------------------

    for f in range(len(fulldata)):

        if fulldata[f] == None:

            continue

        else:

            #--------------------------------------------------------------------------------------------------------------------------------------------

            if str(fulldata[f].cellID) in area.keys():

                neurdic[fulldata[f].cellID] = node_neur.cell(fulldata[f],area[str(fulldata[f].cellID)])

                print(area[str(fulldata[f].cellID)])

                count += 1

    #-------------------------------------------------------------------------------

    print('Compartments: ' + str(count))

    #-------------------------------------------------------------------------------

    print('Connecting cells..')

    #-------------------------------------------------------------------------------

    from structneur import node_syn

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

    synlist = []

    for key in neurdic.keys():

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

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        for p in neurdic[key].partners:

            part = p[0]

            if part in neurdic.keys():

                #L1-----------------------------------------------------------------------------------------------
                """if key in connections['L1_L1'][0] and part in connections['L1_L1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],tau=50)

                    synlist.append(info)"""

                if key in connections['L1_Mi1'][0] and part in connections['L1_Mi1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['L1_Tm3'][0] and part in connections['L1_Tm3'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                #Mi1-----------------------------------------------------------------------------------------------
                """if key in connections['Mi1_Mi1'][0] and part in connections['Mi1_Mi1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                """if key in connections['Mi1_L1'][0] and part in connections['Mi1_L1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                if key in connections['Mi1_Tm3'][0] and part in connections['Mi1_Tm3'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Mi1_Mi4'][0] and part in connections['Mi1_Mi4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Mi1_Mi9'][0] and part in connections['Mi1_Mi9'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Mi1_T4'][0] and part in connections['Mi1_T4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                #Tm3-----------------------------------------------------------------------------------------------
                """if key in connections['Tm3_Tm3'][0] and part in connections['Tm3_Tm3'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                """if key in connections['Tm3_L1'][0] and part in connections['Tm3_L1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                if key in connections['Tm3_Mi1'][0] and part in connections['Tm3_Mi1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Tm3_Mi4'][0] and part in connections['Tm3_Mi4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Tm3_Mi9'][0] and part in connections['Tm3_Mi9'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Tm3_T4'][0] and part in connections['Tm3_T4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                #Mi4-----------------------------------------------------------------------------------------------
                """if key in connections['Mi4_Mi4'][0] and part in connections['Mi4_Mi4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi4_Mi1'][0] and part in connections['Mi4_Mi1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi4_Tm3'][0] and part in connections['Mi4_Tm3'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                if key in connections['Mi4_Mi9'][0] and part in connections['Mi4_Mi9'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi4_T4'][0] and part in connections['Mi4_T4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                #Mi9-----------------------------------------------------------------------------------------------
                """if key in connections['Mi9_Mi9'][0] and part in connections['Mi9_Mi9'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi9_Mi1'][0] and part in connections['Mi9_Mi1'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                """if key in connections['Mi9_Tm3'][0] and part in connections['Mi9_Tm3'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                if key in connections['Mi9_Mi4'][0] and part in connections['Mi9_Mi4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi9_T4'][0] and part in connections['Mi9_T4'][1]:
                    info = node_syn.synapse(neurdic[key],neurdic[part],e=-80)

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

        v_vec = h.Vector()
        t_vec = h.Vector()

        v_vec.record(val.soma(0.5)._ref_v)
        t_vec.record(h._ref_t)

        sim = (t_vec,v_vec)
        ID_sim = numpy.array([val.cellID,v_vec],dtype=list)

        if val.cellID in Mi1list:

            Mi1simlist.append(sim)
            Mi1data.append(v_vec)

        if val.cellID in L1list:

            L1simlist.append(sim)
            L1data.append(v_vec)

        if val.cellID in Tm3list:

            Tm3simlist.append(sim)
            Tm3data.append(v_vec)

        if val.cellID in Mi4list:

            Mi4simlist.append(sim)
            Mi4data.append(v_vec)

        if val.cellID in Mi4list:

            Mi9simlist.append(sim)
            Mi9data.append(v_vec)

        if val.cellID in T4list:

            T4simlist.append(sim)
            T4data.append(v_vec)

        if val.cellID in T4alist:

            T4asimlist.append(sim)
            T4adata.append(v_vec)

        if val.cellID in T4blist:

            T4bsimlist.append(sim)
            T4bdata.append(v_vec)

        if val.cellID in T4clist:

            T4csimlist.append(sim)
            T4cdata.append(v_vec)

        if val.cellID in T4dlist:

            T4dsimlist.append(sim)
            T4ddata.append(v_vec)

    #--------------------------------------------------------------------------------------------------------------------------------------------

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
    datafolder = datadict['dataloc'] + 'node/' + str(stimdir)

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

    Node(s0)

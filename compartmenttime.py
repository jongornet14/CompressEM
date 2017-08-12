from structneur import neur,syndend
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

    """This is the program for the efficiency of the compartment model in the paper _.
    When using this program use the following command:

        ./x86_64/special -python compartmenttime.py (number)

    Where the numbers are for the direction of the signal:

    (number)
    0: 'rl'
    1: 'du'
    2: 'lr'
    3: 'ud'
    4: 'full' (forward direction)

    The data will be saved in the ./data/times/compartment directory."""

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

    neurdic = {}

    print('Creating cells...')

    cellids = []

    area = {}

    for f in range(len(fulldata)):

        if fulldata[f] == None:

            continue

        else:

            neurdic[fulldata[f].cellID] = neur.cell(fulldata[f])
            area[fulldata[f].cellID] = neurdic[fulldata[f].cellID].totalarea

    datadict['areas'] = datadict['dataloc'] + 'areas.json'

    datafile = open(datadict['areas'],'w')
    simplejson.dump(area,datafile)
    datafile.close()

    fileloc = open('locationdic.json', 'w')
    simplejson.dump(datadict,fileloc)
    fileloc.close()

    print('Connecting cells..')

    synlist = []

    count = 0

    looklist = []
    nclist = []

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

    for key in neurdic.keys():
        for part in neurdic[key].partners:
            if part in neurdic.keys():

                #L1-----------------------------------------------------------------------------------------------
                """if key in connections['L1_L1'][0] and part in connections['L1_L1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],tau=50)

                    synlist.append(info)"""

                if key in connections['L1_Mi1'][0] and part in connections['L1_Mi1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],tau=50)

                    synlist.append(info)

                if key in connections['L1_Tm3'][0] and part in connections['L1_Tm3'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],tau=50)

                    synlist.append(info)

                #Mi1-----------------------------------------------------------------------------------------------
                """if key in connections['Mi1_Mi1'][0] and part in connections['Mi1_Mi1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                """if key in connections['Mi1_L1'][0] and part in connections['Mi1_L1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                if key in connections['Mi1_Tm3'][0] and part in connections['Mi1_Tm3'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Mi1_Mi4'][0] and part in connections['Mi1_Mi4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Mi1_Mi9'][0] and part in connections['Mi1_Mi9'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Mi1_T4'][0] and part in connections['Mi1_T4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                #Tm3-----------------------------------------------------------------------------------------------
                """if key in connections['Tm3_Tm3'][0] and part in connections['Tm3_Tm3'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                """if key in connections['Tm3_L1'][0] and part in connections['Tm3_L1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)"""

                if key in connections['Tm3_Mi1'][0] and part in connections['Tm3_Mi1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Tm3_Mi4'][0] and part in connections['Tm3_Mi4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Tm3_Mi9'][0] and part in connections['Tm3_Mi9'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                if key in connections['Tm3_T4'][0] and part in connections['Tm3_T4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part])

                    synlist.append(info)

                #Mi4-----------------------------------------------------------------------------------------------
                """if key in connections['Mi4_Mi4'][0] and part in connections['Mi4_Mi4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                if key in connections['Mi4_Mi1'][0] and part in connections['Mi4_Mi1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi4_Tm3'][0] and part in connections['Mi4_Tm3'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi4_Mi9'][0] and part in connections['Mi4_Mi9'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi4_T4'][0] and part in connections['Mi4_T4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                #Mi9-----------------------------------------------------------------------------------------------
                """if key in connections['Mi9_Mi9'][0] and part in connections['Mi9_Mi9'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)"""

                if key in connections['Mi9_Mi1'][0] and part in connections['Mi9_Mi1'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi9_Tm3'][0] and part in connections['Mi9_Tm3'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi9_Mi4'][0] and part in connections['Mi9_Mi4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

                if key in connections['Mi9_T4'][0] and part in connections['Mi9_T4'][1]:
                    info = syndend.synapse(neurdic[key],neurdic[part],e=-80)

                    synlist.append(info)

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

    print('Connecting stimulus..')

    print('Running Trials...')

    import time

    for t_space in range(100,1100,100):
        timing = []
        for _ in range(100):

            h.tstop = t_space

            start_time = time.time()

            h.run()

            timing.append(time.time() - start_time)

        timing = numpy.array(timing)
        numpy.savetxt('/groups/scheffer/home/gornetj/Documents/em_neuron/data/times/compartment/' + str(t_space) + '_' + str(stimdir) + '_data.csv',timing,delimiter=',')

    print('Done!')

    h.quit()

if __name__ == '__main__':

    stimlist = ['rl','du','lr','ud','full']

    s0 = stimlist[int(argv[-1])]

    Compartment(s0)

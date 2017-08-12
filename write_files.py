import simplejson
import pickle
import os

datafile = open("/groups/scheffer/home/gornetj/Documents/em_neuron/data/simdata/datafile.p",'r')
fulldata = pickle.load(datafile)
datafile.close()

string = ''

for f in range(len(fulldata)):

    if fulldata[f] == None:

        continue

    else:


        url = 'curl -X GET http://emdata2.int.janelia.org:7000/api/node/3b548cfb0faa4339bb09f2201bd68fd9/bodies1104_skeletons/key/' + str(fulldata[f].cellID) + '_swc  > ' + str(fulldata[f].cellID) + '.swc'

        string += url + '\n'

open_file = open('swcdata.sh','w')
open_file.write(string)
open_file.close()

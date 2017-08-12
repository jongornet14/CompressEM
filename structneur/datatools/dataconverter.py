from structneur.datatools import neurlist, parallelcomput
import re
import simplejson
import pickle
from multiprocessing import Pool

def changedata(synname,bodyname,keyname,totaldata):

    pool = Pool(processes=8)

    open_file = open(keyname, 'r')
    keys = simplejson.load(open_file)
    open_file.close()

    cellIDs = []

    neuid = neurlist.ids(synname)

    searchlist = []
    for ni in neuid:

        if ni in keys:
            searchlist.append(ni)

    searchlist = list(set(searchlist))

    fulldata = pool.map(parallelcomput.parneur, searchlist)

    fulldata.remove(None)

    with open(totaldata, 'w') as datafile:
        pickle.dump(fulldata,datafile,pickle.HIGHEST_PROTOCOL)

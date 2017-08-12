from structneur.datatools import cellinfo, neurlist
import simplejson

def parneur(cellID):
    #Function:  parneur
    #Input:     neuron ID
    #Process:   create neuron objects
    #Output:    neuron objects

    fileloc = open('locationdic.json', 'r')
    datadict = simplejson.load(fileloc)
    fileloc.close()

    synname     = datadict['synname']

    bodyname    = datadict['bodyname']

    coordname   = datadict['dataloc'] + str(cellID) + '.txt'

    try:

        fulldata = cellinfo.dataset(coordname,bodyname,synname,int(cellID))

        if len(fulldata.coordinates.shape) > 1:

            return fulldata

    except:

        return None

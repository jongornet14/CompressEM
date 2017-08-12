import numpy
import simplejson

class dataset(object):
    def __init__(self,coordname,bodyname,synname,cellID):
        self.coordinates = numpy.loadtxt(coordname,skiprows=1)
        self.cellID = cellID
        self.cellinfo(synname,cellID)

    def cellinfo(self,synname,ID):
        #Function:  cellinfo
        #Input:     self, synapse file name, neuron ID
        #Process:   create neuron objects
        #Output:    saves neuron object

        open_file = open(synname,'r')
        syndata = simplejson.load(open_file)['data']

        self.partners = []

        for i in range(len(syndata)):
            if syndata[i]['T-bar']['body ID'] == ID:
                self.location = syndata[i]['T-bar']['location']
                for j in range(len(syndata[i]['partners'])):
                    syninfo = [syndata[i]['partners'][j]['body ID'], numpy.array(syndata[i]['partners'][j]['location'])]
                    self.partners.append(syninfo)

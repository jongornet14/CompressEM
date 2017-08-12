from neuron import h
import numpy
from scipy.spatial import distance
from structneur.datatools import cellinfo
import collections
import math
import simplejson

class cell(object):
    def __init__(self,dataset):

        #create variables
        coordinates = dataset.coordinates
        celllocation = dataset.location

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.cellID = dataset.cellID

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.stimlist = []
        self.dendgraph = {}

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.coordinates = coordinates
        self.partners = dataset.partners
        self.celllocation = celllocation

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        #build cell
        self.graph()
        self.build_subsets()
        self.define_biophysics()

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def graph(self):
        #Function:  graph
        #Input:     self
        #Process:   create dendrite branch network
        #Output:    neuron

        self.dendsegs = numpy.array([self.coordinates[:,0], self.coordinates[:,2], self.coordinates[:,3],self.coordinates[:,4],self.coordinates[:,5],self.coordinates[:,6]])

        self.seglist = numpy.array(self.coordinates[:,0]-1,dtype=int)
        self.segmap = numpy.array(self.coordinates[:,6]-1,dtype=int)

        if self.seglist[0] == 1:
            self.seglist = numpy.array(self.seglist-1,dtype=int)
            self.segmap = numpy.array(self.segmap-1,dtype=int)

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.compartmentdict = {}
        segvals = []
        Gcompartment = []

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        for c in range(len(self.seglist)):

            #-----------------------------------------------------------------------------------------------------------------------------------------------

            if self.segmap[c] < self.seglist[c] - 1:

                if len(segvals) == 0:
                    continue

                i = c

                self.compartmentdict[i] = [Gcompartment,h.Section(name='compartment',cell=self),segvals]

                Gcompartment = []
                segvals = []

            #-----------------------------------------------------------------------------------------------------------------------------------------------

            if c == len(self.seglist) - 1:

                if len(segvals) == 0:
                    break

                i = c

                self.compartmentdict[i] = [Gcompartment,h.Section(name='compartment',cell=self),segvals]

                Gcompartment = []
                segvals = []

            #-----------------------------------------------------------------------------------------------------------------------------------------------

            else:

                segvals.append([self.dendsegs[1,c]*1/125.0,self.dendsegs[2,c]*1/125.0,self.dendsegs[3,c]*1/125.0,self.dendsegs[4,c]*1/125.0])
                Gcompartment.append(self.seglist[c])

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        for key in self.compartmentdict.keys():

            if len(self.compartmentdict[key][2]) > 0:

                s = self.compartmentdict[key][2][0]
                e = self.compartmentdict[key][2][-1]

                if distance.euclidean(s[0:2],e[0:2]) == 0:

                    h.pt3dadd(s[0],s[1],s[2],s[3],sec=self.compartmentdict[key][1])
                    h.pt3dadd(e[0] + 1e-5,e[1] + 1e-5,e[2] + 1e-5,e[3],sec=self.compartmentdict[key][1])

                else:

                    h.pt3dadd(s[0],s[1],s[2],s[3],sec=self.compartmentdict[key][1])
                    h.pt3dadd(e[0],e[1],e[2],e[3],sec=self.compartmentdict[key][1])

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        for key in self.compartmentdict.keys():

            for part in self.compartmentdict.keys():

                if key in self.compartmentdict[part][0]:

                    self.compartmentdict[key][1].connect(self.compartmentdict[part][1])

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        for dendID in self.compartmentdict.keys():

            n3dID = int(h.n3d(sec=self.compartmentdict[dendID][1]))

            for n in range(n3dID):

                self.dendgraph[dendID]  = numpy.array([float(h.x3d(n,sec=self.compartmentdict[dendID][1])),float(h.y3d(n,sec=self.compartmentdict[dendID][1])),float(h.z3d(n,sec=self.compartmentdict[dendID][1]))])

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def build_subsets(self):
        #Build all
        self.all = h.SectionList()
        self.all.wholetree(sec=self.compartmentdict[self.compartmentdict.keys()[0]][1])

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def define_biophysics(self):
        #Function:  define_biophysics
        #Input:     self
        #Process:   set parameters
        #Output:    neurons with biophysics

        self.totalarea = 0

        for sec in self.all:   # 'all' exists in parent object.

            sec.Ra = 1e-5         # Axial resistance in Ohm * cm
            sec.cm = 1         # Membrane capacitance in micro Farads / cm^2

            for seg in sec:

                self.totalarea += h.area(seg.x)

        # Dendrite passive
        for d in self.compartmentdict.values():
            d[1].insert('leak')
            d[1].g_leak = 1e-5

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def create_stim(self,time):
        #Function:  create_stim
        #Input:     self
        #Process:   create stimulus
        #Output:    neurons with stimulus at time (ms)

        istim = h.IClamp(self.compartmentdict[self.compartmentdict.keys()[0]][1](0.5))
        istim.amp = 0.002
        istim.dur = 10
        istim.delay = time
        self.stimlist.append(istim)

        istim = h.IClamp(self.compartmentdict[self.compartmentdict.keys()[0]][1](0.5))
        istim.amp = 0.0002
        istim.dur = 200
        istim.delay = time+15
        self.stimlist.append(istim)

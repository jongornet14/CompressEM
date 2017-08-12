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
        self.cellID = dataset.cellID
        self.synlist = []
        self.branchd = []

        self.stimlist = []
        self.dendlist = []
        self.dendgraph = {}
        self.synapse = {}
        self.denddict = {}

        self.coordinates = coordinates
        self.partners = dataset.partners
        self.celllocation = celllocation

        #build cell
        self.graph()
        self.build_subsets()
        self.define_biophysics()

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

        #Geometry of cell
        self.dendlist = []

        prior_coord = [self.dendsegs[1,0]*1/125.0,self.dendsegs[2,0]*1/125.0,self.dendsegs[3,0]*1/125.0,self.dendsegs[4,0]*1/125.0]

        for P in range(len(self.seglist)):

            self.dendlist.append(h.Section(name='compartment',cell=self))

        prior_coord = [self.dendsegs[1,0]*1/125.0,self.dendsegs[2,0]*1/125.0,self.dendsegs[3,0]*1/125.0,self.dendsegs[4,0]*1/125.0]

        for c in range(len(self.dendlist)):

            self.dendlist[self.seglist[c]].diam = self.dendsegs[4,c]

            if distance.euclidean([self.dendsegs[1,c]*1/125.0,self.dendsegs[2,c]*1/125.0,self.dendsegs[3,c]*1/125.0],[prior_coord[0],prior_coord[1],prior_coord[2]]) == 0:

                h.pt3dadd(self.dendsegs[1,c]*1/125.0,self.dendsegs[2,c]*1/125.0,self.dendsegs[3,c]*1/125.0,self.dendsegs[4,c]*1/125.0,sec=self.dendlist[self.seglist[c]])
                h.pt3dadd(self.dendsegs[1,c]*1/125.0 + 1e-9,self.dendsegs[2,c]*1/125.0+1e-9,self.dendsegs[3,c]*1/125.0+1e-9,self.dendsegs[4,c]*1/125.0,sec=self.dendlist[self.seglist[c]])

            else:

                h.pt3dadd(prior_coord[0],prior_coord[1],prior_coord[2],prior_coord[3],sec=self.dendlist[self.seglist[c]])
                h.pt3dadd(self.dendsegs[1,c]*1/125.0,self.dendsegs[2,c]*1/125.0,self.dendsegs[3,c]*1/125.0,self.dendsegs[4,c]*1/125.0,sec=self.dendlist[self.seglist[c]])

            prior_coord = [self.dendsegs[1,c]*1/125.0,self.dendsegs[2,c]*1/125.0,self.dendsegs[3,c]*1/125.0,self.dendsegs[4,c]*1/125.0]

            if int(self.dendsegs[5,c]) < 0:
                continue
            else:
                self.dendlist[self.seglist[c]].connect(self.dendlist[self.segmap[c]])

        for dendID in range(len(self.dendlist)):

            n3dID = int(h.n3d(sec=self.dendlist[dendID]))

            graphcoord = []

            for n in range(n3dID):

                self.dendgraph[dendID]  = numpy.array([float(h.x3d(n,sec=self.dendlist[dendID])),float(h.y3d(n,sec=self.dendlist[dendID])),float(h.z3d(n,sec=self.dendlist[dendID]))])

    def build_subsets(self):
        #Build all
        self.all = h.SectionList()
        self.all.wholetree(sec=self.dendlist[0])

    def define_biophysics(self):
        #Function:  define_biophysics
        #Input:     self
        #Process:   set parameters
        #Output:    neurons with biophysics

        self.totalarea = 0

        for sec in self.all:   # 'all' exists in parent object.
            sec.Ra = 1e-5     # Axial resistance in Ohm * cm
            sec.cm = 1         # Membrane capacitance in micro Farads / cm^2

            for seg in sec:

                self.totalarea += h.area(seg.x)

        # Dendrite passive
        for d in self.dendlist:
            d.insert('leak')

    def create_stim(self,time):
        #Function:  create_stim
        #Input:     self
        #Process:   create stimulus
        #Output:    neurons with stimulus at time (ms)

        istim = h.IClamp(self.dendlist[0](0.5))
        istim.amp = 0.002
        istim.dur = 10
        istim.delay = time
        self.stimlist.append(istim)

        istim = h.IClamp(self.dendlist[0](0.5))
        istim.amp = 0.0002
        istim.dur = 200
        istim.delay = time+15
        self.stimlist.append(istim)

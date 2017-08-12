from neuron import h
import numpy
from scipy.spatial import distance
from structneur.datatools import cellinfo

class cell(object):
    def __init__(self):

        #create variables
        self.stimlist = []
        self.dendlist = []
        self.dendgraph = {}

        #build cell
        self.graph()
        self.build_subsets()
        self.define_biophysics()

    def graph(self):
        #Function:  graph
        #Input:     self
        #Process:   create dendrite branch network
        #Output:    neuron
        
        self.soma = h.Section(name='soma',cell=self)
        self.dend = h.Section(name='dend',cell=self)
        self.dend.connect(self.soma(1))

        self.dend.diam = 2
        self.dend.nseg = 10

        self.soma.L = self.soma.diam = 5.0 # microns

        h.pt3dclear(sec=self.soma)

        h.pt3dadd(0,0,0,self.soma.diam,sec=self.soma)
        h.pt3dadd(0 + self.soma.L,0 + self.soma.L,0 + self.soma.L,self.soma.diam,sec=self.soma)

        h.pt3dadd(0 + self.soma.L,0 + self.soma.L,0 + self.soma.L,self.soma.diam,sec=self.soma)
        h.pt3dadd(0 + self.soma.L + 10,0 + self.soma.L + 10,0 + self.soma.L + 10,self.soma.diam,sec=self.soma)

    def build_subsets(self):
        #Build all
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

    def define_biophysics(self):
        #Function:  define_biophysics
        #Input:     self
        #Process:   set parameters
        #Output:    neurons with biophysics

        self.totalarea = 0

        for sec in self.all:    # 'all' exists in parent object.
            sec.Ra = 1          # Axial resistance in Ohm * cm
            sec.cm = 1         # Membrane capacitance in micro Farads / cm^2

            for seg in sec:

                self.totalarea += h.area(seg.x)

        # Soma passive
        self.soma.insert('leak')
        self.soma.g_leak = 0.00001

        # Dendrite passive
        self.dend.insert('leak')
        self.dend.g_leak = 0.00001

    def create_stim(self,time):
        #Function:  create_stim
        #Input:     self
        #Process:   create stimulus
        #Output:    neurons with stimulus at time (ms)

        istim = h.IClamp(self.soma(0.5))
        istim.amp = 0.002
        istim.dur = 500
        istim.delay = time+15
        self.stimlist.append(istim)

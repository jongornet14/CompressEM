from neuron import h
import numpy
from scipy.spatial import distance
from structneur.datatools import cellinfo

class cell(object):
    def __init__(self,areaval):

        #create variables
        self.stimlist = []
        self.dendlist = []
        self.dendgraph = {}

        #build cell
        self.nodegraph(areaval)
        self.build_subsets()
        self.define_biophysics()

    def nodegraph(self,areaval):
        #Function:  nodegraph
        #Input:     self
        #Process:   create neurons
        #Output:    neuron
        
        self.soma = h.Section(name='soma',cell=self)

        self.soma.L = self.soma.diam = 5.0 # microns

        self.Captot     = self.cap(areaval)
        self.condtot    = self.cond(areaval)

        self.soma = h.Section(name='soma',cell=self)
        self.soma.L = self.soma.diam = 5.0 # microns

    def cap(self,S,cap_prior=0.1):
        #Function:  cap
        #Input:     self, surface area S
        #Process:   adjust capacitance
        #Output:    capacitance

        C = (S * cap_prior) / 78.5398163397
        return C

    def cond(self,S,cond_prior=0.00001):
        #Function:  cond
        #Input:     self, surface area S
        #Process:   adjust conductance
        #Output:    conductance

        g = (S * cond_prior) / 78.5398163397
        return g

    def build_subsets(self):
        #Build all
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

    def define_biophysics(self):
        #Function:  define_biophysics
        #Input:     self
        #Process:   set parameters
        #Output:    neurons with biophysics

        for sec in self.all:            # 'all' exists in parent object.

            sec.Ra = 1      # Axial resistance in Ohm * cm
            sec.cm = self.Captot       # Membrane capacitance in micro Farads / cm^2

        # Soma passive
        self.soma.insert('leak')
        self.soma.g_leak = self.condtot

    def create_stim(self,time):
        #Function:  create_stim
        #Input:     self
        #Process:   create stimulus
        #Output:    neurons with stimulus at time (ms)

        istim = h.IClamp(self.soma(0.5))
        istim.amp = 0.02
        istim.dur = 10
        istim.delay = time
        self.stimlist.append(istim)

        istim = h.IClamp(self.soma(0.5))
        istim.amp = 0.002
        istim.dur = 200
        istim.delay = time+15
        self.stimlist.append(istim)

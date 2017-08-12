from neuron import h
import numpy
from scipy.spatial import distance
from structneur.datatools import cellinfo

class cell(object):
    def __init__(self,dataset,areaval):

        #create variables
        coordinates = dataset.coordinates
        celllocation = dataset.location

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.cellID = dataset.cellID
        self.area   = areaval

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.stimlist = []
        self.dendlist = []

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        self.coordinates = coordinates
        self.partners = dataset.partners
        self.celllocation = celllocation

        #-----------------------------------------------------------------------------------------------------------------------------------------------

        #build cell
        self.nodegraph(areaval)
        self.build_subsets()
        self.define_biophysics()

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def nodegraph(self,areaval):
        #Function:  nodegraph
        #Input:     self
        #Process:   create neurons
        #Output:    neuron

        self.Captot     = self.cap(areaval)
        self.condtot    = self.cond(areaval)

        self.soma   = h.Section(name='soma',cell=self)
        self.soma.L = self.soma.diam = 5.0 # microns

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def cap(self,S,cap_prior=1):
        #Function:  cap
        #Input:     self, surface area S
        #Process:   adjust capacitance
        #Output:    capacitance

        C = (S * cap_prior) / 78.5398163397
        return C

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def cond(self,S,cond_prior=1e-5):
        #Function:  cond
        #Input:     self, surface area S
        #Process:   adjust conductance
        #Output:    conductance

        g = (S * cond_prior) / 78.5398163397
        return g

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def build_subsets(self):
        #Build all
        self.all = h.SectionList()
        self.all.wholetree(sec=self.soma)

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def define_biophysics(self):
        #Function:  define_biophysics
        #Input:     self
        #Process:   set parameters
        #Output:    neurons with biophysics

        self.totalarea = 0

        for sec in self.all:           # 'all' exists in parent object.

            sec.Ra = 1e-5                 # Axial resistance in Ohm * cm
            sec.cm = self.Captot       # Membrane capacitance in micro Farads / cm^2

            for seg in sec:

                self.totalarea += h.area(seg.x)

        # Soma passive
        self.soma.insert('leak')
        self.soma.g_leak = self.condtot

    #-----------------------------------------------------------------------------------------------------------------------------------------------

    def create_stim(self,time):
        #Function:  create_stim
        #Input:     self
        #Process:   create stimulus
        #Output:    neurons with stimulus at time (ms)

        istim = h.IClamp(self.soma(0.5))
        istim.amp = 2e-3
        istim.dur = 10
        istim.delay = time
        self.stimlist.append(istim)

        istim = h.IClamp(self.soma(0.5))
        istim.amp = 2e-4
        istim.dur = 200
        istim.delay = time+15
        self.stimlist.append(istim)

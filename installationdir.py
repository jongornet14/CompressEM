from structneur.datatools import dataconverter
from matplotlib import pyplot
import re
import simplejson
import pickle
from multiprocessing import Pool
import os

"""Program converts data to objects"""

programloc  = os.path.dirname(os.path.realpath(__file__))

synname     = 'annotations-synapse.json'

bodyname    = 'annotations-body.json'

datadict = {}

datadict['synname']     = str(programloc) + '/data/' + str(synname)
datadict['bodyname']    = str(programloc) + '/data/' + str(bodyname)
datadict['totaldata']   = str(programloc) + '/data/simdata/' + 'datafile.p'
datadict['programloc']  = str(programloc)
datadict['dataloc']     = str(programloc) + '/data/'

fileloc = open('locationdic.json', 'w')
simplejson.dump(datadict, fileloc)
fileloc.close()

fileloc = open('structneur/datatools/locationdic.json', 'w')
simplejson.dump(datadict, fileloc)
fileloc.close()

#dataconverter.changedata(synname,bodyname,keyname,totaldata)

from structneur.datatools import dataconverter
from matplotlib import pyplot
import re
import simplejson
import pickle
from multiprocessing import Pool

"""Program converts data to objects"""

fileloc = open('locationdic.json', 'r')
datadict = simplejson.load(fileloc)
fileloc.close()

synname     = datadict['synname']
bodyname    = datadict['bodyname']
keyname     = datadict['keys']
totaldata   = datadict['totaldata']

dataconverter.changedata(synname,bodyname,keyname,totaldata)

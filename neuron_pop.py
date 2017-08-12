import pickle
import simplejson
fileloc = open('locationdic.json', 'r')
datadict = simplejson.load(fileloc)
fileloc.close()

#--------------------------------------------------------------------------------------------------------------------------------------------

datafile = open(datadict['L1data'],'r')
L1list = pickle.load(datafile)
datafile.close()

datafile = open(datadict['Mi1data'],'r')
Mi1list = pickle.load(datafile)
datafile.close()

datafile = open(datadict['Tm3data'],'r')
Tm3list = pickle.load(datafile)
datafile.close()

datafile = open(datadict['Mi4data'],'r')
Mi4list = pickle.load(datafile)
datafile.close()

datafile = open(datadict['Mi9data'],'r')
Mi9list = pickle.load(datafile)
datafile.close()

datafile = open(datadict['T4data'],'r')
T4list = pickle.load(datafile)
datafile.close()

datafile = open(datadict['T4adata'],'r')
T4alist = pickle.load(datafile)
datafile.close()

datafile = open(datadict['T4bdata'],'r')
T4blist = pickle.load(datafile)
datafile.close()

datafile = open(datadict['T4cdata'],'r')
T4clist = pickle.load(datafile)
datafile.close()

datafile = open(datadict['T4ddata'],'r')
T4dlist = pickle.load(datafile)
datafile.close()

datafile = open(datadict['totaldata'],'r')
fulldata = pickle.load(datafile)
datafile.close()

print('L1', L1list)
#print('Mi1', 4096 in Mi1list)
#print('Tm3', 4096 in Tm3list)
#print('Mi4', 4096 in Mi4list)
#print('Mi9', 4096 in Mi9list)
#print('T4', 4096 in T4list)

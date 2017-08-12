import simplejson
import pickle
import numpy

"""This program converts the given SWC files in the /data folder to the network needed for
simulation."""

fileloc = open('locationdic.json', 'r')
datadict = simplejson.load(fileloc)
fileloc.close()

datafile = open(str(datadict['bodyname']),'r')
bodydata = simplejson.load(datafile)
datafile.close()

str1 = 'Mi1'
str2 = 'Tm3'
str3 = 'Mi4'
str4 = 'Mi9'
str5 = 'T4'
str6 = 'L1'

IDlist = ['Mi1','Tm3','Mi4','Mi9','T4','L1']

T4str1 = 'T4a'
T4str2 = 'T4b'
T4str3 = 'T4c'
T4str4 = 'T4d'

saveneuron = []
saveID = []
stimlist1 = []
stimlist2 = []
stimlist3 = []
stimlist4 = []
stimlist5 = []

stim1 = ['O','P','Q',None,None]
stim2 = ['N','E','F','R',None]
stim3 = ['M','D','T','A','G']
stim4 = ['L','C','B','H',None]
stim5 = ['K','J','I',None,None]

fullstim = [stim1,stim2,stim3,stim4,stim5]

fullstim = numpy.array(fullstim)

stimname = ['rl','du','lr','ud']

fullstimlist = []

Mi1list = []
Tm3list = []
L1list = []
Mi4list = []
Mi9list = []
T4list = []

T4alist = []
T4blist = []
T4clist = []
T4dlist = []

for j in range(4):

    stimlist1 = []
    stimlist2 = []
    stimlist3 = []
    stimlist4 = []
    stimlist5 = []

    for i in bodydata['data']:

        if 'name' in i.keys():

            if str(i['name'])[:2] in IDlist:
                saveID.append(i['body ID'])
            if str(i['name'])[:3] in IDlist:
                saveID.append(i['body ID'])

            if str(i['name'])[:3] == 'Mi1':
                Mi1list.append(i['body ID'])
            if str(i['name'])[:3] == 'Tm3':
                Tm3list.append(i['body ID'])
            if str(i['name'][:3]) == 'Mi4':
                Mi4list.append(i['body ID'])
            if str(i['name'][:3]) == 'Mi9':
                Mi9list.append(i['body ID'])
            if str(i['name'][:2]) == 'T4':
                T4list.append(i['body ID'])

            if str(i['name'][:2]) == 'L1':
                L1list.append(i['body ID'])
                if str(i['name'][3]) in fullstim[0,:]:
                    stimlist1.append(i['body ID'])
                if str(i['name'][3]) in fullstim[1,:]:
                    stimlist2.append(i['body ID'])
                if str(i['name'][3]) in fullstim[2,:]:
                    stimlist3.append(i['body ID'])
                if str(i['name'][3]) in fullstim[3,:]:
                    stimlist4.append(i['body ID'])
                if str(i['name'][3]) in fullstim[4,:]:
                    stimlist5.append(i['body ID'])

            if str(i['name'])[:3] == 'T4a':
                T4alist.append(i['body ID'])

            if str(i['name'])[:3] == 'T4b':
                T4blist.append(i['body ID'])

            if str(i['name'])[:3] == 'T4c':
                T4clist.append(i['body ID'])

            if str(i['name'])[:3] == 'T4d':
                T4dlist.append(i['body ID'])

    savestim = [stimlist1,stimlist2,stimlist3,stimlist4,stimlist5]

    fullstim = numpy.rot90(fullstim)

    datadict[str(stimname[j])] = datadict['dataloc'] + str(stimname[j]) + '.p'

    datafile = open(datadict[str(stimname[j])],'w')
    pickle.dump(savestim,datafile)
    datafile.close()

stimfull = []

for s0 in range(len(savestim)):
    for s1 in range(len(savestim[s0])):
        stimfull.append(savestim[s0][s1])

datadict['full'] = datadict['dataloc'] + 'full' + '.p'

datafile = open(datadict['full'],'w')
pickle.dump(stimfull,datafile)
datafile.close()

saveID      = list(set(saveID))

L1list      = list(set(L1list))
Mi1list     = list(set(Mi1list))
Tm3list     = list(set(Tm3list))
Mi4list     = list(set(Mi4list))
Mi9list     = list(set(Mi9list))
T4list      = list(set(T4list))

T4alist = list(set(T4alist))
T4blist = list(set(T4blist))
T4clist = list(set(T4clist))
T4dlist = list(set(T4dlist))

datadict['L1data']      = datadict['dataloc'] + 'L1data.p'
datadict['Mi1data']     = datadict['dataloc'] + 'Mi1data.p'
datadict['Tm3data']     = datadict['dataloc'] + 'Tm3data.p'
datadict['Mi4data']     = datadict['dataloc'] + 'Mi4data.p'
datadict['Mi9data']     = datadict['dataloc'] + 'Mi9data.p'
datadict['T4data']      = datadict['dataloc'] + 'T4data.p'

datadict['T4adata']     = datadict['dataloc'] + 'T4adata.p'
datadict['T4bdata']     = datadict['dataloc'] + 'T4bdata.p'
datadict['T4cdata']     = datadict['dataloc'] + 'T4cdata.p'
datadict['T4ddata']     = datadict['dataloc'] + 'T4ddata.p'

datadict['keys']        = datadict['dataloc'] + 'keys.json'
datadict['simdata']     = datadict['dataloc'] + 'simdata.p'

datafile = open(datadict['L1data'],'w')
pickle.dump(L1list,datafile)
datafile.close()

datafile = open(datadict['Mi1data'],'w')
pickle.dump(Mi1list,datafile)
datafile.close()

datafile = open(datadict['Tm3data'],'w')
pickle.dump(Tm3list,datafile)
datafile.close()

datafile = open(datadict['Mi4data'],'w')
pickle.dump(Mi4list,datafile)
datafile.close()

datafile = open(datadict['Mi9data'],'w')
pickle.dump(Mi9list,datafile)
datafile.close()

datafile = open(datadict['T4data'],'w')
pickle.dump(T4list,datafile)
datafile.close()

datafile = open(datadict['T4adata'],'w')
pickle.dump(T4alist,datafile)
datafile.close()

datafile = open(datadict['T4bdata'],'w')
pickle.dump(T4blist,datafile)
datafile.close()

datafile = open(datadict['T4cdata'],'w')
pickle.dump(T4clist,datafile)
datafile.close()

datafile = open(datadict['T4ddata'],'w')
pickle.dump(T4dlist,datafile)
datafile.close()

datafile = open(datadict['keys'],'w')
simplejson.dump(saveID,datafile)
datafile.close()

fileloc = open('locationdic.json', 'w')
datadict = simplejson.dump(datadict,fileloc)
fileloc.close()

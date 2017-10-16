# CompressEM

## Introduction

This is a tutorial how to use the em_neuron program.  This program uses [NEURON](https://www.neuron.yale.edu/neuron/).

## Installation

To first start the simulation, first install the following programs

* [NEURON](http://neuron.yale.edu/neuron/download/getstd).

After following the directions in the NEURON installation documentation, then clone the github repository for FlyEM Simulation Construction.  NOTE: Installation instructions for em_neuron is only for `x86-linux` systems.  

To start the program installation process, run the following commands:

```
cd CompressEM
nrnivmodl mod
python installationdir.py
```

The command `nrnivmodl mod` will compile the special mods that were created for the FlyEM model.  The `python installationdir.py` command is for saving the directory structure of where files are in the program.   

To run an example of the network simulation:

```
export PYTHONHOME=/usr
python savedata.py      #to convert data for CompressEM to use
python graphconvert.py  #this is to graph what neuron connects to what
python columncreate.py  #this is to grab cells in the column dataset
python columndata.py    #this is to create a dataset for column simulations
./x86_64/special -python nodetest.py 0 #this is to run the simulation of node network with stimuli right to left
```

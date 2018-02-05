# utilities.py
#
# These are various helper functions for the proTAGonist script
#
# Michael Porter 2018
# 

from pyteomics import mgf
import numpy as np

# open_aa opens up a file containing the amino acid residue masses
# and returns a dict where the keys are the amino acid single
# letter codes and the values are the masses 
def open_aa():
    AA = {}
    with open('AA.dat', 'r') as f:
        for line in f:
            line = line.rstrip()
            if line[0] == 'I':
                continue
            AA[line.split(" ")[0]] = float(line.split(" ")[3])
    return add_mods(AA)

# add_mods takes in a dict of amino acid codes/masses and then adds
# in the mods specified in the mods file
# The format for the mods in the mods file is:
# Single letter code of the residue being modified (string)
# Mass shift of the modification (float)
# Whether it's an increase/decrease in mass (+/-)
# Whether or not it's a fixed or a variable mod (f/v)
# Example:
# M 15.9949 + v
# In this case methionine is being modified with a mass increase
# of 15.9949 Da and it is a variable modification
def add_mods(AA):
    with open('MODS.dat', 'r') as f:
        for line in f:
            line = line.rstrip()
            residue = line.split(" ")[0]
            mass_shift = float(line.split(" ")[1])
            direction = line.split(" ")[2]
            type = line.split(" ")[3]
            key = residue+'['+direction+str(mass_shift)+']'
            if direction=='+':
                AA[key] = AA[residue] + mass_shift
            else:
                AA[key] = AA[residue] - mass_shift
            if type=='f':
                del AA[residue]
    return AA

# find_nearest will find the value in array that is closest to value
def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return idx

# read_mgf will read in an mgf file and return a list of the
# spectra contained within that file
def read_mgf(filename):
    spectra = mgf.read(filename)
    return spectra
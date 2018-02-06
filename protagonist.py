import sys
import utilities as util
from Spectrum import Spectrum

AA = util.open_aa()
#print(AA)
filename = sys.argv[1]
tagCandidates = util.createTagCandidates(AA)
#print(tagCandidates)
spectra = util.read_mgf(filename)

for s in spectra:
    #print(s)
    spectrum = Spectrum(s, tagCandidates)

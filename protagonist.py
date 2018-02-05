import sys
import utilities as util
from Spectrum import Spectrum

AA = util.open_aa()

filename = sys.argv[1]

spectra = util.read_mgf(filename)

for s in spectra:
    #print(s)
    print("##########")
    spectrum = Spectrum(s)
import utilities as util

class Spectrum():

    def __init__(self, spectrum):
        self.topN = 100
        self.PROTON = 1.007276
        self.raw_mz = spectrum['m/z array']
        self.raw_intensity = spectrum['intensity array']
        self.charge = spectrum['params']['charge'][0]
        self.RTinSeconds = spectrum['params']['rtinseconds']
        self.pepMass = spectrum['params']['pepmass'][0]
        self.MH = self.pepMass * self.charge - self.charge * self.PROTON + self.PROTON

        print('charge',self.charge)
        print('pepmass', self.pepMass)
        print('m+h',self.MH)
        
        # These two lists will be initialized by chooseTopN()
        self.mz = []
        self.intensity = []

        self.chooseTopN()

        # This function will create Peak objects
        self.createPeaks()

    def chooseTopN(self):
        intensity, mz = self.sortByFirstList(self.raw_intensity, self.raw_mz)
        intensityTopN = intensity[:self.topN]
        mzTopN = mz[:self.topN]
        self.mz, self.intensity = self.sortByFirstList(mzTopN, intensityTopN)

    def sortByFirstList(self, list1, list2):
        list1, list2 = (list(t) for t in zip(*sorted(zip(list1, list2))))
        return list1, list2

    def createPeaks(self):
        dummy = 0





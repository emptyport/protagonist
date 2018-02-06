import numpy as np
from scipy import stats
import utilities as util
from Peak import Peak

class Spectrum():

    def __init__(self, spectrum, tagCandidates):
        self.topN = 100
        self.mzTolerance = 0.5
        self.PROTON = 1.007276
        self.tagCandidates = tagCandidates
        self.raw_mz = spectrum['m/z array']
        self.raw_intensity = spectrum['intensity array']
        self.charge = spectrum['params']['charge'][0]
        #self.RTinSeconds = spectrum['params']['rtinseconds']
        self.pepMass = spectrum['params']['pepmass'][0]
        self.MH = self.pepMass * self.charge - self.charge * self.PROTON + self.PROTON

        #print('charge',self.charge)
        #print('pepmass', self.pepMass)
        #print('m+h',self.MH)
        
        # These lists will be initialized by chooseTopN()
        self.mz = []
        self.intensity = []
        self.ranks = []

        self.chooseTopN()

        # This function will create Peak objects
        self.peakList = []
        self.createPeaks()
        self.findTags()

    def chooseTopN(self):
        intensity, mz = self.sortByFirstList(self.raw_intensity, self.raw_mz)
        intensityTopN = intensity[:self.topN]
        mzTopN = mz[:self.topN]
        ranks = [i for i in range(self.topN, 0, -1)]
        self.mz, self.intensity = self.sortByFirstList(mzTopN, intensityTopN)
        self.mz, self.ranks = self.sortByFirstList(mzTopN, ranks)

    def sortByFirstList(self, list1, list2):
        list1, list2 = (list(t) for t in zip(*sorted(zip(list1, list2))))
        return list1, list2

    def createPeaks(self):
        for i in range(0, len(self.mz)):
            mz = self.mz[i]
            intensity = self.intensity[i]
            rank = self.ranks[i]
            counterpartMass = self.MH - mz + 1
            counterpartIndex = util.find_nearest(counterpartMass, self.mz)
            counterpartDifference = abs(self.mz[counterpartIndex] - mz)
            if counterpartDifference < self.mzTolerance:
                hasCounterpart = True
            else:
                hasCounterpart = False
            self.peakList.append(Peak(mz, intensity, hasCounterpart, rank))
        #for p in self.peakList:
        #    print(p)

    def calculateIntensityRankPValue(self, rank):
        # Shortcutting here. Code to calculate u and s is in mann-whitney-test.py
        u = 202
        s = 57.7321400954
        l = 100000000
        t = (rank-u)/(s)
        p = stats.t.cdf(t,df=l-1)
        return p
    
    def getPeak(self, mz):
        closestPeak = None
        closestDifference = 99999
        for peak in self.peakList:
            if abs(peak.mz - mz) < closestDifference:
                closestDifference = abs(peak.mz - mz)
                closestPeak = peak
        return closestPeak
    
    def findTags(self):
        for offset in self.mz:
            newMZ = np.array(self.mz) - offset
            for tagCandidate in self.tagCandidates:
                tagPeak2 = tagCandidate['peaks'][0]
                tagPeak3 = tagCandidate['peaks'][1]
                tagPeak4 = tagCandidate['peaks'][2]
                index2 = util.find_nearest(tagPeak2, newMZ)
                index3 = util.find_nearest(tagPeak3, newMZ)
                index4 = util.find_nearest(tagPeak4, newMZ)
                peak1 = 0
                peak2 = newMZ[index2]
                peak3 = newMZ[index3]
                peak4 = newMZ[index4]
                #print(peak1, peak2, peak3, peak4)
                base1 = 0
                base2 = peak2 - tagPeak2
                base3 = peak3 - tagPeak3
                base4 = peak4 - tagPeak4
                baseAvg = (base1 + base2 + base3 + base4)/4.0
                #print(base1, base2, base3, base4, baseAvg)
                ss1 = (base1 - baseAvg)**2
                ss2 = (base2 - baseAvg)**2
                ss3 = (base3 - baseAvg)**2
                ss4 = (base4 - baseAvg)**2
                sse = ss1 + ss2 + ss3 + ss4
                #print(sse)
                if sse<0.2:
                    p1 = self.getPeak(peak1 + offset)
                    p2 = self.getPeak(peak2 + offset)
                    p3 = self.getPeak(peak3 + offset)
                    p4 = self.getPeak(peak4 + offset)

                    complementScore = 0
                    for p in [p1, p2, p3, p4]:
                        if p.hasCounterpart:
                            complementScore += 1
                    rank = p1.rank + p2.rank + p3.rank + p4.rank
                    rankScore = self.calculateIntensityRankPValue(rank)
                    if rankScore < 0.1:
                        print(tagCandidate['sequence'], rankScore, complementScore)





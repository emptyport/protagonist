import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats

N = 100
numPeaks = 4

rankVals = [i for i in range(1, N+1)]
ranks = []
'''
for a in rankVals:
    for b in rankVals:
        for c in rankVals:
            for d in rankVals:
                ranks.append(a+b+c+d)

l = len(ranks)
u = np.mean(ranks)
s = np.std(ranks)
#plt.hist(ranks, bins=201)
#plt.show()
'''
u = 202
s = 57.7321400954
l = 100000000

vals = [1, 4, 100, 200, 202, 250, 300, 320, 450]

for v in vals:
    t = (v-u)/(s)
    p = stats.t.cdf(t,df=l-1)

    print(v,t,p)



import numpy as np
from matplotlib import pyplot as plt

class stat2d:

    @staticmethod
    def joint(fs1,fs2):
        maxn = max(np.max(fs1.N),np.max(fs2.N))
        bins = np.arange(maxn)
        print bins
        return np.histogram2d(fs1.N,fs2.N,bins = bins)

    @staticmethod
    def plotjoint(histogram):
        X, Y = np.meshgrid(histogram[1], histogram[2])
        plt.pcolormesh(X, Y, histogram[0])

    @staticmethod
    def g2(fs1,fs2):
        avgprod = np.mean(fs1.N*fs2.N)
        #print avgprod
        avgfs1 = np.mean(fs1.N)
        #print avgfs1
        avgfs2 = np.mean(fs2.N)
        #print avgfs2
        return avgprod/(avgfs1*avgfs2)

    @staticmethod
    def g2fromcounts(N1,N2):
        avgprod = np.mean(N1*N2)
        #print avgprod
        avgfs1 = np.mean(N1)
        #print avgfs1
        avgfs2 = np.mean(N2)
        #print avgfs2
        return avgprod/(avgfs1*avgfs2)
import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries
from multimethods import multimethod

overload = multimethod

class stat2d:
    # TODO: let instance of this class be a representation of joint statistics
    
    @staticmethod
    def joint(fs1,fs2):
        # TODO: resolve strange problem with empty data...
        maxn = max(np.max(fs1.N),np.max(fs2.N))
        bins = np.arange(maxn)
        # print bins
        return np.histogram2d(fs1.N,fs2.N,bins = bins)

    @staticmethod
    def plotjoint(histogram,showvalues=True):
        # TODO: choose counts or probabilites
        X, Y = np.meshgrid(histogram[1], histogram[2])
        plt.pcolormesh(X, Y, histogram[0])
        if showvalues:
            for i, v in np.ndenumerate(histogram[0]):
                # FIXME: better text positioning
                plt.text(i[0]+0.4,i[1]+0.4,"%d"%v)

    @staticmethod
    @overload( frameseries, frameseries)
    def g2(fs1,fs2):
        avgprod = np.mean(fs1.N*fs2.N)
        avgfs1 = np.mean(fs1.N)
        avgfs2 = np.mean(fs2.N)
        return avgprod/(avgfs1*avgfs2)

    @staticmethod
    @overload( np.ndarray, np.ndarray)
    def g2(N1,N2):
        avgprod = np.mean(N1*N2)
        avgfs1 = np.mean(N1)
        avgfs2 = np.mean(N2)
        return avgprod/(avgfs1*avgfs2)
    
    @staticmethod
    def fanofactor(fs1,fs2):
        # TODO: implement
        pass
    
    
  
      
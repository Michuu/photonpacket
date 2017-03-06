import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries
from multimethods import multimethod
from exceptions import FrameSeriesLenError
overload = multimethod

class stat2d:
    # TODO: let instance of this class be a representation of joint statistics
    
    @staticmethod
    @overload( frameseries, frameseries)
    def joint(fs1,fs2):
        # TODO: resolve strange problem with empty data...
        checkfs(fs1,fs2)
        maxn = max(np.max(fs1.N),np.max(fs2.N))
        bins = np.arange(maxn)
        return np.histogram2d(fs1.N,fs2.N,bins = bins)
    
    @staticmethod
    @overload( np.ndarray, np.ndarray)
    def joint(N1, N2):
        # TODO: resolve strange problem with empty data...
        checkcounts(N1,N2)
        maxn = max(np.max(N1),np.max(N2))
        bins = np.arange(maxn)
        return np.histogram2d(N1,N2,bins = bins)


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
        stat2d.checkfs(fs1,fs2)
        avgprod = np.mean(fs1.N*fs2.N)
        avgfs1 = np.mean(fs1.N)
        avgfs2 = np.mean(fs2.N)
        return avgprod/(avgfs1*avgfs2)

    @staticmethod
    @overload( np.ndarray, np.ndarray)
    def g2(N1,N2):
        stat2d.checkcount(N1,N2)
        avgprod = np.mean(N1*N2)
        avgfs1 = np.mean(N1)
        avgfs2 = np.mean(N2)
        return avgprod/(avgfs1*avgfs2)
    
    @staticmethod
    def fanofactor(fs1,fs2):
        # TODO: implement
        pass
    
    @staticmethod
    def checkfs(fs1,fs2):
        if (fs1.len() != fs2.len()):
            raise FrameSeriesLenError()
    
    @staticmethod
    def checkcounts(N1,N2):
        if (N1.shape[0] != N2.shape[0]):
            raise FrameSeriesLenError()
    
    
    
  
      
import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries
from exceptions import FrameSeriesLenError
from stat1d import stat1d

class stat2d:
    '''
    Class for 2D statistics
    '''
    # TODO: let instance of this class be a representation of joint statistics
    
    @staticmethod
    def joint(s1, s2, normed=False):
        '''
        Create joint statistics histogram
        '''
        if s1.__class__ == frameseries and s2.__class__ == frameseries:
            stat2d.checkfs(s1,s2)
            N1 = s1.N
            N2 = s2.N
        elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
            stat2d.checkcounts(s1,s2)
            N1 = s1
            N2 = s2
        else:
            raise ValueError
        maxn = max(np.max(N1)+1,np.max(N2)+1)
        bins = np.arange(maxn)
        return np.histogram2d(N1, N2, bins = bins, normed=normed)

    @staticmethod
    def plotjoint(histogram, showvalues=True, cmap=plt.rcParams['image.cmap']):
        '''
        Plot the joint statistics histogram generated with :func:`joint`
        '''
        X, Y = np.meshgrid(histogram[1], histogram[2])
        plt.pcolormesh(X, Y, histogram[0], cmap=cmap)
        if showvalues:
            for i, v in np.ndenumerate(histogram[0]):
                # FIXME: better text positioning
                plt.text(i[1]+0.4, i[0]+0.4, "%d"%v)

    @staticmethod
    def g2(s1,s2,uncert=False):
        '''
        Second order cross-correlation function.
        
        '''
        if s1.__class__ == frameseries and s2.__class__ == frameseries:
            stat2d.checkfs(s1,s2)
            N1 = s1.N
            N2 = s2.N
        elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
            stat2d.checkcounts(s1,s2)
            N1 = s1
            N2 = s2
        else:
            raise ValueError
        meanprod = np.mean(N1*N2)
        mean1 = np.mean(N1)
        mean2 = np.mean(N2)
        g2 = meanprod/(mean1*mean2)
        if uncert:
            Nframes = len(N1)
            unc_mean1 = np.sqrt(np.sum(N1))/Nframes
            unc_mean2 = np.sqrt(np.sum(N2))/Nframes
            # uncertainty of nominator
            unc_nom = np.sqrt(np.sum(N1*N2))/Nframes
            # uncertainty of denominator
            unc_den = mean1*mean2*\
            np.sqrt((unc_mean1/mean1)**2+(unc_mean2/mean2)**2)
            # uncertainty of g2
            unc = g2*np.sqrt((unc_den/(mean1*mean2))**2+(unc_nom/meanprod)**2)
            return (g2,unc)
        else:
            return g2
    
    @staticmethod
    def fanofactor(s1,s2):
        '''
        Fano photon number noise reduction factor.
        
        Parameters
        '''
        return (stat1d.var(s1)+stat1d.var(s2)-2*stat2d.covar(s1,s2))/\
            (stat1d.mean(s1)+stat1d.mean(s2))
    
    def Wfactor(s1,s2):
        '''
        Mean-weighted noise reduction factor. See Notes for details.
        
        Parameters
        
        Returns
        
        Notes
        
        '''
        if s1.__class__ == frameseries and s2.__class__ == frameseries:
            stat2d.checkfs(s1,s2)
            N1 = s1.N
            N2 = s2.N
        elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
            stat2d.checkcounts(s1,s2)
            N1 = s1
            N2 = s2
        else:
            raise ValueError
        nor = np.sqrt(1.0/stat1d.mean(N1)+1.0/stat1d.mean(N2))
        w = N1/stat1d.mean(N1) - N2/stat1d.mean(N2)
        return stat1d.var(w/nor)
    
    @staticmethod
    def checkfs(fs1,fs2):
        '''
        Check if frameseries have proper shapes
        '''
        if (fs1.len() != fs2.len()):
            raise FrameSeriesLenError()
    
    @staticmethod
    def checkcounts(N1,N2):
        '''
        Check if count vectors have proper shapes
        '''
        if (N1.shape[0] != N2.shape[0]):
            raise FrameSeriesLenError()
    
    @staticmethod
    def covar(s1,s2):
        '''
        Photon number covariance
        '''
        if s1.__class__ == frameseries and s2.__class == frameseries:
            stat2d.checkfs(s1,s2)
            N1 = s1.N
            N2 = s2.N
        elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
            stat2d.checkcounts(s1,s2)
            N1 = s1
            N2 = s2
        else:
            raise ValueError
        cv = np.cov(N1, N2)
        return cv[1,1]
    
    @staticmethod
    def cov(s1,s2):
        '''
        Short for :func:`covar`
        '''
        return stat2d.covar(s1,s2)
    
    @staticmethod
    def corr(s1,s2):
        '''
        Normalized photon-number correlation coefficient
        '''
        return stat2d.covar(s1,s2)/np.sqrt(stat1d.var(s1)*stat1d.var(s2))  
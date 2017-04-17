import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries
from exceptions import FrameSeriesLenError
import stat1d
from uncertainties import ufloat, umath

def rawmoment(s1, s2, i, j, uncert=False):
    if s1.__class__ == frameseries and s2.__class__ == frameseries:
        checkfs(s1,s2)
        N1 = s1.N
        N2 = s2.N
    elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
        checkcounts(s1,s2)
        N1 = s1
        N2 = s2
    else:
        raise ValueError
    if uncert:
        return ufloat(np.mean(N1**i * N2**j), np.std(N1**i * N2**j)/np.sqrt(len(N1)))
    else:
        return np.mean(N1**i * N2**j)
    
def g2(s1, s2, uncert=False):
    '''
    Second order cross-correlation function.
    
    '''
    if s1.__class__ == frameseries and s2.__class__ == frameseries:
        checkfs(s1,s2)
        N1 = s1.N
        N2 = s2.N
    elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
        checkcounts(s1,s2)
        N1 = s1
        N2 = s2
    else:
        raise ValueError
    return rawmoment(N1,N2,1,1,uncert)/(stat1d.rawmoment(N1,1,uncert)*stat1d.rawmoment(N2,1,uncert))

def fanofactor(s1, s2, uncert=False):
    '''
    Fano photon number noise reduction factor.
    
    Parameters
    '''
    return (stat1d.var(s1, uncert)+stat1d.var(s2, uncert)-2*covar(s1,s2))/\
        (stat1d.mean(s1, uncert)+stat1d.mean(s2, uncert))

def Wfactor(s1,s2):
    '''
    Mean-weighted noise reduction factor. See Notes for details.
    
    Parameters
    
    Returns
    
    Notes
    
    '''
    if s1.__class__ == frameseries and s2.__class__ == frameseries:
        checkfs(s1,s2)
        N1 = s1.N
        N2 = s2.N
    elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
        checkcounts(s1,s2)
        N1 = s1
        N2 = s2
    else:
        raise ValueError
    nor = np.sqrt(1.0/stat1d.mean(N1)+1.0/stat1d.mean(N2))
    w = N1/stat1d.mean(N1) - N2/stat1d.mean(N2)
    return stat1d.var(w/nor)

def checkfs(fs1,fs2):
    '''
    Check if frameseries have proper shapes
    '''
    if (fs1.len() != fs2.len()):
        raise FrameSeriesLenError()

def checkcounts(N1,N2):
    '''
    Check if count vectors have proper shapes
    '''
    if (N1.shape[0] != N2.shape[0]):
        raise FrameSeriesLenError()

def covar(s1,s2, uncert=False):
    '''
    Photon number covariance
    '''
    if s1.__class__ == frameseries and s2.__class__ == frameseries:
        checkfs(s1,s2)
        N1 = s1.N
        N2 = s2.N
    elif s1.__class__ == np.ndarray and s2.__class__ == np.ndarray:
        checkcounts(s1,s2)
        N1 = s1
        N2 = s2
    else:
        raise ValueError
    return rawmoment(N1, N2, 1, 1, uncert)-stat1d.rawmoment(N1, 1, uncert)*stat1d.rawmoment(N2, 1, uncert)

def cov(s1, s2, uncert=False):
    '''
    Short for :func:`covar`
    '''
    return covar(s1,s2)

def corr(s1, s2, uncert=False):
    '''
    Normalized photon-number correlation coefficient
    '''
    if uncert:
        return covar(s1,s2,uncert)/umath.sqrt(stat1d.var(s1,uncert)*stat1d.var(s2,uncert))      
    else:
        return covar(s1,s2,uncert)/np.sqrt(stat1d.var(s1,uncert)*stat1d.var(s2,uncert)) 

def R2(s1,s2, uncert=False):
    '''
    R2 factor from the Cauchy-Scharz inequality
    '''
    return g2(s1,s2, uncert)**2/(stat1d.g2(s1, uncert)*stat1d.g2(s2, uncert))
# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from scipy.special import gamma
from frameseries import frameseries
from scipy.stats import moment
from uncertainties import ufloat, umath

 
def centralmoment(s, m):
    if s.__class__ == frameseries:
        N = s.N
    elif s.__class__ == np.ndarray:
        N = s
    else:
        raise ValueError
    return moment(N, m)

def rawmoment(s, m, uncert=False):
    if s.__class__ == frameseries:
        N = s.N
    elif s.__class__ == np.ndarray:
        N = s
    else:
        raise ValueError
    if uncert:
        return ufloat(np.mean(N**m), np.std(N**m)/np.sqrt(len(N)))
    else:
        return np.mean(N**m)


def mean(s, uncert=False):
    '''
    Calculate the mean photon number
    
    Parameters
    ----------
    s : :class:`photonpacket.frameseriesq` or :class:`np.ndarray` 
        Series of photon frames or photon counts
    
    Returns
    ----------
    double
        Mean photon number
        
    Notes
    ----------
    The mean photon number is calculated as
        
    .. math:: \langle n \\rangle = \sum_i^N n_i / N
    
    where :math:`n_i` is the total number of photons in frame :math:`i` and :math:`N` is the total number of frames in the series.

    
    References
    ----------
    
    Examples
    ----------
    >>> fs.mean()
    0.553

    '''
    if s.__class__ == frameseries:
        N = s.N
    elif s.__class__ == np.ndarray:
        N = s
    else:
        raise ValueError
    if uncert:
        return rawmoment(N, 1, uncert=True)
    else:
        return np.mean(N)
  
def var(s, uncert=False):
    if s.__class__ == frameseries:
        N = s.N
    elif s.__class__ == np.ndarray:
        N = s
    else:
        raise ValueError
    if uncert:
        return rawmoment(N, 2, uncert=True)-rawmoment(N, 1, uncert=True)**2
    else:
        return np.var(N)
  
def std(s, uncert=False):
    if s.__class__ == frameseries:
        N = s.N
    elif s.__class__ == np.ndarray:
        N = s
    else:
        raise ValueError
    if uncert:
        return umath.sqrt(var(N, uncert=True))
    else:
        return np.std(N)

def subbinomal(fs):
    '''
    Calculate the sub-binomial paramter
    
    Parameters
    ----------
    fs : :class:`photonpacket.frameseries`
        Series of photon frames
    
    Returns
    ----------
    double
        The sub-binomial parameter
        
    Notes
    ----------
    The sub-binomial parameter was introduced in [1]_
    
    References
    ----------
    .. [1] J. Sperling, W. Vogel, and G. S. Agarwal, “Sub-binomial light”, `Phys. Rev. Lett. 109, 093601 (2012) <https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.109.093601>`_.
    
    Examples
    ----------
    >>> fs.subbinomial()
    1
    
    '''
    pass
    
def qmandel(fs):
    '''
    Q_M
    Mandel Q parameter
    TODO: implement
    '''
    pass

def thmodes(fs, uncert=False):
    '''
    Calculate the number of modes estimated assuming the photons are distributed thermally
    
    Parameters
    ----------
    fs : :class:`photonpacket.frameseries`
        Series of photon frames
    
    Returns
    ----------
    double
        Estimated number of thermal modes
        
    See Also
    ----------
    qmandel : Related Mandel Q Parameter
    
    Notes
    ----------
    Number of thermal modes may be estimated as:
        
    .. math:: M = \langle n \\rangle^2 / (\Delta^2 n - \langle n \\rangle)
    
    where :math:`\langle n \\rangle` is the mean photon number and :math:`\Delta^2 n` is photon number variance.

    
    References
    ----------
    
    Examples
    ----------
    >>> fs.thmodes()
    1
    
    '''
    return mean(fs, uncert)**2/(var(fs, uncert)-mean(fs, uncert))

def g2(s, uncert=False):
    '''
    Second order autocorrelation
    '''
    if s.__class__ == frameseries:
        N = s.N
    elif s.__class__ == np.ndarray:
        N = s
    else:
        raise ValueError
    return 1+(var(N, uncert)-mean(N, uncert))/(mean(N, uncert)**2)
    



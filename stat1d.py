# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from scipy.special import gamma
from frameseries import frameseries
from scipy.stats import moment
from uncertainties import ufloat

class stat1d:
        
    @staticmethod  
    def centralmoment(s, m, uncert=False):
        return moment(N, m)
    
    @staticmethod
    def rawmoment(s, m, uncert=False):
        return np.mean(N**m)
    
    @staticmethod
    def mean(s):
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
        return np.mean(N)
      
    @staticmethod
    def var(s):
        if s.__class__ == frameseries:
            N = s.N
        elif s.__class__ == np.ndarray:
            N = s
        else:
            raise ValueError
        return np.var(N)
      
    @staticmethod
    def std(fs):
        if s.__class__ == frameseries:
            N = s.N
        elif s.__class__ == np.ndarray:
            N = s
        else:
            raise ValueError
        return np.std(N)
    
    @staticmethod
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
        
    @staticmethod   
    def qmandel(fs):
        '''
        Q_M
        Mandel Q parameter
        TODO: implement
        '''
        pass
    
    @staticmethod
    def thmodes(fs):
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
        return stat1d.mean(fs)**2/(stat1d.var(fs)-stat1d.mean(fs))
    
    @staticmethod
    def g2(s):
        '''
        Second order autocorrelation
        '''
        if s.__class__ == frameseries:
            N = s.N
        elif s.__class__ == np.ndarray:
            N = s
        else:
            raise ValueError
        return 1+(stat1d.var(N)-stat1d.mean(N))/(stat1d.mean(N)**2)
        
    @staticmethod
    def nmodethermal(n, navg, M):
        pass
    
    
    @staticmethod
    def coherent(n, navg):
        pass
    
    
    
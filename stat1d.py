# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from scipy.special import gamma

class stat1d:
    # TODO: let instance of this class be a representation of statistics (histogram)
    
    @staticmethod
    def stat(fs):
        bins = np.arange(np.max(fs.N)+2)
        return np.histogram(fs.N, bins=bins)
    
    @staticmethod
    def plotstat(h, **kwargs):
        if 'log' in kwargs:
            log = kwargs['log']
        else:
            log = False
        plt.bar(h[1][:-1], h[0], log=log)
      
    @staticmethod
    def mean(fs):
        '''
        Calculate the mean photon number
        
        Parameters
        ----------
        fs : frameseries
            Series of photon frames
        
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
        return np.mean(fs.N)
      
    @staticmethod
    def var(fs):
        return np.var(fs.N)
      
    @staticmethod
    def std(fs):
        return np.std(fs.N)
    
    @staticmethod
    def subbinomal(fs):
        '''
        Calculate the sub-binomial paramter
        
        Parameters
        ----------
        fs : frameseries
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
        fs : frameseries
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
    def nmodethermal(n, navg, M):
        pass
    
    
    @staticmethod
    def coherent(n, navg):
        pass
    
    
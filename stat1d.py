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
        Q_b
        Sub-binomal 
        see J. Sperling, W. Vogel, and G. S. Agarwal, “Sub-binomial light,” 
        Phys. Rev. Lett. 109, 093601 (2012).
        TODO: implement
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
        number of modes estimated assuming the photons are distributed thermally
        M = mean^2 / (variance - mean)
        '''
        return stat1d.mean(fs)**2/(stat1d.var(fs)-stat1d.mean(fs))
    
    @staticmethod
    def nmodethermal(n, navg, M):
        pass
    
    
    @staticmethod
    def coherent(n, navg):
        pass
    
    
# -*- coding: utf-8 -*-
import numpy as np

class stat1d:
    # TODO: let instance of this class be a representation of statistics (histogram)
    
    @staticmethod
    def stat(fs):
        # TODO: implement
        pass
      
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
    def mandel(fs):
        '''
        Q_M
        Mandel Q parameter
        TODO: implement
        '''
        pass
    
    
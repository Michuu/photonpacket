from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries


class hist1d:
    '''
    
    Paramters
    '''
    hist = np.array([])
    bins = np.array([])
    N = 0
    normed = False
    
    @staticmethod
    def fromcounts(N):
        '''
            
        Paramterers
        ---------
        N: np.array
            array of counts

        '''
        bins = np.arange(np.max(N)+2)
        h = np.histogram(N, bins=bins)
        return hist1d(h[0],h[1])
    
    @staticmethod
    def fromfs(fs):
        '''
        
        Parameters
        --------
        fs: frameseries
            frameseries object
            
        '''
        bins = np.arange(np.max(fs.N)+2)
        h = np.histogram(fs.N, bins=bins)
        return hist1d(h[0],h[1])
        
    def __init__(self, hist, bins):
        '''
        
        '''
        self.hist = hist
        self.bins = bins
        self.N = np.sum(hist)
        
    def plot(self, log=False, normed=False):
        '''
        '''
        if normed:
            plt.bar(self.bins[:-1], self.hist/self.N, log=log)     
        else:
            plt.bar(self.bins[:-1], self.hist, log=log)
        
    def mean(self):
        '''
        '''
        return np.average(self.bins[:-1], weights=self.hist, axis=0)
        
    def mean2(self):
        '''
        '''
        return np.average(self.bins[:-1], weights=self.hist, axis=0)**2
       
    def avgn2(self):
        '''
        '''
        return np.average(self.bins[:-1]**2, weights=self.hist, axis=0)
    
    def var(self):
        '''
        '''
        return self.avgn2() - self.mean2()
    
    def g2(self):
        '''
        '''
        return 1.0+(self.avgn2()-self.mean2()-self.mean())/self.mean2()
        
    def thmodes(self):
        '''
        '''
        return self.mean2()/(self.avgn2()-self.mean2()-self.mean())
    
    def subbinomial(self):
        '''
        '''
        pass
    
    def qmandel(self):
        '''
        '''
        pass
        
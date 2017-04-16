# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot as plt
from scipy.special import gamma
from frameseries import frameseries
from hist1d import hist1d
from __future__ import division

class hist2d:
    bins = np.array([])
    hist = np.array([])
    N = 0
    normed = False
    
    @staticmethod
    def fromfs(fs1, fs2):
        '''
        Create joint statistics histogram
        '''
        maxn = max(np.max(fs1.N)+2, np.max(fs2.N)+2)
        bins = np.arange(maxn)
        hist = np.histogram2d(fs1.N, fs2.N, bins = bins, normed=False)
        return hist2d(hist[0], (hist[1], hist[2]))
    
    @staticmethod
    def fromcount(N1, N2):
        '''
        Create joint statistics histogram
        '''
        maxn = max(np.max(N1)+2, np.max(N2)+2)
        bins = np.arange(maxn)
        hist = np.histogram2d(N1, N2, bins = bins, normed=False)
        return hist2d(hist[0], (hist[1], hist[2]))
    
    def __init__(self, hist, bins):
        self.hist = hist
        self.bins = bins
        self.N = np.sum(hist)
    
    def __getitem__(self, i):
        if self.normed:
            return self.hist[i]/self.N
        else:
            return self.hist[i]
    
    def setnorm(self, normed):
        self.normed = normed
        
    def gethist(self, normed=self.normed):
        if normed:
            return self.hist/self.N
        else:
            return self.hist
        
    def plot(self, showvalues=False, cmap='viridis', normed=self.formed):
        '''
        Plot the joint statistics histogram generated with :func:`joint`
        '''
        X, Y = np.meshgrid(self.bins[0], self.bins[1])
        if normed:
            plt.pcolormesh(X, Y, self.hist/self.N, cmap=cmap)
        else:
            plt.pcolormesh(X, Y, self.hist, cmap=cmap)
        ax=plt.gca()
        ax.set_xticks(self.bins[0][:-1]+0.5)
        ax.set_xticklabels(np.array(self.bins[0][:-1], dtype=np.uint16))
        ax.set_yticks(self.bins[1][:-1]+0.5)
        ax.set_yticklabels(np.array(self.bins[1][:-1], dtype=np.uint16))       
        if showvalues:
            for i, v in np.ndenumerate(self.hist):
                plt.text(i[1]+0.4, i[0]+0.4, "%d"%v)
    
    def rawmoment(self, i, j):
        return np.average(self.bins[0][:-1]**i, self.bins[0][:-1]**j,
                          weights=self.hist)
        
    def mariginal(self, axis):
        return hist1d(np.sum(self.hist, axis=axis), self.bins[axis])
    
    def csec(self, i, axis):
        if axis == 0:
            return hist1d(self.hist[:, i], self.bins[axis])
        elif axis == 1:
            return hist1d(self.hist[i, :], self.bins[axis])
        else:
            raise ValueError
    
    def g2(self):
        pass
    
    def Wfactor(self):
        pass
    
    def fanofactor(self):
        pass
    
    def covar(self):
        pass
    
    def cov(self):
        pass
    
    def corr(self):
        pass
    
    def R2(self):
        pass
    
    def p11(self):
        return self.hist[1,1]/self.N
    
    def N11(self):
        return self.hist[1,1]
    
    def mean(self, axis):
        if axis == 0:
            return self.rawmoment(1,0)
        elif axis == 1:
            return self.rawmoment(0,1)
        else:
            raise ValueError
            
    def var(self, axis):
        if axis == 0:
            return self.rawmoment(2,0)-self.rawmoment(1,0)**2
        elif axis == 1:
            return self.rawmoment(0,2)-self.rawmoment(0,1)**2
        else:
            raise ValueError
        
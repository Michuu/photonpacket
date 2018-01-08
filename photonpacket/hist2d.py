from __future__ import division
import numpy as np
from matplotlib import pyplot as plt
from scipy.special import gamma
from frameseries import frameseries
from hist1d import hist1d
import matplotlib.cm as cmx
import matplotlib as mpl
from helpers import opcolor
from mpl_toolkits.mplot3d import Axes3D

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
        '''
        '''
        self.hist = hist
        self.bins = bins
        self.N = np.sum(hist)
    
    def __getitem__(self, i):
        '''
        '''
        if self.normed:
            return self.hist[i]/self.N
        else:
            return self.hist[i]
    
    def setnorm(self, normed):
        '''
        '''
        self.normed = normed
        
    def gethist(self, normed=None):
        '''
        '''
        if normed is None:
            normed = self.normed
        if normed:
            return self.hist/self.N
        else:
            return self.hist
        
    def plot(self, showvalues=False, normed=None, cmap=None, log=None, cut=None):
        '''
        Plot the joint statistics histogram generated with :func:`joint`
        '''
        if normed is None:
            normed = self.normed
        X, Y = np.meshgrid(self.bins[0], self.bins[1])
        if normed:
            data = self.hist/self.N  
        else:
			data = self.hist			
        q=-1
        if cut:
			data=data[:3,:3]
			X=X[:3,:3]
			Y=Y[:3,:3]
			q=2
        if log is None or log == False:
            norm = mpl.colors.Normalize(vmin=data.min(), vmax=data.max())
        else:
            vmin = np.min(data[np.nonzero(data)])
            norm = mpl.colors.LogNorm(vmin=vmin, vmax=data.max())
        cplt = plt.pcolormesh(X, Y, data, cmap=cmap, norm=norm)
        ax = plt.gca()
        ax.set_xticks(self.bins[0][:q]+0.5)
        ax.set_xticklabels(np.array(self.bins[0][:q], dtype=np.uint16))
        ax.set_yticks(self.bins[1][:q]+0.5)
        ax.set_yticklabels(np.array(self.bins[1][:q], dtype=np.uint16))
        vmin, vmax = plt.gci().get_clim()
        cm = cplt.get_cmap()
        sm = cmx.ScalarMappable(norm=norm, cmap=cm)
        plt.xlabel('Region 1')
        plt.ylabel('Region 2')
        if showvalues:
            for i, v in np.ndenumerate(data):
                rgba = opcolor(sm.to_rgba(v))
                if normed:
                    plt.text(i[1]+0.4, i[0]+0.4, "%.3e" % v, color=rgba)
                else:
                    plt.text(i[1]+0.4, i[0]+0.4, "%d" % v, color=rgba)
                    
    def plot3d(self, normed=False, cmap=None, fill=0.7, alpha=0.95, log=False):
        '''
        Plot the histogram as 3D bar plot
        '''
        if normed:
            data = self.hist/self.N  
        else:
            data = self.hist
        X, Y = np.meshgrid(self.bins[0][:-1], self.bins[1][:-1])
        xpos, ypos = X, Y
        xpos = xpos.flatten('F')
        ypos = ypos.flatten('F')
        zpos = np.zeros_like(xpos)
        if log is None or log == False:
            v = data
        else:
            v = np.log10(data+1.0)
        ma = v.max()
        mi = v.min()
        dv = ma - mi
        values = (v.flatten()-mi)/(dv)
        cmap = cmx.get_cmap(cmap)
        colors = cmap(values)
    
        dx = fill * np.ones_like(zpos)
        dy = dx.copy()
        dz = v.flatten()
        ax=plt.gca(projection='3d')
        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=colors, zsort='average',alpha=alpha)

    def rawmoment(self, i, j):
        '''
        '''
        return np.average(np.outer(self.bins[0][:-1]**i, self.bins[0][:-1]**j),
                          weights=self.hist)

    def mariginal(self, axis):
        '''
        '''
        return hist1d(np.sum(self.hist, axis=axis), self.bins[axis])
    
    def csec(self, i, axis):
        '''
        '''
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
        '''
        '''
        g2a = self.mariginal(axis=0).g2()
        g2b = self.mariginal(axis=1).g2()
        g2ab = self.g2()
        return g2ab**2/(g2a*g2b)
    
    def p11(self):
        '''
        '''
        return self.hist[1,1]/self.N
    
    def N11(self):
        '''
        '''
        return self.hist[1,1]
    
    def mean(self, axis=None):
        '''
        '''
        if axis == 0:
            return self.rawmoment(1,0)
        elif axis == 1:
            return self.rawmoment(0,1)
        elif axis is None:
            return np.average(np.sum.outer(self.bins[0][:-1], self.bins[1][:-1]),
                              weights=self.hist)
        else:
            raise ValueError
         
    def var(self, axis):
        '''
        '''
        if axis == 0:
            return self.rawmoment(2,0)-self.rawmoment(1,0)**2
        elif axis == 1:
            return self.rawmoment(0,2)-self.rawmoment(0,1)**2
        else:
            raise ValueError
        
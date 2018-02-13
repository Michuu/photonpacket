# -*- coding: utf-8 -*-

#%%
photons = np.array()
#%%
import numpy as np
#%%
N=np.array([1,1,3,4,6,1,3,0,2,2])
idxs=np.r_[0, np.cumsum(N)]
pmask = N<=4
mask = np.repeat(pmask, N)

nidxs=np.r_[0, np.cumsum(mask)][idxs]
#%%
a=np.array([1,2,3])
b=np.array([4,5,6])
c=np.array([7,8,9,10])
np.stack([a,b,c],axis=1).flatten()
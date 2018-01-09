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
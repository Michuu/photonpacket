import numpy as np

array = np.concatenate(fs.frames)
shape=fs.shape
aux_shape = np.sort(shape)[::-1]
sel = np.argsort(shape)[::-1]
flat_array = np.zeros(shape=array.shape[0],dtype=np.int64)
exp = 1
array = array[:,sel]
for dim, size in enumerate(aux_shape):
    flat_array = flat_array + array[:,dim] * exp
    exp = exp * size
accum = np.bincount(flat_array, minlength = np.prod(aux_shape))
#%%
accum = np.zeros((250,600))
for frame in fs2.frames:
    for photon in frame:
        accum[photon[0],photon[1]]=accum[photon[0],photon[1]]+1
                    
                     
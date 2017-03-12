# -*- coding: utf-8 -*-

import sys
sys.path.append('/Users/michal/Repozytoria')
from matplotlib import pyplot as plt
import numpy as np
import time

import photonpacket as pp

f=pp.file.read('tests/pom1-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw0.00G-dr6.02G-pw0.0m-pr0.0m-fs100x400-nf50k-T0-fB0-fT0k-II2.60-sr0.dat')
fs=f.getframeseries()

#%%
m1 = int(round(time.time() * 1000))
accum = np.zeros(shape=np.prod(fs.shape))
i = np.argmax(fs.shape)
m = np.max(fs.shape)
j = int(not i)
flat_fs = np.concatenate(fs.frames)
flat_fs = flat_fs[:,i] + m * flat_fs[:,j]
accum1 = np.bincount(flat_fs,minlength = np.prod(fs.shape))
accum1 = np.reshape(accum1,fs.shape)

m2=int(round(time.time() * 1000))
accum2=np.zeros(shape=fs.shape)
for fr in fs.frames:
    for photon in fr:
        accum2[photon[0],photon[1]]=accum2[photon[0],photon[1]]+1
m3=int(round(time.time() * 1000))

print m2-m1
print m3-m2
#%%
flat_fs = np.concatenate(fs.frames)
shape=(100,400)
array=flat_fs
aux_shape = np.sort(shape)[::-1]
sel = np.argsort(shape)[::-1]
flat_array = np.zeros(shape=array.shape[0],dtype=np.uint16)
exp = 1
array = array[:,sel]
for dim, size in enumerate(aux_shape):
    flat_array = flat_array + array[:,dim] * exp
    exp = exp * size
accum = np.bincount(flat_array, minlength = np.prod(aux_shape))
accum = np.reshape(accum,shape)
#%%
sk = np.argsort(map(len,fs.frames))
sN = np.sort(map(len,fs.frames))
np.array(fs.frames)[sk]
#%%
signs = (True, True)
i=0
cframes = np.zeros(shape=(0,2),dtype=np.uint16)
acc=np.zeros(shape=(fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1),dtype=np.uint32)
for frame in fs1.frames:
    if i%10000==0:
        print i
    frame2 = fs2.frames[i]
    if len(frame2) != 0 and len(frame) != 0:
        #cframe = np.hstack((
        #        np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),
        #        np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)
        #        ))
        cfx=np.meshgrid(frame[:,0],frame2[:,0])
        cfy=np.meshgrid(frame[:,1],frame2[:,1])
        cframe2 = np.zeros(shape=(len(cfx[0].flatten()),2),dtype=np.uint16)
        if signs[0]:
            cframe2[:,0] = cfx[0].flatten() + cfx[1].flatten()
        else:
            cframe2[:,0] = cfx[0].flatten() - cfx[1].flatten() + fs2.shape[0]
        if signs[1]:
            cframe2[:,1] = cfy[0].flatten() + cfy[1].flatten()
        else:
            cframe2[:,1] = cfy[0].flatten() - cfy[1].flatten() + fs2.shape[1]
        cframes = np.append(cframes,cframe2,axis=0)
        if len(cframes) > 1000000 or i == fs1.len() - 1:
            acc+=bincountnd(cframes,(fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1))
            cframes = np.zeros(shape=(0,2),dtype=np.uint16)          
        acc+=bincountnd(cframe2,(fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1))
    i += 1
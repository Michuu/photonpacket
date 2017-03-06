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
m1=int(round(time.time() * 1000))
accum=np.zeros(shape=np.prod(fs.shape))
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
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
# for fr in fs.frames:
    # flat_fs=np.concatenate((flat_fs,fr[:,i] + m * fr[:,j]))
    # bc = np.bincount(flat_frame,minlength = np.prod(fs.shape))
    # bc = np.reshape(bc,fs.shape)
    # accum=accum+bc
accum = np.bincount(flat_fs,minlength = np.prod(fs.shape))
accum = np.reshape(accum,fs.shape)

m2=int(round(time.time() * 1000))
accum=np.zeros(shape=fs.shape)
for fr in fs.frames:
    for photon in fr:
        accum[photon[0],photon[1]]=accum[photon[0],photon[1]]+1
m3=int(round(time.time() * 1000))

print m2-m1
print m3-m2
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 13:53:12 2019

@author: michal
"""

#%%
import numpy as np
#from .frameseries import frameseries
import re
import os
from photonpacket.message import progress
from photonpacket import settings
#from .message import message, progress
#from . import settings
#from .helpers import siprefix
import io
# from scipy.sparse import dok_matrix, kron, csr_matrix, coo_matrix
import time

def py3_fromfile(f, dtype, num):
    #buf = np.empty(num, dtype,order='F')
    #b = bytearray(num*np.dtype(dtype))
    #f.readinto(b)
    dt = np.dtype(dtype)
    return np.frombuffer(f.read(num*dt.itemsize), dtype)

settings.verbose=3
#%%
s=time.time()
f = io.open(r"C:\Users\michal\Desktop\pom1-wiecejFotonow-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw5.24G-dr6.64G-pw16.1m-pr12.3m-fs250x450-nf1000k-T70-fB200-fT11k-II2.75-sr0.dat",'rb')
#f=io.BytesIO(ff.read(-1))
frames = []
empty_frame = np.empty(shape=(0, 2), dtype=np.uint16)
nxy=0
img=0
frame=0
frames_limit=False
maxframes=1e9
rounding=False
photinfoMask = slice(None,2,None)
div=10

nframes=0
while(True):
    # read number of photons in a frame
    # nxy = (number of photons, information per photon)
    nxy =py3_fromfile(f, '>i4', 2) 
    #print(nxy)
    # break if file ended or acquired enough frames
    if nxy.size == 0 or (nframes >= maxframes and frames_limit):
        break
    N = nxy[0] * nxy[1]
    nframes += 1
    # read frame data

    if N > 0:
        # TODO: possibility of getting other info about photons,
        #       add dtype attribute basing on rounding parameter
        #       (double or uint) and propagate it to getframeseries
        # extract only photon positions
        img = py3_fromfile(f, '>u2', N)  
        #if rounding:
        #    img = np.array(np.round(np.array(img,dtype=np.float)/div),dtype=np.uint16)
        #else:
        #    img = img/int(div)
        #frame = np.reshape(img, nxy)[:, photinfoMask]
    else:
        frame = empty_frame
    #frames.append(frame)
    progress(nframes)
# close file access
f.close()
print(time.time()-s)
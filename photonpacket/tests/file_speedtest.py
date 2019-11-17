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
#%%
import time
folder = r"\\Astrosciema\f\dane\1909 BELL\poszukiwania g2\31_10"+"\\"
file = r"pom_interf_shift70-sr0.dat"
fname= folder + file

#%%
import photonpacket as pp
%time pp.file.read(fname,Nframes=int(10**7),rounding=True)

#%%
import time
import numpy as np
from photonpacket.message import message, progress
from photonpacket.index_raw_file import index_raw_file

t0=time.time()
idxs, photoDim = index_raw_file(fname)
t2=time.time()    
print('len(idxs)=',len(idxs),'t2-t0=',t2-t0)
#%%
import mmap
import numpy as np
from photonpacket.message import message, progress
from struct import unpack
from collections import deque
t0=time.time()
dt_body=np.dtype('>u2')
with open(fname,"rb") as f:
    #mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    b = f.read()    
t1=time.time()      
print('len [MB] b=',len(b)/(1<<20),'t1-t0=',t1-t0)
#%%
t1b=time.time()      
idxs=deque()
#npht=deque()
photons=[]#deque()
i=0
idxs.append(i)
nframes=0
len_b=len(b)
while i<len_b:
    nph,nc=unpack('>ii',b[i:i+8])
    #assert(x0==0&y0==0)
    if i==0:
        photoDim = nc
    i+=8+2*nph*nc
    idxs.append(i)
    npht.append(nph)
    #photons.append(b[i+8:i+8+2*nph*nc])
    nframes+=1
    progress(nframes)
    
t2=time.time()    
print()
print('len(idxs)=',len(idxs),'t2-t1b=',t2-t1b)
#%%
t2b=time.time()    
photons=(b[i+8:i+8+2*nph*nc] for i,nph in zip(idxs,npht))
#npxyz = np.frombuffer(b''.join(photons), dt_body)
npxyz = np.frombuffer(b''.join(b[i+8:i+8+2*nph*nc] for i,nph in zip(idxs,npht)), np.dtype('>u2'))
photons2=np.reshape(npxyz,(len(npxyz)//photoDim,photoDim))[:, :2] 
t3=time.time()    
print('photons2.shape=',photons2.shape,'t2-t2b=',t3-t2b)

#%%
import mmap
import numpy as np
from photonpacket.message import message, progress
t0=time.time()
dt_body=np.dtype('>u2')
with open(fname,"rb") as f:
    #mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    #fb = f.read()
    b = np.frombuffer(f.read(), dt_body)
t1=time.time()      
print('len [MB] b=',len(b)/(1<<20),'t1-t0=',t1-t0)
idxs=[]
i=0
idxs.append(i)
nframes=0
while i<b.shape[0]:
    x0,nph,y0,nc=b[i:i+4]
    #assert(x0==0&y0==0)
    if i==0:
        photoDim = nc
    i+=4+nph*nc
    idxs.append(i)
    nframes+=1
    progress(nframes)
    
t2=time.time()    
print()
print('len(idxs)=',len(idxs),'t2-t0=',t2-t0)
#%%


#%%
import numpy as np
from photonpacket.message import message, progress
t0=time.time()
dt_head=np.dtype('>i4')
dt_body=np.dtype('>u2')
if 1:
    idxs=[]
    photons=[]
    i=0
    idxs.append(i)
    nframes=0

with open(fname,"rb") as f:
    #b = f.read()
    mm = mmap.mmap(f.fileno(), 0,access=mmap.ACCESS_READ)
    
    
    while(True):
        # read number of photons in a frame
        # nxy = (number of photons, information per photon)
        #nxy = py3_fromfile(f, '>i4', 2)
        nxy = np.frombuffer(mm.read(2*dt_head.itemsize), dt_head)
        
        if i == 0:
            photoDim = nxy[1]
            
        # break if file ended or acquired enough frames
        if nxy.size == 0 :
            break
        
        N = nxy[0] * nxy[1]
        nframes += 1
        # read frame data
    
        i += nxy[0]
        idxs.append(i)
        
        if N > 0:
            # TODO: possibility of getting other info about photons,
            #       add dtype attribute basing on rounding parameter
            #       (double or uint) and propagate it to getframeseries            
            #img = py3_fromfile(f, '>u2', N)  
            img = np.frombuffer(mm.read(2*dt_body.itemsize), dt_body)
            photons.append(img)
    
        progress(nframes)
t1=time.time()    
print()
print('len photons b=',len(photons),'t1-t0=',t1-t0)        
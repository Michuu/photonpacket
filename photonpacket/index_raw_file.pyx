# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as np
ctypedef fused DTYPE_t:    
    np.uint16_t
    
ctypedef np.int_t cNDTYPE_t

cimport cython    
    
def index_raw_file(fname):
    from photonpacket.message import progress
    dt_body=np.dtype('>u2')
    with open(fname,"rb") as f:
        #mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        #b = f.read()
        b = np.frombuffer(f.read(), dt_body)
    idxs=[]
    i=0
    idxs.append(i)
    nframes=0
    while i<b.shape[0]:
        x0,nph,y0,nc=b[i:i+4]
        #assert(x0==0&y0==0)
        if i==0:
            photoDim = nc
        i+=nph
        idxs.append(i)
        nframes+=1
        progress(nframes)
    return idxs, photoDim
import numpy as np
cimport numpy as np

cimport cython 

DTYPE = np.uint32
ctypedef np.uint32_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
def coinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2):
    '''
    Generate coincidences between two frames
    
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l, 4], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    for i in range(f1l):
        for j in range(f2l):
            idx = i+f1l*j
            cframe[idx,0] =  frame1[i,0]
            cframe[idx,1] =  frame2[j,0]
            cframe[idx,2] =  frame1[i,1]
            cframe[idx,3] =  frame2[j,1]
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
def coinc3(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, np.ndarray[DTYPE_t, ndim=2] frame3):
    '''
    Generate triple coincidences between three frames
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int f3l = frame3.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l*f3l, 6], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    for i in range(f1l):
        for j in range(f2l):
            for k in range(f3l):
                idx = i+f1l*j+f1l*f2l*k
                cframe[idx,0] =  frame1[i,0]
                cframe[idx,1] =  frame2[j,0]
                cframe[idx,2] =  frame3[k,0]
                cframe[idx,3] =  frame1[i,1]
                cframe[idx,4] =  frame2[j,1]
                cframe[idx,5] =  frame3[k,1]
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
def coinc4(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, np.ndarray[DTYPE_t, ndim=2] frame3, np.ndarray[DTYPE_t, ndim=2] frame4):
    '''
    Generate quadrupole coincidences between four frames
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int f3l = frame3.shape[0]
    cdef int f4l = frame4.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l*f3l*f4l, 8], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int l = 0
    for i in range(f1l):
        for j in range(f2l):
            for k in range(f3l):
                for l in range(f4l):
                    idx = i+f1l*j+f1l*f2l*k+f1l*f2l*f3l*l
                    cframe[idx,0] =  frame1[i,0]
                    cframe[idx,1] =  frame2[j,0]
                    cframe[idx,2] =  frame3[k,0]
                    cframe[idx,3] =  frame4[l,0]
                    cframe[idx,4] =  frame1[i,1]
                    cframe[idx,5] =  frame2[j,1]
                    cframe[idx,6] =  frame3[k,1]
                    cframe[idx,7] =  frame4[l,1]
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)  
def bincoinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[DTYPE_t, ndim=4] hist):
    '''
    Bin coincidences between two frames, adding them to hist
    
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int i = 0
    cdef int j = 0
    for i in range(f1l):
        for j in range(f2l):
            hist[frame1[i,0], frame2[j,0], frame1[i,1], frame2[j,1]] += 1
  
@cython.boundscheck(False)
@cython.wraparound(False)
def coincsd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, 
            signs, shape):
    '''
    Generete coincidences between two frames in sum/difference variables
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l, 2], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if signs[0] == -1:
        shift1 = shape[0]
    if signs[1] == -1:
        shift2 = shape[1]
    for i in range(f1l):
        for j in range(f2l):
            cframe[i+f1l*j,0] =  frame1[i,0] + sign0*frame2[j,0] + shift1
            cframe[i+f1l*j,1] =  frame1[i,1] + sign1*frame2[j,1] + shift2
    return cframe
          
@cython.boundscheck(False)
@cython.wraparound(False)  
def bincoincsd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[DTYPE_t, ndim=2] hist, signs, shape):
    '''
    Bin coincidences in sum/difference variables, adding them to hist
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if sign0 == -1:
        shift1 = shape[0]
    if sign1 == -1:
        shift2 = shape[1]
    for i in range(f1l):
        for j in range(f2l):
            hist[frame1[i,0] + sign0*frame2[j,0] + shift1, frame1[i,1] + sign1*frame2[j,1] + shift2] += 1
            
@cython.boundscheck(False)
@cython.wraparound(False)
def autocoinc(np.ndarray[DTYPE_t, ndim=2] frame):
    '''
    Generate autocoincidences inside a single frame
    
    '''
    cdef int f1l = frame.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*(f1l-1)/2, 4], dtype=DTYPE)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    for i in range(f1l):
        for j in range(f1l):
            if i != j:
                cframe[k,0] =  frame[i,0]
                cframe[k,1] =  frame[j,0]
                cframe[k,2] =  frame[i,1]
                cframe[k,3] =  frame[j,1]
                k += 1
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)  
def binautocoinc(np.ndarray[DTYPE_t, ndim=2] frame, 
             np.ndarray[DTYPE_t, ndim=4] hist):
    '''
    Bin autocoincidences inside a single frame, adding them to hist
    
    '''
    cdef int f1l = frame.shape[0]
    cdef int i = 0
    cdef int j = 0
    for i in range(f1l):
        for j in range(f1l):
            if i != j:
                hist[frame[i,0], frame[j,0], frame[i,1], frame[j,1]] += 1
                
@cython.boundscheck(False)
@cython.wraparound(False)  
def bincount2d(np.ndarray[DTYPE_t, ndim=2] cframe,
             np.ndarray[DTYPE_t, ndim=2] hist):
    '''
    Bin counts with two cooridinates
    
    '''
    cdef int cfl = cframe.shape[0]
    cdef int i = 0
    for i in range(cfl):
            hist[cframe[i,0], cframe[i,1]] += 1
            
@cython.boundscheck(False)
@cython.wraparound(False)  
def bincoinc4sd2(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
                np.ndarray[DTYPE_t, ndim=2] frame3, np.ndarray[DTYPE_t, ndim=2] frame4,
             np.ndarray[DTYPE_t, ndim=2] hist, signs, shape):
    '''
    Bin quad coincidences in total sum/difference variables, adding them to 2D hist
    order = s, i, s, i
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int f3l = frame3.shape[0]
    cdef int f4l = frame4.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int l = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if sign0 == -1:
        shift1 = 2*(shape[0]-1)
    if sign1 == -1:
        shift2 = 2*(shape[1]-1)
    for i in range(f1l):
        for j in range(f2l):
            for k in range(f3l):
                for l in range(f4l):            
                        hist[frame1[i,0] + sign0*frame2[j,0] + frame3[k,0] + sign0*frame4[l,0] + shift1, frame1[i,1] + sign1*frame2[j,1] + frame3[k,1] + sign0*frame4[l,1] + shift2] += 1
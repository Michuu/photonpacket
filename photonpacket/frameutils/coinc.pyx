import numpy as np
cimport numpy as np

cimport cython


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef coinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2):
    '''
    Generate coincidences between two frames

    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int f1d = frame1.shape[1]
    cdef int f2d = frame2.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l, f1d+f2d], dtype=frame1.dtype)
    cdef int i = 0
    cdef int j = 0
    for i in range(f1l):
        for j in range(f2l):
            idx = i+f1l*j
            jdx=0
            for k,l in zip(range(f1d),range(f2d)):
                cframe[idx,jdx] =  frame1[i,k]
                cframe[idx,jdx+1] =  frame2[j,l]
                jdx+=2
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef coinc3(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, np.ndarray[DTYPE_t, ndim=2] frame3):
    '''
    Generate triple coincidences between three frames
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int f3l = frame3.shape[0]
    cdef int f1d = frame1.shape[1]
    cdef int f2d = frame2.shape[2]
    cdef int f3d = frame3.shape[3]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l*f3l, f1d+f2d+f3d], dtype=frame1.dtype)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int l = 0
    cdef int m = 0
    cdef int n = 0
    for i in range(f1l):
        for j in range(f2l):
            for k in range(f3l):
                idx = i+f1l*j+f1l*f2l*k
                jdx=0
                for l,m,n in zip(range(f1d),range(f2d),range(f3d)):
                    cframe[idx,jdx] =  frame1[i,l]
                    cframe[idx,jdx+1] =  frame2[j,m]
                    cframe[idx,jdx+2] =  frame3[k,n]
                    jdx+=3
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef coinc4(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, np.ndarray[DTYPE_t, ndim=2] frame3, np.ndarray[DTYPE_t, ndim=2] frame4):
    '''
    Generate quadrupole coincidences between four frames
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int f3l = frame3.shape[0]
    cdef int f4l = frame4.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l*f3l*f4l, 8], dtype=frame1.dtype)
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
cpdef coinc4_2(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2):
    '''
    Generate quadrupole coincidences between two frames
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l*(f1l-1)*(f2l-1), 8], dtype=frame1.dtype)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int l = 0
    cdef int idx =0
    for i in range(f1l):
        for j in range(f2l):
            for k in range(f1l):
                for l in range(f2l):
                    if i < k and j < l:
                        cframe[idx,0] =  frame1[i,0]
                        cframe[idx,1] =  frame2[j,0]
                        cframe[idx,2] =  frame1[k,0]
                        cframe[idx,3] =  frame2[l,0]
                        cframe[idx,4] =  frame1[i,1]
                        cframe[idx,5] =  frame2[j,1]
                        cframe[idx,6] =  frame1[k,1]
                        cframe[idx,7] =  frame2[l,1]
                        idx += 1
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bincoinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[hist_DTYPE_t, ndim=4] hist):
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
cpdef coincsd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
            signs, shape):
    '''
    Generete coincidences between two frames in sum/difference variables
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*f2l, 2], dtype=frame1.dtype)
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if signs[0] == -1:
        shift1 = shape[0]-1
    if signs[1] == -1:
        shift2 = shape[1]-1
    for i in range(f1l):
        for j in range(f2l):
            cframe[i+f1l*j,0] =  frame1[i,0] + sign0*frame2[j,0] + shift1
            cframe[i+f1l*j,1] =  frame1[i,1] + sign1*frame2[j,1] + shift2
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bincoincsd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape):
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
        shift1 = shape[0]-1
    if sign1 == -1:
        shift2 = shape[1]-1
    for i in range(f1l):
        for j in range(f2l):
            hist[frame1[i,0] + sign0*frame2[j,0] + shift1, frame1[i,1] + sign1*frame2[j,1] + shift2] += 1

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bincoinc_4d_sd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[hist_DTYPE_t, ndim=4] hist, np.ndarray[hist_DTYPE_t, ndim=1] shape):
    '''
    Bin coincidences in sum/difference variables (4 dimensional, sum_y, diff_y=y1-y2, s_x d_x), adding them to  hist
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift3 = 0
    shift1 = shape[0]-1
    shift3 = shape[1]-1
    for i in range(f1l):
        for j in range(f2l):
            hist[
            frame1[i,0] + frame2[j,0],
            frame1[i,0] - frame2[j,0] + shift1,
            frame1[i,1] + frame2[j,1],
            frame1[i,1] - frame2[j,1] + shift3
            ] += 1

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef autocoinc(np.ndarray[DTYPE_t, ndim=2] frame):
    '''
    Generate autocoincidences inside a single frame

    '''
    cdef int f1l = frame.shape[0]
    cdef int f1d = frame.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=2] cframe = np.zeros([f1l*(f1l-1), 2*f1d], dtype=frame.dtype)
    cdef int i = 0
    cdef int j = 0
    cdef int k = 0
    cdef int l = 0
    cdef int idx = 0
    for i in range(f1l):
        for j in range(f1l):
            if i != j:
                jdx=0
                for k,l in zip(range(f1d),range(f1d)):
                    cframe[idx,jdx] =  frame[i,k]
                    cframe[idx,jdx+1] =  frame[j,l]
                    jdx += 2
                idx += 1
    return cframe

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef binautocoinc(np.ndarray[DTYPE_t, ndim=2] frame,
             np.ndarray[hist_DTYPE_t, ndim=4] hist):
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
cpdef binautocoincsd(np.ndarray[DTYPE_t, ndim=2] frame1,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape):
    '''
    Bin autocoincidences in sum/difference variables, adding them to hist
    '''
    cdef int f1l = frame1.shape[0]
    cdef int i = 0
    cdef int j = 0
    cdef int shift1 = 0
    cdef int shift2 = 0
    cdef int sign0 = signs[0]
    cdef int sign1 = signs[1]
    if sign0 == -1:
        shift1 = (hist.shape[0]+1)//2-1
    if sign1 == -1:
        shift2 = (hist.shape[1]+1)//2-1
    for i in range(f1l):
        for j in range(f1l):
            if i != j:
                coordy = frame1[i,0] + sign0*frame1[j,0] + shift1 
                coordx = frame1[i,1] + sign1*frame1[j,1] + shift2
                if (coordy >= hist.shape[0] or coordx >= hist.shape[1] or coordy < 0 or coordx < 0): continue
                hist[coordy,coordx] += 1

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bincount2d(np.ndarray[DTYPE_t, ndim=2] cframe,
             np.ndarray[hist_DTYPE_t, ndim=2] hist):
    '''
    Bin counts with two cooridinates

    '''
    cdef int cfl = cframe.shape[0]
    cdef int i = 0
    for i in range(cfl):
            hist[cframe[i,0], cframe[i,1]] += 1

@cython.boundscheck(False)
@cython.wraparound(False)  
cpdef bincoinc4sd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape):
    '''
    Bin quad coincidences from only two frames in total sum/difference variables, adding them to 2D hist
    order = s, i, s, i
    '''
    cdef int f1l = frame1.shape[0]
    cdef int f2l = frame2.shape[0]
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
            for k in range(f1l):
                for l in range(f2l):
                    if i < k and j < l:
                        hist[frame1[i,0] + sign0*frame2[j,0] + \
                        frame1[k,0] + sign0*frame2[l,0] + shift1, \
                        frame1[i,1] + sign1*frame2[j,1] + \
                        frame1[k,1] + sign1*frame2[l,1] + shift2] += 1

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bincoinc4sd2(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
                np.ndarray[DTYPE_t, ndim=2] frame3, np.ndarray[DTYPE_t, ndim=2] frame4,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape):
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
                        hist[frame1[i,0] + sign0*frame2[j,0] + frame3[k,0] + sign0*frame4[l,0] + shift1, frame1[i,1] + sign1*frame2[j,1] + frame3[k,1] + sign1*frame4[l,1] + shift2] += 1
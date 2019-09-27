import numpy as np
from photonpacket.message import progress
cimport numpy as np
from coinc cimport bincoinc, bincoincsd, bincount2d, coinc, bincoinc4sd, \
bincoinc4sd2,  binautocoincsd, coinc4, coinc4_2, autocoinc, coinc3
cimport cython

ctypedef fused DTYPE_t:
    np.uint8_t
    np.uint16_t
    np.uint32_t

ctypedef fused accum_DTYPE_t:
    np.uint8_t
    np.uint16_t
    np.uint32_t

@cython.boundscheck(False)
@cython.wraparound(False)
def concat_coinc(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                 np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2):
    cdef int i = 0
    cdef list cframes = []
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            cframes.append(coinc(frame1, frame2))
    return np.concatenate(cframes)

@cython.boundscheck(False)
@cython.wraparound(False)
def concat_autocoinc(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1):
    cdef int i = 0
    cdef list cframes = []
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            cframes.append(autocoinc(frame1))
    return np.concatenate(cframes)

@cython.boundscheck(False)
@cython.wraparound(False)
def concat_coinc4(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                       np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2,
                       np.ndarray[DTYPE_t, ndim=2] photons3, np.ndarray[np.int32_t, ndim=1] idxs3,
                       np.ndarray[DTYPE_t, ndim=2] photons4, np.ndarray[np.int32_t, ndim=1] idxs4, constr=None):
    cdef list cframes = []
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    cdef np.ndarray[DTYPE_t, ndim=2] frame3
    cdef np.ndarray[DTYPE_t, ndim=2] frame4
    cdef np.ndarray[np.uint8_t, ndim=1] mask
    cdef np.ndarray[DTYPE_t, ndim=2] c4
    cdef int i = 0
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1] and idxs3[i] != idxs3[i+1] and idxs4[i] != idxs4[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            frame3 = photons3[idxs3[i]:idxs3[i+1]]
            frame4 = photons4[idxs4[i]:idxs4[i+1]]
            if constr is None:
                cframes.append(coinc4(frame1, frame2, frame3, frame4))
            else:
                c4 = coinc4(frame1, frame2, frame3, frame4)
                mask = constr(c4)
                cframes.append(c4[mask])
    return np.concatenate(cframes)        

@cython.boundscheck(False)
@cython.wraparound(False)
def concat_coinc3(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                       np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2,
                       np.ndarray[DTYPE_t, ndim=2] photons3, np.ndarray[np.int32_t, ndim=1] idxs3, constr=None):
    cdef list cframes = []
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    cdef np.ndarray[DTYPE_t, ndim=2] frame3
    cdef np.ndarray[np.uint8_t, ndim=1] mask
    cdef np.ndarray[DTYPE_t, ndim=2] c3
    cdef int i = 0
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1] and idxs3[i] != idxs3[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            frame3 = photons3[idxs3[i]:idxs3[i+1]]
            if constr is None:
                cframes.append(coinc3(frame1, frame2, frame3))
            else:
                c3 = coinc3(frame1, frame2, frame3)
                mask = constr(c3)
                cframes.append(c3[mask])
    return np.concatenate(cframes)

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoinc(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                   np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2,
                                                         np.ndarray[accum_DTYPE_t, ndim=4] accum):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            bincoinc(frame1, frame2, accum)

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoincsd(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                     np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2,
                                             np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            bincoincsd(frame1, frame2, accum, signs, shape)

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoinc4sd(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                      np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2,
                                             np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            bincoinc4sd(frame1, frame2, accum, signs, shape)

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoinc4sd2(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                       np.ndarray[DTYPE_t, ndim=2] photons2, np.ndarray[np.int32_t, ndim=1] idxs2,
                       np.ndarray[DTYPE_t, ndim=2] photons3, np.ndarray[np.int32_t, ndim=1] idxs3,
                       np.ndarray[DTYPE_t, ndim=2] photons4, np.ndarray[np.int32_t, ndim=1] idxs4,
                                             np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    cdef np.ndarray[DTYPE_t, ndim=2] frame3
    cdef np.ndarray[DTYPE_t, ndim=2] frame4
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1] and idxs2[i] != idxs2[i+1] and idxs3[i] != idxs3[i+1] and idxs4[i] != idxs4[i+1]:
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            frame2 = photons2[idxs2[i]:idxs2[i+1]]
            frame3 = photons1[idxs3[i]:idxs3[i+1]]
            frame4 = photons2[idxs4[i]:idxs4[i+1]]
            bincoinc4sd2(frame1, frame2, frame3, frame4, accum, signs, shape)

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_binautocoincsd(np.ndarray[DTYPE_t, ndim=2] photons1, np.ndarray[np.int32_t, ndim=1] idxs1,
                                             np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape, **kwargs):
    cdef bint mincondition = False
    cdef bint maxcondition = False
    cdef int minphotnumber = 0
    cdef int maxphotnumber = 0
    
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    
    if 'minphotons' in kwargs:
        mincondition = True
        minphotnumber = kwargs['minphotons']
    if 'maxphotons' in kwargs:
        maxcondition = True
        maxphotnumber = kwargs['maxphotons']
    
    for i in xrange(len(idxs1)-1):
        progress(i)
        if idxs1[i] != idxs1[i+1]:
            if mincondition:
                if idxs1[i+1]-idxs1[i] < minphotnumber:
                    continue
            if maxcondition:
                if idxs1[i+1]-idxs1[i] > maxphotnumber:
                    continue
            frame1 = photons1[idxs1[i]:idxs1[i+1]]
            binautocoincsd(frame1, accum, signs, shape)
        
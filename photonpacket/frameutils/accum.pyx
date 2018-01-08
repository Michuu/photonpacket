from itertools import izip
import numpy as np
from photonpacket.message import progress
cimport numpy as np
from coinc cimport bincoinc, bincoincsd, bincount2d, coinc, bincoinc4sd2, binautocoincsd
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
def concat_coinc(list frames1, list frames2, np.ndarray[DTYPE_t, ndim=2] dtype):
    cdef int i = 0
    cdef list cframes = []
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for frame1, frame2 in izip(frames1, frames2):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[1] != 0:
            cframes.append(coinc(frame1, frame2))
        i += 1
    return np.concatenate(cframes)

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoinc(list frames1, list frames2, np.ndarray[accum_DTYPE_t, ndim=4] accum, np.ndarray[DTYPE_t, ndim=2] dtype):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for frame1, frame2 in izip(frames1, frames2):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[1] != 0:
            bincoinc(frame1, frame2, accum)
        i += 1

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoincsd(list frames1, list frames2, np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape, np.ndarray[DTYPE_t, ndim=2] dtype):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    for frame1, frame2 in izip(frames1, frames2):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[1] != 0:
            bincoincsd(frame1, frame2, accum, signs, shape)
        i += 1

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_bincoinc4sd2(list frames1, list frames2, list frames3, list frames4, np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape, np.ndarray[DTYPE_t, ndim=2] dtype):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    cdef np.ndarray[DTYPE_t, ndim=2] frame2
    cdef np.ndarray[DTYPE_t, ndim=2] frame3
    cdef np.ndarray[DTYPE_t, ndim=2] frame4
    for frame1, frame2, frame3, frame4 in izip(frames1, frames2, frames3, frames4):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[0] != 0 and frame3.shape[0] != 0 and frame4.shape[0] != 0:
            bincoinc4sd2(frame1, frame2, frame3, frame4, accum, signs, shape)
        i += 1

@cython.boundscheck(False)
@cython.wraparound(False)
def accum_binautocoincsd(list frames1, np.ndarray[accum_DTYPE_t, ndim=2] accum, signs, shape, np.ndarray[DTYPE_t, ndim=2] dtype):
    cdef int i = 0
    cdef np.ndarray[DTYPE_t, ndim=2] frame1
    for frame1 in frames1:
        progress(i)
        if frame1.shape[0] != 0:
            binautocoincsd(frame1, accum, signs, shape)
        i += 1
import numpy as np
cimport numpy as np


ctypedef np.uint8_t DTYPE8_t
ctypedef np.uint16_t DTYPE16_t
ctypedef np.uint32_t DTYPE32_t
ctypedef np.int_t cNDTYPE_t

cimport cython

__all__ = ['arraysplit']

@cython.boundscheck(False)
@cython.wraparound(False)

def arraysplit8(np.ndarray[DTYPE8_t, ndim=2] ary, np.ndarray[cNDTYPE_t, ndim=1] indices_or_sections):
    cdef int Ntotal = ary.shape[0]
    cdef int i
    cdef int st
    cdef int end
    cdef list sub_arys = [] 
    A = sub_arys.append
    cdef int Nsections = indices_or_sections.shape[0] + 1
    cdef list div_points = [0] + list(indices_or_sections) + [Ntotal]
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i+1]
        A(ary[st:end])
    return sub_arys

@cython.boundscheck(False)
@cython.wraparound(False)

def arraysplit16(np.ndarray[DTYPE16_t, ndim=2] ary, np.ndarray[cNDTYPE_t, ndim=1] indices_or_sections):
    cdef int Ntotal = ary.shape[0]
    cdef int i
    cdef int st
    cdef int end
    cdef list sub_arys = [] 
    A = sub_arys.append
    cdef int Nsections = indices_or_sections.shape[0] + 1
    cdef list div_points = [0] + list(indices_or_sections) + [Ntotal]
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i+1]
        A(ary[st:end])
    return sub_arys

@cython.boundscheck(False)
@cython.wraparound(False)

def arraysplit32(np.ndarray[DTYPE32_t, ndim=2] ary, np.ndarray[cNDTYPE_t, ndim=1] indices_or_sections):
    cdef int Ntotal = ary.shape[0]
    cdef int i
    cdef int st
    cdef int end
    cdef list sub_arys = [] 
    A = sub_arys.append
    cdef int Nsections = indices_or_sections.shape[0] + 1
    cdef list div_points = [0] + list(indices_or_sections) + [Ntotal]
    for i in range(Nsections):
        st = div_points[i]
        end = div_points[i+1]
        A(ary[st:end])
    return sub_arys

@cython.boundscheck(False)
@cython.wraparound(False)

def arraysplit(np.ndarray ary, np.ndarray[cNDTYPE_t, ndim=1] indices_or_sections):
    '''
    Faster version of :func:`numpy.array_split`
    
    Parameters
    ---------
    ary : ndarray
        Array to be divided into sub-arrays.
    indices_or_sections : int or 1-D array
        If indices_or_sections is an integer, N, the array will be divided into N equal arrays along axis. If such a split is not possible, an error is raised.
        If indices_or_sections is a 1-D array of sorted integers, the entries indicate where along axis the array is split. For example, [2, 3] would, for axis=0, result in
        ary[:2]
        ary[2:3]
        ary[3:]
        If an index exceeds the dimension of the array along axis, an empty sub-array is returned correspondingly.

    Returns
    ---------    
    sub-arrays : list of ndarrays
        A list of sub-arrays.

    Raises
    --------- 
    ValueError
        If ary dtype is not supported.
    '''
    if ary.dtype == np.uint8:
        return arraysplit8(ary, indices_or_sections)
    elif ary.dtype == np.uint16:
        return arraysplit16(ary, indices_or_sections)
    elif ary.dtype == np.uint32:
        return arraysplit32(ary, indices_or_sections)
    else:
        raise ValueError("dtype {0} not supported".format(ary.dtype))
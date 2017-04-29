import numpy as np
cimport numpy as np


ctypedef np.uint32_t DTYPE_t
ctypedef np.int_t cNDTYPE_t

cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
def arraysplit(np.ndarray[DTYPE_t, ndim=2] ary, np.ndarray[cNDTYPE_t, ndim=1] indices_or_sections):
    '''
    Faster version of :func:`numpy.array_split`
    
    
    '''
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
        
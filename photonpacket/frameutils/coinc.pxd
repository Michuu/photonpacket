import numpy as np
cimport numpy as np

cimport cython

ctypedef fused DTYPE_t:
    np.uint8_t
    np.uint16_t
    np.uint32_t

ctypedef fused hist_DTYPE_t:
    np.uint8_t
    np.uint16_t
    np.uint32_t


cpdef coinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2)
cpdef coinc3(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, np.ndarray[DTYPE_t, ndim=2] frame3)
cpdef coinc4(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2, np.ndarray[DTYPE_t, ndim=2] frame3, np.ndarray[DTYPE_t, ndim=2] frame4)
cpdef bincoinc(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[hist_DTYPE_t, ndim=4] hist)
cpdef coincsd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
            signs, shape)
cpdef bincoincsd(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape)
cpdef autocoinc(np.ndarray[DTYPE_t, ndim=2] frame)
cpdef binautocoinc(np.ndarray[DTYPE_t, ndim=2] frame,
             np.ndarray[hist_DTYPE_t, ndim=4] hist)
cpdef binautocoincsd(np.ndarray[DTYPE_t, ndim=2] frame1,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape)
cpdef bincount2d(np.ndarray[DTYPE_t, ndim=2] cframe,
             np.ndarray[hist_DTYPE_t, ndim=2] hist)
cpdef bincoinc4sd2(np.ndarray[DTYPE_t, ndim=2] frame1, np.ndarray[DTYPE_t, ndim=2] frame2,
                np.ndarray[DTYPE_t, ndim=2] frame3, np.ndarray[DTYPE_t, ndim=2] frame4,
             np.ndarray[hist_DTYPE_t, ndim=2] hist, signs, shape)
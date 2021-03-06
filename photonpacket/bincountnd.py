# -*- coding: utf-8 -*-
import numpy as np

def bincountnd(array, shape):
    '''
    Multidimensional histogram

    Parameters
    ---------
    array : :class:`numpy.ndarray`
            2D array, first dimension being the coordinates, second subsequent counts

    shape : tuple of ints
            list of sizes of dimensions

    Returns
    ----------
    histogram : :class:`numpy.ndarray`
            histogram of counts

    See Also
    ----------

    Notes
    ----------
    The behaviour of this function mimics :func:`numpy.bincount` in many dimensions.

    References
    ----------

    Examples
    ----------

    '''
    # sorted shape
    aux_shape = np.sort(shape)[::-1]
    # sorted mask selector
    sel = np.argsort(shape)[::-1]
    # flatten output histogram
    flat_array = np.zeros(shape=array.shape[0], dtype=np.int32)
    # initial exponent
    exp = 1
    # sorted data array
    array = np.array(array[:, sel], dtype=np.uint32)
    # for each dimension
    for dim, size in enumerate(aux_shape):
        # generate flat data array
        flat_array += array[:, dim] * exp
        # increase exponent
        exp = exp * size
    # accumulate counts
    accum = np.bincount(flat_array, minlength=np.prod(aux_shape))
    # reshape to size
    # we are using Fortran style indexing
    # first index changing fastest
    accum = np.reshape(accum, aux_shape, 'F')
    # re-sort
    for i in np.arange(np.max(sel)):
        j = sel[i]
        accum = accum.swapaxes(i, j)
    return accum

def bincount2d(array, shape):
    xe = np.arange(0, shape[0]+1)
    ye = np.arange(0, shape[1]+1)
    H, X, Y = np.histogram2d(array[:, 0], array[:, 1], bins=[xe, ye])
    return H

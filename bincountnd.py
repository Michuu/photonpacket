# -*- coding: utf-8 -*-
import numpy as np

def bincountnd(array, shape):
    aux_shape = np.sort(shape)[::-1]
    sel = np.argsort(shape)[::-1]
    flat_array = np.zeros(shape=array.shape[0],dtype=np.uint16)
    exp = 1
    array = array[:,sel]
    for dim, size in enumerate(aux_shape):
        flat_array = flat_array + array[:,dim] * exp
        exp = exp * size
    accum = np.bincount(flat_array, minlength = np.prod(aux_shape))
    return np.reshape(accum,shape)
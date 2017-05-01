import numpy as np
from scipy.signal import convolve2d
from bincountnd import bincountnd
from message import message, progress
from collections import deque
from frameutils.coinc import bincoinc, bincoincsd, bincount2d, coinc

accumtype = np.uint32

def accumframes(fs):
    '''
    Accumulate photon through all frames. 
    Wrapper for :func:`photonpacket.frameseries.accumframes`
    
    Parameters
    ----------
    fs : :class:`photonpacket.frameseries`
            Series of photon frames
            
    Returns
    ---------
    accum : :class:`numpy.ndarray`
        photon counts histogram
    
    '''
    return fs.accumframes()

def accumcoinc(fs1, fs2):
    '''
    Accumulate coincidences into 4D matrix
    
    Parameters
    ----------
    fs1 : :class:`photonpacket.frameseries`
            Series of photon frames
            
    fs2 : :class:`photonpacket.frameseries`
            Series of photon frames
            
    signs : tuple of two booleans
            Signs
            
    method : bincount or accum
            Method
            
    Returns
    ----------
    coinchist : :class:`numpy.ndarray`
    
    See Also
    ----------
    
    Notes
    ----------
    
    Examples
    ----------
    '''
    i = 0
    accum = np.zeros(shape=(fs1.shape[0],fs2.shape[0],
                          fs1.shape[1],fs2.shape[1]), dtype=accumtype)
    for frame1, frame2 in zip(fs1.frames, fs2.frames):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[1] != 0:
            bincoinc(frame1, frame2, accum)
        i += 1
    return accum  

def accumcoinc2d(fs1, fs2, axis=0, constr=None):
    '''
    Coincidences map for one of the dimensions
    '''
    i = 0
    accum = np.zeros(shape=(fs1.shape[axis],fs2.shape[axis]), dtype=accumtype)
    cframes = []
    A = cframes.append
    for frame1, frame2 in zip(fs1.frames, fs2.frames):
        if frame1.shape[0] != 0 and frame2.shape[1] != 0:
            A(coinc(frame1, frame2))
        i += 1
    cframes = np.concatenate(cframes)
    if constr is not None:
        mask = constr(cframes.copy())
        bincount2d(cframes.take([2*axis, 2*axis+1], axis=1)[mask], accum)
    else:
        bincount2d(cframes.take([2*axis, 2*axis+1], axis=1), accum)
    return accum

def coinchist(fs1, fs2, signs):
    '''
    Coincidence histogram in terms of sum/differnce variables
    
    Parameters
    ----------
    fs1 : :class:`photonpacket.frameseries`
        
    fs2 : :class:`photonpacket.frameseries`
        
    signs : 
        
    Returns
    ----------
    
    See Also
    ----------
    
    Notes
    ----------
    
    Examples
    ----------
    '''
    i = 0
    shape = (fs1.shape[0]+fs2.shape[0]-1, fs1.shape[1]+fs2.shape[1]-1)
    accum = np.zeros(shape, dtype=accumtype)
    for frame1, frame2 in zip(fs1.frames, fs2.frames):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[0] != 0:
            bincoincsd(frame1, frame2, accum, signs, fs2.shape)
        i += 1
    return accum


def acchist(h1, h2, signs, **kwargs):
    '''
    Accidential coincidences histogram in terms of sum/differnce variables
    
    Parameters
    ----------
    h1 : :class:`numpy.ndarray`
        first photon counts histogram
        
    h2 : :class:`numpy.ndarray`
        second photon counts histogram
        
    signs : tuple of booleans
        
    Nframes : int
        number of frames
        
    Returns
    ----------
    
    See Also
    ----------
    
    Notes
    ----------
    
    Examples
    ----------
    '''
    if 'Nframes' in kwargs:
        div = float(kwargs['Nframes'])
    else:
        div = 1.0
    if signs[0] == -1:
        h2 = np.flip(h2, axis=0)
    if signs[1] == -1:
        h2 = np.flip(h2, axis=1)
    return convolve2d(h1, h2)/div


def acccoinc(h1, h2, axis=0, constr=None):
    '''
    Accidental coincidences map for one of the dimensions
    '''
    acc = np.zeros((h1.shape[axis], h2.shape[axis]))
    for v1 in range(h1.shape[axis]):
        for v2 in range(h2.shape[axis]):
            if constr is not None:
                pass
            else:
                if axis == 1:
                    acc += np.outer(h1[v1, :], h2[v2, :])
                else:
                    acc += np.outer(h1[:, v1], h2[:, v2])
    return acc
    

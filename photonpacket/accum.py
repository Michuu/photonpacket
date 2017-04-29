import numpy as np
from scipy.signal import convolve2d
from bincountnd import bincountnd
from message import message, progress
from collections import deque
from frameutils.coinc import bincoinc, bincoinc2d

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
    Accumulate coincidences
    
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
    accum = np.zeros(shape=(fs1.shape[0],fs1.shape[0],
                          fs1.shape[1],fs1.shape[1]), dtype=accumtype)
    for frame1, frame2 in zip(fs1.frames, fs2.frames):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[1] != 0:
            bincoinc(frame1, frame2, accum)
        i += 1
    return accum  

def coinchist(fs1, fs2, signs):
    '''
    Obtain coincidence histogram
    
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
    shape = (fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1)
    accum = np.zeros(shape, dtype=accumtype)
    for frame1, frame2 in zip(fs1.frames, fs2.frames):
        progress(i)
        if frame1.shape[0] != 0 and frame2.shape[0] != 0:
            bincoinc2d(frame1, frame2, accum, signs, fs2.shape)
        i += 1
    return accum
    

def acchist(h1,h2,signs,**kwargs):
    '''
    Obtain accidential coincidences histogram
    
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
          h2=np.flip(h2,axis=0)
    if signs[1] == -1:
          h2=np.flip(h2,axis=1)
    return convolve2d(h1,h2)/div
    

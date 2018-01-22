import numpy as np
from scipy.signal import convolve2d
from bincountnd import bincountnd
from message import message, progress
from collections import deque
from frameutils.coinc import bincount2d
from frameutils.accum import accum_bincoinc, concat_coinc, accum_bincoincsd,\
     accum_bincoinc4sd, accum_bincoinc4sd2, accum_binautocoincsd, concat_autocoinc
import itertools as it

accumtype = np.uint16

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
    accum = np.zeros(shape=(fs1.shape[0],fs2.shape[0],
                          fs1.shape[1],fs2.shape[1]), dtype=accumtype)
    accum_bincoinc(fs1.photons, fs1.idxs, fs2.photons, fs2.idxs, accum)
    return accum

def accumcoinc2d(fs1, fs2, axis=0, constr=None):
    '''
    Coincidences map for one of the dimensions
    '''
    accum = np.zeros(shape=(fs1.shape[axis],fs2.shape[axis]), dtype=np.uint16)
    cframes = concat_coinc(fs1.photons, fs1.idxs, fs2.photons, fs2.idxs)
    if constr is not None:
        mask = constr(cframes.copy())
        bincount2d(cframes.take([2*axis, 2*axis+1], axis=1)[mask], accum)
    else:
        bincount2d(cframes.take([2*axis, 2*axis+1], axis=1), accum)
    return accum

def accumautocoinc2d(fs1, axis=0, constr=None):
    '''
    Coincidences map for one of the dimensions
    '''
    accum = np.zeros(shape=(fs1.shape[axis],fs1.shape[axis]), dtype=np.uint16)
    cframes = concat_autocoinc(fs1.photons, fs1.idxs)
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
    shape = (fs1.shape[0]+fs2.shape[0]-1, fs1.shape[1]+fs2.shape[1]-1)
    accum = np.zeros(shape, dtype=accumtype)
    accum_bincoincsd(fs1.photons, fs1.idxs, fs2.photons, fs2.idxs,
                     accum, signs, fs2.shape)
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
    iaxis = int(not axis)
    acc = np.zeros((h1.shape[iaxis], h2.shape[iaxis]))
    for v1 in range(h1.shape[iaxis]):
        for v2 in range(h2.shape[iaxis]):
            if constr is not None:
                pass
            else:
                if axis == 1:
                    acc += np.outer(h1[v1, :], h2[v2, :])
                else:
                    acc += np.outer(h1[:, v1], h2[:, v2])
    return acc

def coinchist4(*args):
    '''
    Coincidence quad histogram in terms of sum/differnce variables of four-fold coincidences

    Parameters
    ----------
    fs1 : :class:`photonpacket.frameseries`

    fs2 : :class:`photonpacket.frameseries`

    fs3 : :class:`photonpacket.frameseries`

    fs4 : :class:`photonpacket.frameseries`

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
    if len(args) == 5:
        # use accum_bincoinc4sd2
        fs1=args[0]
        fs2=args[1]
        fs3=args[2]
        fs4=args[3]
        signs=args[4]
        shape = (fs1.shape[0]+fs2.shape[0]+fs3.shape[0]+fs4.shape[0]-3,
                 fs1.shape[1]+fs2.shape[1]+fs3.shape[1]+fs4.shape[1]-3)
        accum = np.zeros(shape, dtype=accumtype)
        accum_bincoinc4sd2(fs1.photons, fs1.idxs, fs2.photons, fs2.idxs,
                           fs3.photons, fs3.idxs, fs4.photons, fs4.idxs,
                           accum, signs, fs2.shape)
        return accum
    elif len(args)==3:
        #use accum_bincoinc4sd
        fs1=args[0]
        fs2=args[1]
        signs=args[2]
        shape = (2 * fs1.shape[0] + 2 * fs2.shape[0] - 3,
                 2 * fs1.shape[1] + 2 * fs2.shape[1] - 3)
        accum = np.zeros(shape, dtype=accumtype)
        accum_bincoinc4sd(fs1.photons, fs1.idxs, fs2.photons, fs2.idxs, accum,
                          signs, fs2.shape)
        return accum
    else:
        #error
        return -1
        
def autocoinchist(fs1, signs):
    '''
    Autocoincidence histogram in terms of sum/differnce variables

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
    shape = (2*fs1.shape[0]-1, 2*fs1.shape[1]-1)
    accum = np.zeros(shape, dtype=accumtype)
    accum_binautocoincsd(fs1.photons, fs1.idxs, accum, signs, fs1.shape)
    return accum

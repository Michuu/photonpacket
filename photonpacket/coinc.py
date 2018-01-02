import numpy as np
import coinc8
import coinc16
import coinc32


def coinc(frame1, frame2):
    '''
    Generate coincidences between two frames

    '''
    if frame1.dtype != frame2.dtype:
        raise ValueError("frame2 dtype {0} differs from frame2 dtype {1}".format(frame1.dtype, frame2.dtype))
    elif frame1.dtype == np.uint8:
        return coinc8.coinc(frame1, frame2)
    elif frame1.dtype == np.uint16:
        return coinc16.coinc(frame1, frame2)
    elif frame1.dtype == np.uint32:
        return coinc32.coinc(frame1, frame2)
    else:
        raise ValueError("dtype {0} not supported".format(frame1.dtype))

def coinc3(frame1, frame2, frame3):
    '''
    Generate triple coincidences between three frames
    '''
    if not (frame1.dtype == frame2.dtype == frame3.dtype):
        raise ValueError("frames differ in dtypes")
    elif frame1.dtype == np.uint8:
        return coinc8.coinc3(frame1, frame2, frame3)
    elif frame1.dtype == np.uint16:
        return coinc16.coinc3(frame1, frame2, frame3)
    elif frame1.dtype == np.uint32:
        return coinc32.coinc3(frame1, frame2, frame3)
    else:
        raise ValueError("dtype {0} not supported".format(frame1.dtype))

def coinc4(frame1, frame2, frame3, frame4):
    '''
    Generate quadrupole coincidences between four frames
    '''
    if not (frame1.dtype == frame2.dtype == frame3.dtype == frame4.dtype):
        raise ValueError("frames differ in dtypes")
    elif frame1.dtype == np.uint8:
        return coinc8.coinc4(frame1, frame2, frame3, frame4)
    elif frame1.dtype == np.uint16:
        return coinc16.coinc4(frame1, frame2, frame3, frame4)
    elif frame1.dtype == np.uint32:
        return coinc32.coinc4(frame1, frame2, frame3, frame4)
    else:
        raise ValueError("dtype {0} not supported".format(frame1.dtype))

def bincoinc(frame1, frame2, hist):
    '''
    Bin coincidences between two frames, adding them to hist

    '''
    if not (frame1.dtype == frame2.dtype == hist.dtype):
        raise ValueError("inputs differ in dtypes")
    elif frame1.dtype == np.uint8:
        return coinc8.bincoinc(frame1, frame2, hist)
    elif frame1.dtype == np.uint16:
        return coinc16.bincoinc(frame1, frame2, hist)
    elif frame1.dtype == np.uint32:
        return coinc32.bincoinc(frame1, frame2, hist)
    else:
        raise ValueError("dtype {0} not supported".format(frame1.dtype))

def coincsd(frame1, frame2, signs, shape):
    '''
    Generete coincidences between two frames in sum/difference variables
    '''
    if not (frame1.dtype == frame2.dtype):
        raise ValueError("frames differ in dtypes")
    elif frame1.dtype == np.uint8:
        return coinc8.coincsd(frame1, frame2, signs, shape)
    elif frame1.dtype == np.uint16:
        return coinc16.coincsd(frame1, frame2, signs, shape)
    elif frame1.dtype == np.uint32:
        return coinc32.coincsd(frame1, frame2, signs, shape)
    else:
        raise ValueError("dtype {0} not supported".format(frame1.dtype))

def bincoincsd(frame1, frame2, hist, signs, shape):
    '''
    Bin coincidences in sum/difference variables, adding them to hist
    '''
    if not (frame1.dtype == frame2.dtype == hist.dtype):
        raise ValueError("frames differ in dtypes")
    elif frame1.dtype == np.uint8:
        return coinc8.bincoincsd(frame1, frame2, hist, signs, shape)
    elif frame1.dtype == np.uint16:
        return coinc16.bincoincsd(frame1, frame2, hist, signs, shape)
    elif frame1.dtype == np.uint32:
        return coinc32.bincoincsd(frame1, frame2, hist, signs, shape)
    else:
        raise ValueError("dtype {0} not supported".format(frame1.dtype))

def autocoinc(frame):
    '''
    Generate autocoincidences inside a single frame

    '''
    if frame.dtype == np.uint8:
        return coinc8.autocoinc(frame)
    elif frame.dtype == np.uint16:
        return coinc16.autocoinc(frame)
    elif frame.dtype == np.uint32:
        return coinc32.autocoinc(frame)
    else:
        raise ValueError("dtype {0} not supported".format(frame.dtype))

def binautocoinc(frame, hist):
    '''
    Bin autocoincidences inside a single frame, adding them to hist

    '''
    if not (frame.dtype == hist.dtype):
        raise ValueError("inputs differ in dtypes")
    elif frame.dtype == np.uint8:
        return coinc8.binautocoinc(frame, hist)
    elif frame.dtype == np.uint16:
        return coinc16.binautocoinc(frame, hist)
    elif frame.dtype == np.uint32:
        return coinc32.binautocoinc(frame, hist)
    else:
        raise ValueError("dtype {0} not supported".format(frame.dtype))

def bincount2d(frame, hist):
    '''
    Bin counts with two cooridinates

    '''
    if not (frame.dtype == hist.dtype):
        raise ValueError("inputs differ in dtypes")
    elif frame.dtype == np.uint8:
        return coinc8.bincount2d(frame, hist)
    elif frame.dtype == np.uint16:
        return coinc16.bincount2d(frame, hist)
    elif frame.dtype == np.uint32:
        return coinc32.bincount2d(frame, hist)
    else:
        raise ValueError("dtype {0} not supported".format(frame.dtype))
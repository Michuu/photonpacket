import numpy as np
import frameutils.coinc8 as coinc8
import frameutils.coinc16 as coinc16
import frameutils.coinc32 as coinc32

def detectdtype(numfargs):
    def detectdtype_(func):
        def coincfun(*args):
            for i in range(numfargs):
                if i==0:
                    mdt = args[i].dtype
                else:
                    if args[i].dtype != mdt:
                        raise ValueError("arg1 dtype {0} differs from arg{1} dtype {2}".format(args[0].dtype, i+1, args[i].dtype))
                        return -1
            if args[0].dtype == np.uint8:
                return getattr(coinc8, func.__name__)(*args)
            elif args[0].dtype == np.uint16:
                return getattr(coinc16, func.__name__)(*args)
            elif args[0].dtype == np.uint32:
                return getattr(coinc32, func.__name__)(*args)
            else:
                raise ValueError("dtype {0} not supported".format(args[0].dtype))
        return coincfun
    return detectdtype_
        
@detectdtype(2)    
def coinc(frame1, frame2):
    '''
    Generate coincidences between two frames

    '''

@detectdtype(3)
def coinc3(frame1, frame2, frame3):
    '''
    Generate triple coincidences between three frames
    '''

@detectdtype(4)
def coinc4(frame1, frame2, frame3, frame4):
    '''
    Generate quadrupole coincidences between four frames
    '''

@detectdtype(2)
def bincoinc(frame1, frame2, hist):
    '''
    Bin coincidences between two frames, adding them to hist

    '''

@detectdtype(2)
def coincsd(frame1, frame2, signs, shape):
    '''
    Generete coincidences between two frames in sum/difference variables
    '''

@detectdtype(2)
def bincoincsd(frame1, frame2, hist, signs, shape):
    '''
    Bin coincidences in sum/difference variables, adding them to hist
    '''

@detectdtype(1)
def autocoinc(frame):
    '''
    Generate autocoincidences inside a single frame

    '''

@detectdtype(1)
def binautocoinc(frame, hist):
    '''
    Bin autocoincidences inside a single frame, adding them to hist

    '''

@detectdtype(1)    
def binautocoincsd(frame, hist, signs, shape):
    '''
    Bin autocoincidences in sum/difference variables, adding them to hist
    '''
    
@detectdtype(1)
def bincount2d(frame, hist):
    '''
    Bin counts with two cooridinates

    '''
   
@detectdtype(2)     
def bincoinc4sd(frame1, frame2, hist, signs, shape):
    '''
    Bin quad coincidences in total sum/difference variables, adding them to 2D hist
    order = s, i, s, i

    '''
    
@detectdtype(4)     
def bincoinc4sd2(frame1, frame2, frame3, frame4, hist, signs, shape):
    '''
    Bin quad coincidences in total sum/difference variables, adding them to 2D hist
    order = s, i, s, i

    '''
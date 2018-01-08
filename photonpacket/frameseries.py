import numpy as np
from bincountnd import bincountnd
from scipy.spatial import KDTree
from scipy.signal import resample
from arraysplit import array_split
from matplotlib import pyplot as plt
from copy import deepcopy
from message import message, progress

from coinc import binautocoinc
from frameutils.arraysplit2 import arraysplit

try:
    import cPickle as pickle
except:
    import pickle

# main frameseries class

class frameseries:
    frames = np.array([], dtype=np.object)
    N = np.array([])
    shape = (())
    Nframes = 0
    concat = np.array([])
    dtype = np.uint32

    def __init__(self, frames, shape, cut = True, dtype = np.uint32):
        '''
        Create `frameseries` object from array of frames

        Parameters
        ---------
        frames : :class:`numpy.ndarray`

        shape : tuple

        cut : bool

        dtype : data-type

        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        self.frames = np.array(frames, dtype=np.object)
        self.concat = np.concatenate(frames)
        self.Nframes = len(frames)
        self.shape = shape
        self.dtype = dtype
        # calculate photon numbers
        self.N = np.array([frame.shape[0] for frame in self.frames])
        # cut to rectangular shape if requested
        if cut:
            self.cuttoshape(self.shape)

    def __getitem__(self, key):
        '''
        '''
        if isinstance(key, slice) or isinstance(key, list) or isinstance(key, np.ndarray):
            return frameseries(self.frames[key], self.shape, cut=False)
        elif isinstance(key, int):
            return singleframe([self.frames[key]], self.shape)
        else:
            raise TypeError

    def __setitem__(self, key, frame):
        '''
        '''
        if isinstance(frame, np.ndarray):
            self.frames[key] = frame
            self.N[key] = len(frame)
        else:
            raise TypeError

    def store(self, fname):
        '''
        Store pickled frameseries

        Parameters
        ---------
        fname : string
            file name

        '''
        pickle.dumps(self, open(fname, 'w'))

    def cuttoshape(self, shape):
        '''
        Cut frames to shape

        Parameters
        ---------
        shape :

        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        from region import rect

        self.shape = shape
        # prepare a rectangle
        r = rect((0,0),(shape[0],shape[1]))
        cfs = r.getframeseries(self, reshape=False)
        self.frames = cfs.frames
        self.concat = cfs.concat
        self.N = cfs.N


    def accumframes(self):
        '''
        Accumulate all photons from frames

        Parameters
        ---------


        Returns
        ---------
        accum : :class:`numpy.ndarray`

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        # count photons in each pixel
        accum = bincountnd(np.array(self.concat, dtype=self.dtype), self.shape)
        return accum

    def delneighbours(self, r=5):
        '''
        Find photon pairs that are too close to each other and remove second photon from the frame
        '''
        for i, frame in enumerate(self.frames):
            progress(i)
            if len(frame)>=2:
                kdt=KDTree(np.array(frame))
                ridx=[]
                kdtq=kdt.query_pairs(r,p=2.0)
                for pidx in kdtq:
                    if (pidx[1] not in ridx) and (pidx[0] not in ridx):
                        ridx.append(pidx[1])
                mask=np.ones(len(frame),dtype=np.bool)
                for j in ridx:
                    mask[j]=False
                self.N[i]=np.sum(mask)
                self.frames[i]=frame[mask]
        self.concat = np.concatenate(self.frames)

    def accumautocoinc(self):
        '''
        Accumulate autocoincidences

        Parameters
        ---------

        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        accum = np.zeros(
                shape=(self.shape[0],self.shape[0],self.shape[1],self.shape[1]),
                dtype=np.uint32)
        for frame in self.frames:
            if frame.shape[0] > 0:
                binautocoinc(frame, accum)
        return accum

    def rotate(self, angle, centerpoint):
        '''
        Rotate coordinate system

        Parameters
        ---------
        angle :

        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        cc_frames = np.array(self.concat, dtype=np.float) - centerpoint
        rcc_frames = np.zeros(shape=cc_frames.shape, dtype=cc_frames.dtype)
        rcc_frames[:,0] = cc_frames[:,0]*np.cos(angle) + cc_frames[:,1]*np.sin(angle)
        rcc_frames[:,1] = cc_frames[:,1]*np.cos(angle) - cc_frames[:,0]*np.sin(angle)
        rcc_frames += centerpoint
        self.concat = np.array(np.around(rcc_frames), dtype=self.dtype)
        self.frames = array_split(self.concat, self.N)[1:-1]
        self.cuttoshape(self.shape)


    def rescale(self, scale, centerpoint):
        '''
        Rescale coordinate system

        Parameters
        ---------
        factor :

        axis :

        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        # TODO: implement scaling
        pass

    def len(self):
        '''
        Get total length fo series of frames `Nframes`

        Parameters
        ---------


        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        return self.Nframes

    def __len__(self):
        '''
        Get total length fo series of frames `Nframes`

        Parameters
        ---------


        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        return self.Nframes

    def shift(self, n):
        '''
        Shift frames

        Parameters
        ---------
        n :

        Returns
        ---------

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        self.frames = self.frames[n:] + self.frames[:n]
        self.N = np.roll(self.N, n)
        self.concat = np.concatenate(self.frames)

    def transform(self, transform):
        '''
        Affine tranformation of photons.

        Parameters
        ---------
        transform : tuple
            (a,b,c,d,e,f), where ((a,b), (c,d)) is transofmration matrix
            and (e,f) is the added vector
        '''
        a, b, c, d, e, f=transform
        cc_frames = np.array(self.concat, dtype=np.float)
        rcc_frames = np.zeros(shape=cc_frames.shape, dtype=cc_frames.dtype)
        rcc_frames[:,0] = cc_frames[:,0]*a + cc_frames[:,1]*b + e
        rcc_frames[:,1] = cc_frames[:,1]*d + cc_frames[:,0]*c + f
        self.concat = np.array(np.around(rcc_frames), dtype=self.dtype)
        self.frames = array_split(self.concat, self.N)[1:-1]
        self.cuttoshape(self.shape)

    def append(self, fs):
        '''
        Append antoher frameseries to current frameseries
        '''
        self.frames = np.concatenate((self.frames, fs.frames))
        self.N = np.array(map(len, self.frames))
        self.concat = np.concatenate(self.frames)
        self.Nframes = self.Nframes + fs.Nframes

    def timeseries(self, samples=1000):
        '''
        Get photon numbers as resampled time series
        '''
        tmp = np.cumsum(self.N)[samples:]
        tmp2 = np.cumsum(self.N)[:-samples]
        return (tmp - tmp2) / float(samples)

    def plot(self, samples=1000):
        '''
        Plot the series as a time series of photon number after resampling
        '''
        plt.plot(self.timeseries(samples))

    def copy(self):
        '''
        Copies the frameseries in memory and returns new object
        '''
        return deepcopy(self)

    def mean(self, uncert=False):
        '''
        '''
        from stat1d import mean
        return mean(self, uncert)

    def g2(self, uncert=False):
        '''
        '''
        from stat1d import g2
        return g2(self, uncert)

    def std(self, uncert=False):
        '''
        '''
        from stat1d import std
        return std(self, uncert)

    def thmodes(self, uncert=False):
        '''
        '''
        from stat1d import thmodes
        return thmodes(self, uncert)

    def var(self, uncert=False):
        '''
        '''
        from stat1d import var
        return var(self, uncert)

    def imshow(self):
        '''
        '''
        plt.imshow(self.accumframes())

    def delframes(self, max_photons=20):
        '''
        '''
        self.frames=np.array([frame for frame in self.frames if frame.shape[0] <= max_photons], dtype=np.object)
        self.concat = np.concatenate(self.frames)
        self.N = [frame.shape[0] for frame in self.frames]
        self.Nframes = len(self.frames)

    def delsubsequent(self,Nf=10):
        '''
        Delete Nf frames after photon is detected in one
        '''
        tmp = np.cumsum(self.N)[Nf:]
        tmp2 = np.cumsum(self.N)[:-Nf]
        running_sum = (tmp - tmp2)
        mask=np.concatenate([np.zeros(Nf+1,dtype=np.bool),running_sum[:-1]==0])
        self.frames=self.frames[mask]
        self.concat = np.concatenate(self.frames)
        self.N = [frame.shape[0] for frame in self.frames]
        self.Nframes = len(self.frames)

    def delsubsmask(self,Nf=10):
        '''
        Get the mask corresponding to delsubsequent function; does not alter the object
        '''
        tmp = np.cumsum(self.N)[Nf:]
        tmp2 = np.cumsum(self.N)[:-Nf]
        running_sum = (tmp - tmp2)
        mask=np.concatenate([np.zeros(Nf+1,dtype=np.bool),running_sum[:-1]==0])
        return mask


class singleframe(frameseries):
    '''
    '''

    def scatter(self):
        plt.scatter(self.frames[0][:,1], self.frames[0][:,0])


# functions

def fsconcat(fslist):
    '''
    Concatenate frameseries
    '''
    frames = np.concatenate(map(lambda fs: fs.frames, fslist))
    return frameseries(frames, shape = fslist[0].shape, cut=False)

def fsmerge(fslist):
    '''
    Merge frame-by-frame
    '''
    
def fsplot(fslist, samples=1000):
    '''
    Plot mutltiple frameseries as photon number time series
    '''
    for fs in fslist:
        fs.plot(samples)

def emptyframe(shape):
    return singleframe(np.empty(shape=(0, 2), dtype=self.dtype),
                       shape, cut=False)

def loadfs(fname):
    '''
    Load frameseries from file
    '''
    fs = pickle.load(open(fname, 'r'))
    if fs.__class__ == frameseries:
        return fs
    else:
        print 'Error: pickled object not of class frameseries.'


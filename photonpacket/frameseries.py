import numpy as np
from bincountnd import bincountnd
from scipy.spatial import KDTree
from matplotlib import pyplot as plt
from copy import deepcopy
from message import message, progress

from coinc import binautocoinc
from frameutils.arraysplit import arraysplit

try:
    import cPickle as pickle
except:
    import pickle

# main frameseries class

class frameseries:
    N = np.array([])
    shape = (())
    Nframes = 0
    photons = np.array([])
    idxs = np.array([])
    dtype = np.uint16

    class fs_frames:
        '''
        '''
        def __init__(self, fs):
            '''
            '''
            self.fs =  fs
           
        def __getitem__(self, key):
            '''
            '''
            if isinstance(key, slice):
                start, stop, step = key.indices(self.fs.Nframes)
                frames = []
                idx = start
                while idx < stop:
                    frames.append(self.fs.photons[self.fs.idxs[idx]:self.fs.idxs[idx+1]])
                    idx += step
                return np.array(frames, dtype=np.object)
            elif isinstance(key, list) or isinstance(key, np.ndarray):
                if max(key) > self.fs.Nframes:
                    raise KeyError
                else:
                    frames = []
                    for idx in key:
                        frames.append(self.fs.photons[self.fs.idxs[idx]:self.fs.idxs[idx+1]])
                    idx += step
                    return np.array(frames, dtype=np.object)
            elif isinstance(key, int):
                if key > self.fs.Nframes:
                    raise KeyError
                else:
                    st_idx = self.fs.idxs[key]
                    end_idx = self.fs.idxs[key+1]
                    photons = self.fs.photons[st_idx:end_idx]
                    return np.array([photons])
            else:
                raise TypeError
            
        def asarray(self):
            '''
            '''
            return np.array(arraysplit(self.fs.photons, self.fs.idxs[1:-1]), dtype=np.object)
        
        def __repr__(self):
            '''
            '''
            return np.array(arraysplit(self.fs.photons, self.fs.idxs[1:-1]), dtype=np.object).__repr__()
            
    def __init__(self, photons, idxs, shape, cut = True, dtype = np.uint16):
        '''
        Create `frameseries` object from photons and indices

        Parameters
        ---------
        photons : :class:`numpy.ndarray`

        idxs : :class:`numpy.ndarray`
        
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
        self.photons = photons
        self.idxs = idxs #maybe from N?
        self.frames = frameseries.fs_frames(self)
        self.Nframes = len(idxs) - 1
        self.shape = shape
        self.dtype = dtype
        # calculate photon numbers
        self.N = np.diff(idxs) #from arg?
        # cut to rectangular shape if requested
        if cut:
            self.cuttoshape(self.shape)

    def __getitem__(self, key):
        '''
        '''
        if isinstance(key, slice) or isinstance(key, list) or isinstance(key, np.ndarray):
            pass# TODO
        elif isinstance(key, int):
            st_idx = self.idxs[key]
            end_idx = self.idxs[key+1]
            photons = self.photons[st_idx:end_idx]
            return singleframe(photons, np.array([0, end_idx - st_idx]), 
                               self.shape, cut=False)
        else:
            raise TypeError

    def __setitem__(self, key, frame):
        '''
        '''
        if isinstance(frame, np.ndarray):
            # TODO
            self.frames[key] = frame
            self.N[key] = len(frame)
        else:
            raise TypeError
            
    def __del__(self):
        del self.photons
        del self.idxs
        del self.N
        del self.frames
        
    def store(self, fname):
        '''
        Store pickled frameseries

        Parameters
        ---------
        fname : string
            file name

        '''
        pickle.dumps(self, open(fname, 'wb'))

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
        self.idxs = cfs.idxs
        self.photons = cfs.photons
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
        accum = bincountnd(np.array(self.photons, dtype=self.dtype), self.shape)
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
        cc_frames = np.array(self.photons, dtype=np.float) - centerpoint
        rcc_frames = np.zeros(shape=cc_frames.shape, dtype=cc_frames.dtype)
        rcc_frames[:,0] = cc_frames[:,0]*np.cos(angle) + cc_frames[:,1]*np.sin(angle)
        rcc_frames[:,1] = cc_frames[:,1]*np.cos(angle) - cc_frames[:,0]*np.sin(angle)
        rcc_frames += centerpoint
        self.photons = np.array(np.around(rcc_frames), dtype=self.dtype)
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
        Get total length of series of frames `Nframes`

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
        self.photons = self.photons[self.idxs[n]:] + self.photons[:self.idxs[n]]
        self.N = np.roll(self.N, n)
        self.idxs = np.r_[0, np.cumsum(self.N)]

    def transform(self, transform):
        '''
        Affine tranformation of photons.

        Parameters
        ---------
        transform : tuple
            (a,b,c,d,e,f), where ((a,b), (c,d)) is transformation matrix
            and (e,f) is the added vector
        '''
        a, b, c, d, e, f=transform
        cc_frames = np.array(self.photons, dtype=np.float)
        rcc_frames = np.zeros(shape=cc_frames.shape, dtype=cc_frames.dtype)
        rcc_frames[:,0] = cc_frames[:,0]*a + cc_frames[:,1]*b + e
        rcc_frames[:,1] = cc_frames[:,1]*d + cc_frames[:,0]*c + f
        self.photons = np.array(np.around(rcc_frames), dtype=self.dtype)

        self.cuttoshape(self.shape)

    def append(self, fs):
        '''
        Append antoher frameseries to current frameseries
        '''
        self.idxs = np.concatenate([self.idxs, self.idxs[-1] + fs.idxs[1:]])
        self.N = np.concatenate([self.N, fs.N])
        self.photos = np.concatenate([self.photons, fs.photons])
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
    
    def maskframes(self, frame_mask):
        '''
        
        '''
        mask = np.repeat(frame_mask, self.N)
        self.photons = self.photons[mask]
        self.N = self.N[frame_mask]
        self.idxs = np.r_[0, np.cumsum(self.N)]
        self.Nframes = len(self.idxs) - 1
        
    def delframes(self, max_photons=20):
        '''
        '''
        frame_mask = self.N <= max_photons
        self.maskframes(frame_mask)

    def delsubsequent(self, Nf=10):
        '''
        Delete Nf frames after photon is detected in one
        '''
        tmp = np.cumsum(self.N)[Nf:]
        tmp2 = np.cumsum(self.N)[:-Nf]
        running_sum = (tmp - tmp2)
        frame_mask = np.concatenate([np.zeros(Nf+1,dtype=np.bool),running_sum[:-1]==0])
        self.maskframes(frame_mask)

    def delsubsmask(self, Nf=10):
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
        plt.scatter(self.photons[:,1], self.photons[:,0])


# functions

def fsconcat(fslist):
    '''
    Concatenate frameseries
    '''
    photons = np.concatenate([fs.photons for fs in fslist])
    fs_idxs = np.array([fs.idxs[-1] for fs in fslist])
    fs_idxs = np.r_[0, np.cumsum(fs_idxs)]
    idxs = np.concatenate([fs.idxs[1:] + fs_idxs[i] for i, fs in enumerate(fslist)])
    idxs = np.r_[0, idxs]
    return frameseries(photons, idxs, shape = fslist[0].shape, cut=False, dtype=fslist[0].dtype)

def fsmerge(fslist):
    '''
    Merge frame-by-frame
    ''' 
    
    new_photons = []
    idxs = np.sum(np.array([fs.idxs for fs in fslist]), axis=0)
    for i in xrange(len(idxs)-1):
        new_photons.extend([fs.photons[fs.idxs[i]:fs.idxs[i+1]] for fs in fslist])
    return frameseries(np.concatenate(new_photons), idxs, shape = fslist[0].shape, cut=False, dtype=fslist[0].dtype)
            
def fsplot(fslist, samples=1000):
    '''
    Plot mutltiple frameseries as photon number time series
    '''
    for fs in fslist:
        fs.plot(samples)

def emptyframe(shape):
    return singleframe(np.empty(shape=(0, 2), dtype=np.uint16),
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


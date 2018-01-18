import numpy as np
from bincountnd import bincountnd
from scipy.spatial import KDTree
from scipy.spatial.distance import pdist, squareform
from matplotlib import pyplot as plt
from copy import deepcopy
from message import message, progress
 
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
                i = start
                while i < stop:
                    frames.append(self.fs.photons[self.fs.idxs[i]:self.fs.idxs[i+1]])
                    i += step
                return np.array(frames, dtype=np.object)
            elif isinstance(key, list) or isinstance(key, np.ndarray):
                if max(key) > self.fs.Nframes:
                    raise KeyError
                else:
                    frames = []
                    for i in key:
                        frames.append(self.fs.photons[self.fs.idxs[i]:self.fs.idxs[i+1]])
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
        if isinstance(key, slice):
            start, stop, step = key.indices(self.Nframes)
            photons = []
            i = start
            idx = 0
            idxs = [0,]
            while i < stop:
                st = self.idxs[i]
                end = self.idxs[i+1]
                photons.append(self.photons[st:end])
                i += step
                idx += end - st
                idxs.append(idx)
            photons = np.concatenate(photons)
            return frameseries(photons, np.array(idxs), self.shape, cut=False, dtype=self.dtype)
        elif isinstance(key, list) or isinstance(key, np.ndarray):
            if max(key) > self.Nframes:
                raise KeyError
            else:
                photons = []
                idxs = np.zeros(len(key) + 1)
                idxs[0] = 0
                idx = 0
                for i in key:
                    st = self.idxs[i]
                    end = self.idxs[i+1]
                    photons.append(self.photons[st:end])
                    idx += end - st
                    idxs[i+1] = idx
                photons = np.concatenate(photons)
                return frameseries(photons, idxs, self.shape, cut=False, dtype=self.dtype)
        elif isinstance(key, int):
            st_idx = self.idxs[key]
            end_idx = self.idxs[key+1]
            photons = self.photons[st_idx:end_idx]
            return singleframe(photons, np.array([0, end_idx - st_idx]), 
                               self.shape, cut=False, dtype=self.dtype)
        else:
            raise TypeError

    def __setitem__(self, key, fr):
        '''
        '''
        # fr is a numpy array
        if isinstance(fr, np.ndarray):
            
            # fr is a series of frames
            if fr.dtype == np.object:

                if isinstance(key, int) and len(fr) == 1:
                    pass
                elif isinstance(key, list) or isinstance(key, np.ndarray):
                    if len(key) == len(fr):
                        pass
                    else:
                        raise KeyError
                elif isinstance(key, slice):
                    pass
                else:
                    raise KeyError
                    
            # fr is a single frame
            elif fr.dtype == self.dtype:
                if isinstance(key, int):
                    pass
                else:
                    # this does not make sense
                    raise KeyError
            else:
                raise TypeError
                
        # fr is a frameseries
        elif isinstance(fr, frameseries):
            if isinstance(key, int) and len(fr) == 1:
                pass
            elif isinstance(key, list) or isinstance(key, np.ndarray):
                if len(key) == len(fr):
                    pass
                else:
                    raise KeyError
            elif isinstance(key, slice):
                pass
            else:
                raise KeyError
                
        else:
            raise KeyError
            
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


    def accumframes(self,first=0,nframes='all'):
        '''
        Accumulate all photons from frames ranging from first to first+nframes
        defaults to all frames

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
        if (nframes != 'all' or first != 0):
            if isinstance(first,int):
                first = max(0,min(first,self.N.shape[0]))
                if(nframes == 'all'): 
                    nframes = max(self.N.shape[0] - first,0)
                nframes = max(0,min(nframes,self.N.shape[0]))  
                nrest = max(self.N.shape[0] - first - nframes,0)
                frame_mask = np.r_[np.zeros(first,dtype=np.bool),np.ones(nframes,dtype=np.bool),np.zeros(nrest,dtype=np.bool)]
                mask = np.repeat(frame_mask, self.N)
                phts = self.photons[mask]
            else:
                raise KeyError
        else:
            phts = self.photons
        accum = bincountnd(np.array(phts, dtype=self.dtype), self.shape)    
        return accum

    def delneighbours(self, r=5, metric='euclidean'):
        '''
        Find photon pairs that are too close to each other and remove second photon from the frame
        args: radius, metric (c.f. scipy.spatial.distance.pdist)
        '''
        
        '''
        This is an old version of delneighbours that does not actually delete all neigbours that should be deleted
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
        '''
        def outofrange(frame, rng):
            tmp = pdist(frame, metric)
            tmp = squareform(tmp)<rng
            plist = range(0,frame.shape[0])
            for j in plist:
                tmp[:,j]=False
                for i in np.where(tmp[j])[0]:
                    try:
                        plist.remove(i)
                    except ValueError:
                        pass
            return plist
        
        masks = []
        newN = []
        for i in range(len(self.idxs)-1):
            frame = self.photons[self.idxs[i]:self.idxs[i+1]]
            tmp = self.idxs[i]+np.array(outofrange(frame, r),dtype=np.uint32)
            masks.append(tmp)
            newN.append(tmp.shape[0])
            progress(i)
        mask = np.array(np.hstack(masks),dtype=np.uint32)
        self.photons = self.photons[mask]
        self.N = np.array(newN)
        self.idxs = np.array(np.r_[0, np.cumsum(self.N)],dtype=np.int32)
        
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
    fs = pickle.load(open(fname, 'rb'))
    if fs.__class__ == frameseries:
        return fs
    else:
        print 'Error: pickled object not of class frameseries.'


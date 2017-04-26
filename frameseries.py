import numpy as np
from bincountnd import bincountnd
from scipy.spatial import KDTree
from scipy.signal import resample
from arraysplit import array_split
from matplotlib import pyplot as plt
from copy import deepcopy

# main frameseries class

class frameseries:
    frames = []
    N = np.array([])
    shape = (())
    frameN = 0
    concat = np.array([])

    def __init__(self, frames, shape, cut = True):
        '''
        Create `frameseries` object from array of frames
        
        Parameters
        ---------
        frames : :class:`numpy.ndarray`
            
        shape : tuple
            
        cut : bool
            
        Returns
        ---------
        coa
        See Also
        ---------
        
        Notes
        ---------
        
        Examples
        ---------
        '''
        self.frames = frames
        self.concat = np.concatenate(frames)
        self.frameN = len(frames)
        self.shape = shape
        # calculate photon numbers
        self.N = np.array(map(len, frames))
        # cut to rectangular shape if requested
        if cut:
            self.cuttoshape(self.shape)

    def __getitem__(self, key):
        '''
        '''
        return self.frames[key]
    
    def __setitem__(self, key, frame):
        '''
        '''
        self.frames[key] = frame
        self.N[key] = len(frame)
        
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
        '''
        self.shape = shape
        j = 0
        aux_frames = self.frames
        for frame in aux_frames:
            # prepare mask to cut out photons outside rectangular shape
            mask0 = frame[:, 0] < shape[0]
            mask1 = frame[:, 1] < shape[1]
            mask = mask0 * mask1
            # apply mask
            self.frames[j] = frame[mask]
            # calculate total photon number
            self.N[j] = np.sum(mask)
            j += 1
        '''


    def accumframes(self):
        '''
        Accumulate all photons from frames
        
        Parameters
        ---------
        fs1 : 
            
            
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
        accum = bincountnd(np.array(self.concat, dtype=np.uint32), self.shape)
        return accum
    
    def delneighbours(self, r=5):
        '''
        Find photon pairs that are too close to each other and remove second photon from the frame
        '''
        for i, frame in enumerate(self.frames):
            if len(frame)>=2:
                kdt=KDTree(np.array(frame))
                ridx=[]
                kdtq=kdt.query_pairs(r,p=2)
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
        i=0
        accum=np.zeros(
                shape=(self.shape[0],self.shape[0],self.shape[1],self.shape[1])
                )
        for frame in self.frames:
            frame=np.hstack((
                    np.dstack(np.meshgrid(frame[:,0], frame[:,0])).reshape(-1, 2),
                    np.dstack(np.meshgrid(frame[:,1], frame[:,1])).reshape(-1, 2)
                    ))
            for coinc in frame:
                accum[coinc[0],coinc[1],coinc[2],coinc[3]]=accum[coinc[0],
                      coinc[1],coinc[2],coinc[3]]+1
            print i
            i=i+1

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
        self.concat = np.array(rcc_frames, dtype=np.uint32)
        self.frames = array_split(self.concat, self.N)[1:-1]
        self.cuttoshape(self.shape)
        
    
    def rescale(self, factor, axis, **kwargs):
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
        Get total length fo series of frames `frameN`
        
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
        return self.frameN
    
    def roll(self, n):
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
        
    
    def append(self, fs):
        '''
        Append antoher frameseries to current frameseries
        '''
        self.frames = np.concatenate((self.frames, fs.frames))
        self.N = np.array(map(len, self.frames))
        self.concat = np.concatenate(self.frames)
        self.frameN = self.frameN + fs.frameN
    
    def timeseries(self, samples=1000):
        '''
        Get photon numbers as resampled time series
        '''
        return resample(self.N, samples)
        
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
        

# functions

def fsconcat(fslist):
    '''
    Concatenate frameseries
    '''
    frames = np.concatenate(map(lambda fs: fs.frames, fslist))
    return frameseries(frames, shape = fslist[0].shape, cut=False)

def fsplot(fslist, samples=1000):
    '''
    Plot mutltiple frameseries as photon number time series
    '''
    for fs in fslist:
        fs.plot(samples)
        
        
    
import numpy as np
from bincountnd import bincountnd
from scipy.spatial import KDTree

class frameseries:
    frames = []
    N = np.array([])
    shape = (())
    frameN = 0

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
        self.frameN = len(frames)
        self.shape = shape
        self.N = np.array(map(len, frames))
        # calculate photon numbers
        # for i, frame in enumerate(self.frames):
        #    self.N[i] = int(frame.shape[0])
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
        r = rect((0,0),(shape[0],shape[1]))
        r.getframeseries(self, reshape=False)
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
        # concatenate all frames
        flat_fs = np.concatenate(self.frames)
        # count photons in each pixel
        accum = bincountnd(flat_fs, self.shape)
        return accum
    
    def delneighbours(self,r=5):
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
  
    def rotate(self, angle, **kwargs):
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
        # TODO: implement rotation
        pass
    
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
        # TODO: implement shifting of frames
        pass
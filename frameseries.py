import numpy as np
from bincountnd import bincountnd

class frameseries:
    frames = []
    N = np.array([])
    shape = (())
    frameN = 0

    def __init__(self, frames, shape, cut = True):
        self.frames = frames
        self.frameN = len(frames)
        self.shape = shape
        self.N = np.zeros((len(self.frames)))
        # calculate photon numbers
        for i, frame in enumerate(self.frames):
            self.N[i] = int(frame.shape[0])
        # cut to rectangular shape if requested
        if cut:
            self.cuttoshape(self.shape)


    def cuttoshape(self,shape):
        '''
        Delete out-of-bound photons
        :param frameshape: shape of frame, tuple ((x0,y0),(x1,y1))
        :return: none
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


    def accumframes(self):
        '''
        Accumulate photon through all frames
        :return: accumulated array
        '''
        # concatenate all frames
        flat_fs = np.concatenate(self.frames)
        # count photons in each pixel
        accum = bincountnd(flat_fs, self.shape)
        return accum

    def accumautocoinc(self):
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
        # TODO: implement rotation
        pass
    
    def rescale(self, factor, axis, **kwargs):
        # TODO: implement scaling
        pass
    
    def len(self):
        return self.frameN
    
    def shift(self, n):
        # TODO: implement shifting of frames
        pass
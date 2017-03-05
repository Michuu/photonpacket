import numpy as np

class frameseries:
    frames = []
    N = np.array([])
    shape = (())

    def __init__(self, frames, shape):
        self.frames = frames
        self.shape = shape
        self.N = np.zeros((len(self.frames)))
        for i, frame in enumerate(self.frames):
            self.N[i] = int(frame.shape[0])
        self.cuttoshape(self.shape)


    def cuttoshape(self,shape):
        '''
        Delete out-of-bound photons
        :param frameshape: shape of frame, tuple ((x0,y0),(x1,y1))
        :return: none
        '''

        self.shape = shape
        j=0
        aux_frames = self.frames
        for frame in aux_frames:
            i=0
            for photon in frame:
                if(photon[0]>=shape[0] or photon[1]>=shape[1]):
                    self.frames[j]=np.delete(self.frames[j],i,axis=0)
                    self.N[j]=self.N[j]-1
                i=i+1
            j=j+1


    def accumframes(self):
        '''
        Accumulate photon through all frames
        :param shape: TODO: remove
        :return: accumulated array
        '''

        i=0
        accum=np.empty(shape=self.shape)
        for frame in self.frames:
            for photon in frame:
                accum[photon[0],photon[1]]=accum[photon[0],photon[1]]+1
            i=i+1

        return accum

    def accumautocoinc(self):
        i=0
        accum=np.zeros(shape=(self.shape[0],self.shape[0],self.shape[1],self.shape[1]))
        for frame in self.frames:
            frame=np.hstack((np.dstack(np.meshgrid(frame[:,0], frame[:,0])).reshape(-1, 2),np.dstack(np.meshgrid(frame[:,1], frame[:,1])).reshape(-1, 2)))
            for coinc in frame:
                accum[coinc[0],coinc[1],coinc[2],coinc[3]]=accum[coinc[0],coinc[1],coinc[2],coinc[3]]+1
            print i
            i=i+1

        return accum
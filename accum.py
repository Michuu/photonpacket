import numpy as np
from scipy.signal import convolve2d

class accum:

    @staticmethod
    def accumframes(fs):
        '''
        Accumulate photon through all frames
        :return: accumulated array
        '''
        # should this function really be here??
        i=0
        accum=np.empty(shape=fs.shape)
        for frame in fs.frames:
            for photon in frame:
                accum[photon[0],photon[1]]=accum[photon[0],photon[1]]+1
            i=i+1

        return accum

    @staticmethod
    def accumcoinc(fs1,fs2):
        i=0
        accum=np.zeros(shape=(fs1.shape[0],fs1.shape[0],
                              fs1.shape[1],fs1.shape[1]))
        for frame in fs1.frames:
            frame2 = fs2.frames[i]
            if len(frame2) != 0 and len(frame) != 0:
                cframe=np.hstack((
                        np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),
                        np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)
                        ))
                for coinc in cframe:
                    accum[coinc[0],coinc[1],coinc[2],coinc[3]]=accum[coinc[0],
                          coinc[1],coinc[2],coinc[3]]+1
            i=i+1
        return accum
  
    @staticmethod
    def coinchist(fs1,fs2,signs):
        '''
        fs1 and fs2 should rather be reshaped, and have the same number of frames
        '''
        i=0
        accum = np.zeros(shape=(fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1))
        for frame in fs1.frames:
            frame2 = fs2.frames[i]
            if len(frame2) != 0 and len(frame) != 0:
                cframe = np.hstack((
                        np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),
                        np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)
                        ))
                cframe2 = np.zeros(shape=(cframe.shape[0],2),dtype=np.uint16)
                if signs[0]:
                      cframe2[:,0] = cframe[:,0] + cframe[:,1]
                else:
                      cframe2[:,0] = cframe[:,0] - cframe[:,1] + fs2.shape[0]
                if signs[1]:
                      cframe2[:,1] = cframe[:,2] + cframe[:,3]
                else:
                      cframe2[:,1] = cframe[:,2] - cframe[:,3] + fs2.shape[1]
                for coinc in cframe2:
                      accum[coinc[0],coinc[1]] = accum[coinc[0],coinc[1]] + 1
            i = i + 1
        return accum
    
    @staticmethod
    def acchist(h1,h2,signs):
        if signs[0]:
              h1=np.flip(h1,axis=0)
        if signs[1]:
              h2=np.flip(h2,axis=1)
        return convolve2d(h1,h2)
            
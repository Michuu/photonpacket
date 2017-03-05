import numpy as np

class accum:

    @staticmethod
    def accumframes(fs):
        '''
        Accumulate photon through all frames
        :return: accumulated array
        '''

        i=0
        accum=np.empty(shape=shape)
        for frame in frames:
            for photon in frame:
                accum[photon[0],photon[1]]=accum[photon[0],photon[1]]+1
            i=i+1

        return accum

    @staticmethod
    def accumcoinc(fs1,fs2):
        i=0
        accum=np.zeros(shape=(fs1.shape[0],fs1.shape[0],fs1.shape[1],fs1.shape[1]))
        for frame in fs1.frames:
            frame2 = fs2.frames[i]
            if len(frame2) != 0 and len(frame) != 0:
                cframe=np.hstack((np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)))
                for coinc in cframe:
                    accum[coinc[0],coinc[1],coinc[2],coinc[3]]=accum[coinc[0],coinc[1],coinc[2],coinc[3]]+1
            i=i+1

        return accum
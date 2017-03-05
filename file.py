import numpy as np
from frameseries import frameseries
from scipy.sparse import dok_matrix, kron, csr_matrix, coo_matrix

class file:
    frames = []
    # sparse_frames = []
    accum = []
    # sparse_accum = 0
    Nframes = 0
    shape = (100,600)

    @staticmethod
    def readall(name):
        '''
        Read file to memory
        :param name: file name
        :return: instance of class File
        '''

        nframes=0
        f=open(name)
        while(True):
            nxy=np.fromfile(f,'>i4',2)
            if nxy.size==0:
                break
            N = nxy[0]*nxy[1]
            nframes = nframes+1
            img = np.fromfile(f,'>u2',N)

            self=file()
            if N != 0:
                frame=np.reshape(img/10,nxy)[:,:2] # dzielenie przez 10, nie wiadomo za bardzo czemu!
                self.frames.append(frame)
        f.close()
        self.Nframes=nframes
        return self

    def getframeseries(self):
        if self.frames:
            return frameseries(self.frames,self.shape)

    '''
    def sparse_process(self,shape):
        i=0
        for frame in self.frames:
            N=frame.shape[0]
            xc=frame[:,0]
            yc=frame[:,1]
            data=np.ones(shape=N)
            csr_frame=csr_matrix(coo_matrix((data,(xc,yc)),shape=shape))
            self.sparse_frames.append(csr_frame)
            print i
            i=i+1

    def sparse_accumframes(self,shape):
        i=0
        sparse_accum = csr_matrix(shape,dtype=np.uint16)
        for sparse_frame in self.sparse_frames:
            sparse_accum = sparse_accum + sparse_frame
            print i
            i=i+1
        return sparse_accum.toarray()
    '''



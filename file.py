import numpy as np
from frameseries import frameseries
import re
# from scipy.sparse import dok_matrix, kron, csr_matrix, coo_matrix

class file:
    frames = []
    # sparse_frames = []
    accum = []
    # sparse_accum = 0
    Nframes = 0
    name = ''

    def __init__(self,name):
        self.name = name
        self.frames = []
        
    @staticmethod
    def read(name, **kwargs):
        '''
        Read file to memory
        :param name: file name
        :return: instance of class File
        '''
        # TODO: add filename recognition and parsing, automatic shape and framenumber detection
        
        params = file.parsename(name)
        if 'fs' in params:
            shape = params['fs']
            shapedetect = False
        else:
            shapedetect = True
            
        
        if 'Nframes' in kwargs:
              maxframes = kwargs['Nframes']
              frames_limit = True
        else:
              maxframes = 0
              frames_limit = False
              
        nframes=0
        f=open(name,'rb')
        self=file(name)
        while(True):
            nxy=np.fromfile(f,'>i4',2)
            if nxy.size==0 or (nframes > maxframes and frames_limit):
                break
            N = nxy[0]*nxy[1]
            nframes = nframes+1
            img = np.fromfile(f,'>u2',N)

            if N != 0:
                # dzielenie przez 10, nie wiadomo za bardzo czemu!
                # TODO: automatic detection of /10 division
                # TODO: possibility of getting other info about photons
                frame=np.reshape(img/10,nxy)[:,:2]
                self.frames.append(frame)
        f.close()
        self.Nframes = nframes
        self.shape = shape
        return self

    def getframeseries(self):
        if self.frames:
            return frameseries(self.frames,self.shape)
    
    @staticmethod
    def parsename(name):
        data = name.split('-')
        seriesname = data[0]
        data = data[1:]
        params = {}
        for i, p in enumerate(data):
            m = re.match(r"(?P<param>[a-zA-Z]+)(?P<value>.+)$", p)
            param = m.group('param')
            value = m.group('value')
            if param == 'fs':
                value = map(int,value.split('x'))
            if param == 'Nf':
                value = int(value)              
            params[param] = value
        return params
    
    
    '''
    algorithms using sparse matrices
    proved to be quite ineffective due to conversion
    maybe they can be useful in other cases...
    
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
        



import numpy as np
from frameseries import frameseries
import re
import os
# from scipy.sparse import dok_matrix, kron, csr_matrix, coo_matrix

class file:
    frames = []
    # sparse_frames = []
    accum = []
    # sparse_accum = 0
    Nframes = 0
    name = ''
    path = ''

    def __init__(self,path,name):
        self.name = name
        self.frames = []
        
    @staticmethod
    def read(path, **kwargs):
        '''
        Read file to memory
        :param name: file name
        :return: instance of class File
        '''
        
        name = os.path.split(path)[-1]
        name = os.path.splitext(name)[0]
        
        try:
            shape = file.getshape(name)
            if isinstance(shape, np.ndarray):
                shapedetect = False
            else:
                shapedetect = True
        except:
            shapedetect = True
            
        
        if 'Nframes' in kwargs and file.getattribute(name,'Nf'):
              maxframes = min(kwargs['Nframes'], int(file.getattribute(name,'Nf')))
              frames_limit = True
        elif 'Nframes' in kwargs:
              maxframes = kwargs['Nframes']
              frames_limit = True
        elif file.getattribute(name,'Nf'):
              maxframes = file.getattribute(name,'Nf')
              frames_limit = True        
        else:
              maxframes = 0
              frames_limit = False
              
        nframes=0
        f=open(path,'rb')
        self=file(path,name)
        while(True):
            nxy=np.fromfile(f,'>i4',2)
            if nxy.size==0 or (nframes >= maxframes and frames_limit):
                break
            N = np.prod(nxy)
            nframes = nframes+1
            img = np.fromfile(f,'>u2',N)

            if N != 0:
                # dzielenie przez 10, nie wiadomo za bardzo czemu!
                # TODO: automatic detection of /10 division
                # TODO: possibility of getting other info about photons
                frame=np.reshape(img/10,nxy)[:,:2]
                self.frames.append(frame)
            # if shapedetect: TODO: implement shape detection
        f.close()
        self.Nframes = nframes
        print 'Read ' + str(nframes) + ' frames'
        self.shape = shape
        return self

    def getframeseries(self):
        if self.frames:
            return frameseries(self.frames,self.shape)
    
    @staticmethod
    def getshape(name):
        s = re.search(r"-fs(?P<x>\d+)x(?P<y>\d+)", name)
        try:
            if s.group('x') and s.group('y'):
                return np.array([int(s.group('x')),int(s.group('y'))])
            else:
                return False
        except AttributeError:
            return False
        except IndexError:
            return False
    
    @staticmethod
    def getattribute(name, attr):
        pattern = r"-" + attr + "(?P<attr>[\d.]+)(?P<si>[yafnumkMGTZ]{,1})"
        s = re.search(pattern, name)
        try:
            if s.group('attr') and s.group('si') and file.siprefix(s.group('si')):
                return float(s.group('attr')) * file.siprefix(s.group('si'))
            elif s.group('attr'):
                return float(s.group('attr'))
            else:
                return False
        except AttributeError:
            return False
        except IndexError:
            return False
        
    @staticmethod
    def siprefix(prefix):
        prefixes = {'y' : 1e-21, 'a' : 1e-18, 'f' : 1e-15, 'p' : 1e-12,
                    'n' : 1e-9, 'u' : 1e-6, 'm' : 1e-3, 'k' : 1e3,
                    'M' : 1e6, 'G' : 1e9, 'T' : 1e12}
        if prefix in prefixes:
            return prefixes[prefix]
        else:
            return False
            
    '''
    depreciated
    
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
        



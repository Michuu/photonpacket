#%%
import numpy as np
from .frameseries import frameseries
import re
import os
from . import settings
from .message import message, progress
from .helpers import siprefix
import io
# from scipy.sparse import dok_matrix, kron, csr_matrix, coo_matrix

def py3_fromfile(f, dtype, num):
    '''
    Faster than np.fromfile
    
    Parameters
    ----------
    f : file handle
    
    dtype : data type
    
    num : number of elements to read
    
    Returns
    ----------
    data : :class:`numpy.ndarray`
    '''
    dt = np.dtype(dtype)
    return np.frombuffer(f.read(num*dt.itemsize), dtype)
    
# def index_raw_file(fname:str):
#     dt_body=np.dtype('>u2')
#     with open(fname,"rb") as f:
#         #mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#         #b = f.read()
#         b = np.frombuffer(f.read(), dt_body)
#     idxs=[]
#     i=0
#     idxs.append(i)
#     nframes=0
#     while i<b.shape[0]:
#         x0,nph,y0,nc=b[i:i+4]
#         #assert(x0==0&y0==0)
#         if i==0:
#             photoDim = nc
#         i+=nph
#         idxs.append(i)
#         nframes+=1
#         progress(nframes)
#     return idxs, photoDim

class file:
    '''


    '''
    Nframes = 0
    name = ''
    path = ''
    nameversion = 0
    params = {}
    mode = 'fit'

    def __init__(self, path,name):
        '''
        Create instance of class including path and name

        Parameters
        ----------
        path : string

        name : string

        Returns
        ----------

        See Also
        ----------

        Notes
        ----------

        Examples
        ----------
        '''
        self.name = name

    
    def __del__(self):
        if 'params' in dir(self): del self.params
        if 'photons' in dir(self): del self.photons
        if 'idxs' in dir(self): del self.idxs

    @staticmethod
    def createFromPath(path):
        # extract name of file from path
        (directory, name) = os.path.split(path)
        # remove file extension
        name = os.path.splitext(name)[0]
        # create file instance
        self = file(path, name)
        self.directory=directory
        return self
    
    def loadMetadata(self):
        "try to read params json or xml file"
        directory=self.directory
        name = self.name
        try:
            if os.path.isfile(os.path.join(directory, name + '.json')) ==True:
                parse=settings.paramsparserjson
                self.params = parse(os.path.join(directory, name + '.json'))                
            else:
                parse = settings.paramsparserxlm
                self.params = parse(os.path.join(directory, name + '.xml'))
            self.nameversion = 2
            try:
                Nf = self.params['Nf']
            except AttributeError:
                Nf = False
            except KeyError:
                Nf = False
            try:
                roi = self.params['ROI']
                shape = np.array([roi[0], roi[2]])
            except AttributeError:
                shape = False
            
            
        # if this was not possible get them from filename
        except IOError:
            # this means that params file is not present
            shape = self.getshapefromname()
            Nf = self.getattributefromname('Nf')
            self.nameversion = 1
        except NameError:            
            # this means that parser is not defined
            print("Error: File present, but params parser not defined!")
            raise
            shape = self.getshapefromname()
            Nf = self.getattributefromname('Nf')
            self.nameversion = 1        
        except Exception as e:
            # this means there was an unexpected error when parsing
            # we will proceed with automatic shape detection and no frame limit
            print("Unexpected Exception when parsing xml file (trying automatic shape detection): %s"%e)
            shape = False
            Nf = False
            raise
        return (Nf, shape)
    
    def parsephotinfoMask(self,**kwargs):
        photinfoDim = 2
        photinfoMask = slice(None,2,None)
        if 'mode' in kwargs:
            if kwargs['mode'] == 'fit':
                pass
            elif kwargs['mode'] == 'max':
                photinfoMask = slice(6,8,None)
                self.mode = 'max'
            elif kwargs['mode'] == 'fit_step_max':
                photinfoMask = np.r_[np.ones(3,dtype=np.bool),np.zeros(3,dtype=np.bool),np.ones(2,dtype=np.bool)]
                photinfoDim = 5
                self.mode = 'fit_step_max'
            elif kwargs['mode'] == 'fit_step_val_max':
                photinfoMask = np.r_[np.ones(4,dtype=np.bool),np.zeros(2,dtype=np.bool),np.ones(2,dtype=np.bool)]
                photinfoDim = 6
                self.mode = 'fit_step_val_max'
            elif kwargs['mode'] == 'all':
                photinfoMask = np.ones(8,dtype=np.bool)
                photinfoDim = 8
                self.mode = 'all'
            else:
                print('Invalid mode selected, modes available: fit, max, fit_step_max,fit_step_val_max,all')
                return False
        return photinfoMask
    
    @staticmethod
    def read(path, **kwargs):
        '''
        Read photon data file

        Parameters
        ----------
        path : string
            path to file, passed to :func:`open`
        Nframes : int
            number of frames to read
        mode : string
            'fit' to extract photon positions as fitted by photon-finder (default)
            'max' to extract raw maximal photon positions

        Returns
        ----------
        file : :class:`file`
            instance of :class:`file` class

        Notes
        ----------

        References
        ----------

        Examples
        ----------


        '''
        self = file.createFromPath(path)
        (Nf, shape) = self.loadMetadata()


        # try to set shape
        # if not possible, plan for shape detection
        shapedetect = True
        try:
            if isinstance(shape, np.ndarray):
                shapedetect = False            
        except:
            pass         
        shapedetect = kwargs.get('shapedetect',shapedetect)

        # try to extract number of frames from params or filename
        # if number given both in filename and as argument
        if 'Nframes' in kwargs and Nf:
            # select smaller
            maxframes = min(kwargs['Nframes'], Nf)
        # number given only by argument
        elif 'Nframes' in kwargs:
            maxframes = kwargs['Nframes']
        # number given only in params or filename
        elif Nf:
            maxframes = Nf
        # number not given, turn off frame number limit
        else:
            maxframes = -1            
        div=kwargs.get('div',10)

        photinfoMask = self.parsephotinfoMask(**kwargs)
        
        if 'loadToFile' in dir(self.params):
            # see lvjson3 LV305.loadToFile
            self.params.loadToFile(self, path, maxframes)
        else:
            self.loadPhotonsV21(path, photinfoMask, maxframes)
        
        # rounding photons positions
        if kwargs.get('rounding',False):
            self.photons = np.array(np.round(np.array(self.photons,dtype=np.float)/div),dtype=np.uint16)
        else:
            self.photons = np.array(self.photons//div,dtype=np.uint16)
                    
        if shapedetect:
            try:
                shape = np.max(self.photons[:,0:2], axis=0)
            except ValueError:
                print('You must be joking... file contains 0 photons; aborting')
                return False

        # set shape
        self.shape = np.array((np.round(shape*10/div)),dtype=int)
        return self
    
    def loadPhotonsV21(self, path, photinfoMask, maxframes):
        "faster indexing of v2 binary save files"
        nframes = 0
        # open file for binary reading
        with io.open(path,'rb') as f:
            file_datab = f.read()        
        from struct import unpack
        #from collections import deque
        idxs=[]
        npht=[]
        #photons=[]
        i=0
        idxs.append(i)
        len_b=len(file_datab)
        while i<len_b and (maxframes<=0 or nframes<=maxframes):
            # 2d array size from LV
            nph,nc=unpack('>ii',file_datab[i:i+8])            
            if i == 0:
                photoDim = nc        
            i+=8+2*nph*nc # byte advance
            idxs.append(i) # header position
            npht.append(nph)
            #photons.append(b[i+8:i+8+2*nph*nc])
            nframes+=1
            progress(nframes)               

        # set actual number of frames
        self.Nframes = nframes
        
        #npxyz = np.frombuffer(b''.join(photons), dt_body)
        npxyz = np.frombuffer(b''.join(file_datab[i+8:i+8+2*nph*nc] 
                            for i,nph in zip(idxs,npht)), np.dtype('>u2'))
        self.photons=np.reshape(npxyz,(len(npxyz)//photoDim,photoDim))[:, photinfoMask] 
        self.idxs=np.insert(np.cumsum(np.array(npht)),0,0)
        #self.idxs=np.array(i//2-k for k,i in enumerate(idxs))
        message("\nRead+reshape " + str(nframes) + " frames", 1)        

    def getframeseries(self):
        '''
        Get :class:`photonpacket.frameseries` from :class:`file`

        Parameters
        ----------

        Returns
        ----------
        fs : :class:`photonpacket.frameseries`

        '''
        return frameseries(self.photons, self.idxs, self.shape, dtype=np.uint16)

    def getattribute(self, attr):
        if self.nameversion == 1:
            return self.getattributefromname(attr)
        elif self.nameversion == 2:
            try:
                return self.params[attr]
            except AttributeError:
                return False
        else:
            return False

    def getshapefromname(self):
        '''
        Get shape of frame

        Parameters
        ----------

        Returns
        ---------
        shape : tuple
            shape of frame

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        # search for shape info in a string
        s = re.search(r"-fs(?P<x>\d+)x(?P<y>\d+)", self.name)
        try:
            # extract x and y dimensions
            if s.group('x') and s.group('y'):
                return np.array([int(s.group('x')), int(s.group('y'))])
            else:
                return False
        except AttributeError:
            return False
        except IndexError:
            return False

    def getattributefromname(self, attr):
        '''
        Get value for a given attribute in filename

        Parameters
        ----------
        attr : string
            attribute name

        Returns
        ---------
        val : int or float
            attribute value

        See Also
        ---------

        Notes
        ---------

        Examples
        ---------
        '''
        # search for a given attribute
        # pattern: (attribute_name)[number,dots,+-][optional si prefix]
        pattern = r"-" + attr + "(?P<attr>[\d.]+)(?P<si>[yafnumkMGTZ]{,1})"
        s = re.search(pattern, self.name)
        try:
            if s.group('attr') and s.group('si') and siprefix(s.group('si')):
                return float(s.group('attr')) * siprefix(s.group('si'))
            elif s.group('attr'):
                return float(s.group('attr'))
            else:
                return False
        except AttributeError:
            return False
        except IndexError:
            return False

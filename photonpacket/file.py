import numpy as np
from frameseries import frameseries
import re
import os
from message import message, progress
import settings
from helpers import siprefix

# from scipy.sparse import dok_matrix, kron, csr_matrix, coo_matrix

class file:
    '''
    
    
    '''
    Nframes = 0
    name = ''
    path = ''
    nameversion = 0
    params = {}

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
        del self.params
        del self.photons
        del self.idxs
        
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
        # extract name of file from path
        (directory, name) = os.path.split(path)
        # remove file extension
        name = os.path.splitext(name)[0]

        # create file instance
        self = file(path, name)
        
        # try to read params xml file
        try:
            parse = settings.paramsparser
            self.params = parse(os.path.join(directory, name + '.' + settings.paramsext))
            self.nameversion = 2
            try:
                Nf = self.params['Nf']
            except AttributeError:
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
            print "Error: File present, but params parser not defined!"
            shape = self.getshapefromname()
            Nf = self.getattributefromname('Nf')
            self.nameversion = 1
        except Exception as e:
            # this means there was an unexpected error when parsing
            # we will proceed with automatic shape detection and no frame limit
            print "Unexpected Exception when parsing xml file (trying automatic shape detection): %s"%e
            shape = False
            Nf = False
            
        # try to set shape
        try:
            if isinstance(shape, np.ndarray):
                shapedetect = False
            else:
                shapedetect = True
        # if not possible, plan for shape detection
        except:
            shapedetect = True
            
        # try to extract number of frames from params or filename
        # if number given both in filename and as argument
        if 'Nframes' in kwargs and Nf:
            # select smaller
            maxframes = min(kwargs['Nframes'], Nf)
            frames_limit = True
        # number given only by argument
        elif 'Nframes' in kwargs:
            maxframes = kwargs['Nframes']
            frames_limit = True
        # number given only in params or filename
        elif Nf:
            maxframes = Nf
            frames_limit = True
        # number not given, turn off frame number limit
        else:
            maxframes = 0
            frames_limit = False
        
        if 'div' in kwargs:
            div = kwargs['div']
        else:
            div = 10
            
        nframes = 0
        # open file for binary reading
        f = open(path,'rb')
        
        frames = []
        empty_frame = np.empty(shape=(0, 2), dtype=np.uint16)
        while(True):
            # read number of photons in a frame
            # nxy = (number of photons, information per photon)
            nxy = np.fromfile(f, '>i4', 2)
            # break if file ended or acquired enough frames
            if nxy.size == 0 or (nframes >= maxframes and frames_limit):
                break
            N = nxy[0] * nxy[1]
            nframes += 1
            # read frame data

            if N > 0:
                # TODO: possibility of getting other info about photons
                # extract only photon positions
                img = np.fromfile(f, '>u2', N)
                frame = np.reshape(img/div, nxy)[:, :2]
            else:
                frame = empty_frame
            frames.append(frame)
            progress(nframes)
        # close file access
        f.close()
        # set actual number of frames
        self.Nframes = nframes
        
        message("\nRead " + str(nframes) + " frames", 1)
        
        self.photons = np.concatenate(frames)
        self.idxs = (np.r_[0, np.cumsum([frame.shape[0] for frame in frames])])
        
        if shapedetect:
            try:
                shape = np.max(self.photons, axis=0)
            except ValueError:
                print 'You must be joking... file contains 0 photons; aborting'
                return False
                     
        # set shape
        self.shape = shape*10/div
        return self

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
        
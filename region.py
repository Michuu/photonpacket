import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries


class region:

    def __init__(self):
        pass

    def plot(self):
        pass

    def isinregion(self):
        pass

    def getframeseries(self,fs,reshape = False):
        '''
        Select photon in region and obtain frameseries
        
        Parameters
        ---------
        fs : :class:`photonpacket.frameseries`
        
        reshape :  bool
            
        Returns
        ---------
        
        See Also
        ---------
        
        Notes
        ---------
        
        Examples
        ---------
        '''
        frames = []
        for frame in fs.frames:
            aux_frame = np.array(frame, dtype = np.uint32)
            mask = self.getmask(aux_frame)
            if reshape:
                frame = self.reshape(np.array(frame))
            frames.append(frame[mask])
        if reshape:
              return frameseries(frames, self.shape, cut=True)
        else:
              return frameseries(frames, fs.shape, cut=True)

    def getcounts(self,fs):
        '''
        Get total photon number in each frame
        
        Parameters
        ---------
        fs : :class:`photonpacket.frameseries`
            
        Returns
        ---------
        counts : :class:`numpy.ndarray`
            1D array of counts
        
        See Also
        ---------
        
        Notes
        ---------
        
        Examples
        ---------
        '''
        N=np.zeros((len(fs.frames)))
        for i, frame in enumerate(fs.frames):
            for photon in frame:
                if self.isinregion((photon[0],photon[1])):
                    N[i] += 1
        return N
    
    def reshape(self, frame):
        '''
        Reshape frane to gave (0,0) bottom-left corener
        
        Parameters
        ---------
        frane : :class:`numpy.ndarray`
            
        Returns
        ---------
        counts : :class:`numpy.ndarray`
            photon frame
        
        See Also
        ---------
        
        Notes
        ---------
        
        Examples
        ---------
        '''
        frame[:,0] -= self.corner[0]
        frame[:,1] -= self.corner[1]
        return frame
     

class circle(region):
    '''
    Circle region
    '''
    r = 0
    x0 = 0
    y0 = 0
    shape = []
    corner = np.array([])

    def __init__(self, r, (x0, y0)):
        self.r = r
        self.x0 = x0
        self.y0 = y0
        self.shape = [2*r, 2*r]
        self.corner = np.array([self.x0-self.r, self.y0-self.r])

    def plot(self,reshaped = False):
        ax=plt.gca()
        if reshaped:
            c1=plt.Circle((self.y0-self.corner[1],self.x0-self.corner[0]),self.r,fill=False,color='r') 
        else:
            c1=plt.Circle((self.y0,self.x0),self.r,fill=False,color='r')
        ax.add_artist(c1)

    def r2dist(self,R):
        return (self.x0-R[0])**2 + (self.y0-R[1])**2

    def isinregion(self,R):
        return (self.r2dist(R) < self.r**2)
                     
    def getmask(self, frame):
        frame[:, 0] -= self.x0
        frame[:, 1] -= self.y0
        mask = np.sum(frame**2,axis=1) < self.r**2
        return mask
        

class rect(region):
    '''
    Rectangle region
    '''
    # TODO: add rotation angle?
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0

    def __init__(self,(x0,y0),(x1,y1)):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def plot(self):
        v1 = np.array([[self.x0,self.x1],[self.y0,self.y0]])
        v2 = np.array([[self.x0,self.x0],[self.y0,self.y1]])
        v3 = np.array([[self.x1,self.x0],[self.y1,self.y1]])
        v4 = np.array([[self.x1,self.x1],[self.y1,self.y0]])
        plt.plot(v1[0],v1[1],color='r')
        plt.plot(v2[0],v2[1],color='r')
        plt.plot(v3[0],v3[1],color='r')
        plt.plot(v4[0],v4[1],color='r')

    def isinregion(self,R):
        # TODO: implement
        pass
         
    def getmask(self, frame):
        frame[:,0] = frame[:,0] - self.x0
        frame[:,1] = frame[:,1] - self.y0
        mask1 = frame[:,0] > self.x0
        mask2 = frame[:,1] > self.y0
        mask3 = frame[:,0] < self.x1
        mask4 = frame[:,1] < self.y1
        return mask1 * mask2 * mask3 * mask4

class ring(region):
    '''
    Ring region
    '''
    r1 = 0
    r2 = 0
    x0 = 0
    y0 = 0
    shape = []
    corner = np.array([])
    

    def __init__(self,r1,r2,(x0,y0)):
        self.r1 = r1
        self.r2 = r2
        self.x0 = x0
        self.y0 = y0
        self.shape = [2*r2, 2*r2]
        self.corner = np.array([self.x0-self.r2,self.y0-self.r2])

    def plot(self, reshaped = False):
        ax=plt.gca()
        if reshaped:
            c1=plt.Circle((self.y0-self.corner[1],self.x0-self.corner[0]),self.r1,fill=False,color='r')
            c2=plt.Circle((self.y0-self.corner[1],self.x0-self.corner[0]),self.r2,fill=False,color='g')
        else:
            c1=plt.Circle((self.y0,self.x0),self.r1,fill=False,color='r')
            c2=plt.Circle((self.y0,self.x0),self.r2,fill=False,color='g')
        ax.add_artist(c1)
        ax.add_artist(c2)

    def r2dist(self,R):
        return (self.x0-R[0])**2+(self.y0-R[1])**2

    def isinregion(self,R):
        return ((self.r2dist(R)>self.r1**2) and (self.r2dist(R)<self.r2**2))
          
    def getmask(self, frame):
        frame[:,0] = frame[:,0]-self.x0
        frame[:,1] = frame[:,1]-self.y0
        mask1 = np.sum(frame**2,axis=1) > self.r1**2
        mask2 = np.sum(frame**2,axis=1) < self.r2**2
        return mask1 * mask2
            

class ellpise(region):
    '''
    Ellipse region
    '''
    a = 0
    b = 0
    x0 = 0
    y0 = 0
    angle = 0
    frames = []
    shape = []
    corner = np.array([])
    

    def __init__(self,a,b,(x0,y0),angle):
        self.a = b
        self.a = b
        self.x0 = x0
        self.y0 = y0
        self.angle = angle
        # TODO: rewrite shape calc
        self.shape = [2*a, 2*b]
        # TODO: rewrite corner calc
        self.corner = np.array([self.x0-self.a,self.y0-self.b])

    def plot(self):
        ax=plt.gca()
        e=plt.Ellipse(xy=(self.y0,self.x0),width=self.a,height=self.b,
                      angle=self.angle,fill=False,color='r')
        ax.add_artist(e)

    def r2dist(self,R):
        return (self.x0-R[0])**2+(self.y0-R[1])**2

    def isinregion(self,R):
        # TODO: rewrite
        return ((self.r2dist(R)>self.r1**2) and (self.r2dist(R)<self.r2**2))
    
    def getmask(self, frame):
        pass
    
class halfcircle(region):
    '''
    Halfcircle region
    '''
    r1 = 0
    angle = 0
    x0 = 0
    y0 = 0
    frames = []
    shape = []
    corner = np.array([])
    

    def __init__(self,r,angle,(x0,y0)):
        self.r=r
        self.angle=angle
        self.x0=x0
        self.y0=y0
        # TODO: rewrite shape calc
        self.shape = [2*r, 2*r]
        # TODO: rewrite corner calc
        self.corner = np.array([self.x0-self.r2,self.y0-self.r2])

    def plot(self):
        # TODO: rewrite plotting
        ax=plt.gca()
        c1=plt.Circle((self.y0,self.x0),self.r1,fill=False,color='r')
        ax.add_artist(c1)
        c2=plt.Circle((self.y0,self.x0),self.r2,fill=False,color='g')
        ax.add_artist(c2)

    def r2dist(self,R):
        return (self.x0-R[0])**2+(self.y0-R[1])**2

    def isinregion(self,R):
        # TODO: rewrite
        return ((self.r2dist(R)>self.r1**2) and (self.r2dist(R)<self.r2**2))
    
    def getmask(self, frame):
        pass





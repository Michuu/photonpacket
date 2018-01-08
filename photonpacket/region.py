import numpy as np
from matplotlib import pyplot as plt
from frameseries import frameseries
from frameutils.arraysplit import arraysplit

class region(object):
    component_regions = ()
    logic = None
    corner = np.array([])

    def __init__(self, components_regions, logic):
        self.component_regions = components_regions
        self.logic = logic
        if component_regions.__class__ == tuple:
            self.corner[0] = min(component_regions[0].corner[0], component_regions[1].corner[0])
            self.corner[1] = min(component_regions[0].corner[1], component_regions[1].corner[1])
        else:
            self.corner = component_regions.corner

    def __and__(self, other):
        return region((self, other), 'and')

    def __or__(self, other):
        return region((self, other), 'or')

    def __xor__(self, other):
        return region((self, other), 'xor')

    def __invert__(self):
        return region((self), 'not')

    def getmask(self, frame):
        if self.logic == 'and':
            return self.component_regions[0].getmask(frame.copy()) & self.component_regions[1].getmask(frame.copy())
        elif self.logic == 'or':
            return self.component_regions[0].getmask(frame.copy()) | self.component_regions[1].getmask(frame.copy())
        elif self.logic == 'xor':
            return self.component_regions[0].getmask(frame.copy()) ^ self.component_regions[1].getmask(frame.copy())
        elif self.logic == 'not':
            return np.logical_not(self.component_regions.getmask(frame.copy()))

    def plot(self):
        if self.component_regions.__class__ == tuple:
            for reg in self.component_regions:
                reg.plot()
        else:
            self.component_regions.plot()

    def isinregion(self):
        pass

    def getframeseries(self, fs, reshape = False):
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

        Notesa
        ---------

        Examples
        ---------
        '''
        cc_frames = np.array(fs.concat, dtype=fs.dtype)
        csum = np.cumsum(fs.N, dtype=np.uint32)
        mask = self.getmask(cc_frames.copy())
        cmask = np.cumsum(mask)
        cmask = np.insert(cmask, 0, 0)
        cN = cmask[csum]
        cN = np.insert(cN, 0, 0)
        if reshape:
            cc_frames = self.reshape(cc_frames)
            return frameseries(arraysplit(cc_frames[mask], cN)[1:-1], self.shape, cut=False)
        else:
            return frameseries(arraysplit(cc_frames[mask], cN)[1:-1], fs.shape, cut=False)

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

        cc_frames = np.array(fs.concat, dtype=np.uint32)
        csum = np.cumsum(fs.N)

        mask = self.getmask(cc_frames)

        cmask = np.cumsum(mask)
        cmask = np.insert(cmask, 0, 0)

        # cmask length = total number of photons, csum length = total number of frames
        # last element of csum = total number of photons
        # last element of cmask = total number of photons in region
        # we are selecting elements of cmask at points given by csum
        # from this we obtain a cumsum of photon counts cN inside region
        cN = cmask[csum]

        cN = np.insert(cN, 0, 0)

        # differentiation of cumsum photon photon counts from region
        # giving counts in this region
        N = cN - np.roll(cN, 1)
        return N[1:]


    def reshape(self, frame):
        '''
        Reshape frame to have (0,0) bottom-left corner

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
        '''

        Paramterers
        ---------
        r : int
            radius
        (x0, y0) : (int, int)
            position of center

        '''
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
    shape = []
    corner = np.array([])

    def __init__(self, (x0,y0), (x1,y1)):
        '''

        Paramterers
        ---------
        (x0, y0) : (int, int)
            bottom left corner
        (x1, y1) : (int, int)
            top right corner

        '''
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.shape = [x1-x0, y1-y0]
        self.corner = np.array([self.x0, self.y0])

    def plot(self):
        v1 = np.array([[self.y0,self.y1],[self.x0,self.x0]])
        v2 = np.array([[self.y0,self.y0],[self.x0,self.x1]])
        v3 = np.array([[self.y1,self.y0],[self.x1,self.x1]])
        v4 = np.array([[self.y1,self.y1],[self.x1,self.x0]])
        plt.plot(v1[0],v1[1],color='r')
        plt.plot(v2[0],v2[1],color='r')
        plt.plot(v3[0],v3[1],color='r')
        plt.plot(v4[0],v4[1],color='r')

    def isinregion(self,R):
        # TODO: implement
        pass

    def getmask(self, frame):
        # frame[:,0] = frame[:,0] - self.x0
        # frame[:,1] = frame[:,1] - self.y0
        mask1 = frame[:,0] > self.x0
        mask2 = frame[:,1] > self.y0
        mask3 = frame[:,0] < self.x1
        mask4 = frame[:,1] < self.y1
        return mask1 * mask2 * mask3 * mask4

class rect2(rect):
    '''
    Rectangle defined by center
    '''

    def __init__(self, (xc, yc), (a, b)):
        '''

        Paramterers
        ---------
        (xc, yc) : (int, int)
            position of center
        (a, b) : (int, int)
            horizontal and vertical extent

        '''
        x0 = xc - a
        y0 = yc - b
        x1 = xc + a
        y1 = yc + b
        super(rect2, self).__init__((x0, y0), (x1, y1))

class square(rect):
    '''
    Square region
    '''
    def __init__(self, a, (xc, yc)):
        '''

        Paramterers
        ---------
        a : int
            extent
        (xc, yc) : (int, int)
            position of center

        '''
        x0 = xc - a
        y0 = yc - a
        x1 = xc + a
        y1 = yc + a
        super(square, self).__init__((x0, y0), (x1, y1))

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
        '''

        Paramterers
        ---------
        r1 : int
            inner radius
        r2 : int
            outer radius
        (x0, y0) : (int, int)
            position of center

        '''
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
        '''

        Paramterers
        ---------
        a : int
            semi-major axis
        b : int
            semi-minor axis
        (x0,y0) : (int, int)
            position of center
        angle : float
            rotation angle (in radians); not implemented

        '''
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
    Not implemented
    '''
    r1 = 0
    x0 = 0
    y0 = 0
    frames = []
    shape = []
    corner = np.array([])


    def __init__(self,r,angle,(x0,y0)):
        '''

        Paramterers
        ---------
        r : int
            radius
        angle : float
            rotation angle (in radians)
        (x0, y0) : (int, int)
            position of center

        '''
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





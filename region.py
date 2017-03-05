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

    def getframeseries(self,fs,reshape=False):
        self.frames = []
        for frame in fs.frames:
            i=0
            for photon in frame:
                if self.isinregion((photon[0],photon[1])):
                    if reshape:
                          photon = photon - self.corner
                    if i==0:
                        newframe=np.array([photon])
                    else:
                        newframe=np.append(newframe,np.array([photon]),axis=0)
                    i=i+1
            if i == 0:
                newframe=np.array([])
            self.frames.append(newframe)
        if reshape:
              return frameseries(self.frames, self.shape)
        else:
              return frameseries(self.frames, fs.shape)

    def getcounts(self,fs):
        N=np.zeros((len(fs.frames)))
        for i, frame in enumerate(fs.frames):
            for photon in frame:
                if self.isinregion((photon[0],photon[1])):
                    N[i]=N[i]+1
        return N



class circle(region):
    r = 0
    x0 = 0
    y0 = 0
    frames = []
    shape = []
    corner = np.array([])

    def __init__(self,r,(x0,y0)):
        self.r=r
        self.x0=x0
        self.y0=y0
        self.shape = [2*r, 2*r]
        self.corner = np.array([self.x0-self.r, self,y0-self.r])

    def plot(self):
        ax=plt.gca()
        c1=plt.Circle((self.y0,self.x0),self.r,fill=False,color='r')
        ax.add_artist(c1)

    def r2dist(self,R):
        return (self.x0-R[0])**2+(self.y0-R[1])**2

    def isinregion(self,R):
        return (self.r2dist(R)<self.r**2)

class rect(region):
    # TODO: add rotation angle?
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0

    def __init__(self,(x0,y0),(x1,y1)):
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1

    def plot(self):
        # TODO: implement
        pass

    def isinregion(self,R):
        # TODO: implement
        pass

class ring(region):
    r1 = 0
    r2 = 0
    x0 = 0
    y0 = 0
    frames = []
    shape = []
    corner = np.array([])
    

    def __init__(self,r1,r2,(x0,y0)):
        self.r1=r1
        self.r2=r2
        self.x0=x0
        self.y0=y0
        self.shape = [2*r2, 2*r2]
        self.corner = np.array([self.x0-self.r2,self.y0-self.r2])

    def plot(self):
        ax=plt.gca()
        c1=plt.Circle((self.y0,self.x0),self.r1,fill=False,color='r')
        ax.add_artist(c1)
        c2=plt.Circle((self.y0,self.x0),self.r2,fill=False,color='g')
        ax.add_artist(c2)

    def r2dist(self,R):
        return (self.x0-R[0])**2+(self.y0-R[1])**2

    def isinregion(self,R):
        return ((self.r2dist(R)>self.r1**2) and (self.r2dist(R)<self.r2**2))

class ellpise(region):
    a = 0
    b = 0
    x0 = 0
    y0 = 0
    angle = 0
    frames = []
    shape = []
    corner = np.array([])
    

    def __init__(self,a,b,(x0,y0),angle):
        self.a=b
        self.a=b
        self.x0=x0
        self.y0=y0
        self.angle=angle
        # TODO: rewrite shape calc
        self.shape = [2*a, 2*b]
        # TODO: rewrite corner calc
        self.corner = np.array([self.x0-self.a,self.y0-self.b])

    def plot(self):
        ax=plt.gca()
        e=plt.Ellipse(xy=(self.y0,self.x0),width=self.a,height=self.b,angle=self.angle,fill=False,color='r')
        ax.add_artist(e)

    def r2dist(self,R):
        return (self.x0-R[0])**2+(self.y0-R[1])**2

    def isinregion(self,R):
        # TODO: rewrite
        return ((self.r2dist(R)>self.r1**2) and (self.r2dist(R)<self.r2**2))
    
class halfcircle(region):
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





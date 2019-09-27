import sys
sys.path.append('C:\\Users\\Hamamatsu\\Documents\\Repozytoria\\analiza\\')
from matplotlib import pyplot as plt
import numpy as np

import photonpacket as pp
pp.settings.overwrite = False
from mpl_toolkits.mplot3d import Axes3D
from scipy.misc import factorial
#%%
Nframes=1000000
f=pp.file.read(r"H:\dane\1703 testy MOTa\11 04\pom2-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw0.00G-dr6.02G-pw0.0m-pr0.0m-fs150x700-nf300k-T0-fB0-fT0k-II0.00-sr0.dat",Nframes=Nframes)
fs=f.getframeseries()

#%%
print('accumulating')
c1 = pp.circle(60,(60,241))
c2 = pp.circle(60,(61,540))
d=fs.accumframes()
plt.clf()
plt.imshow(d)
c1.plot()
c2.plot()
plt.show()
#%%
d=fs2.accumframes()
plt.imshow(d)
#%%
fs1 = c1.getframeseries(fs, reshape=True)
fs2 = c2.getframeseries(fs, reshape=True)
#%%
c3 = pp.circle(4,(55,64))
c4 = pp.circle(4,(60,60))
fs3 = c3.getframeseries(fs1, reshape=True)
fs4 = c4.getframeseries(fs2, reshape=True)
#%%
print(pp.stat1d.mean(fs4)*pp.stat1d.mean(fs3)*300000)
print(pp.stat1d.mean(fs4)*300000*0.1*0.3)
#%%
print('calculating statistics')
print(pp.stat2d.g2(fs3,fs4))
H=pp.stat2d.joint(fs3,fs4)
pp.stat2d.plotjoint(H,showvalues=True)
print(H[0][0,1])
print(H[0][1,0])
print(H[0][1,1])
plt.show()
#%%
print('calculating statistics')
print(pp.stat2d.g2(fs1,fs2))
H=pp.stat2d.joint(fs1,fs2)
pp.stat2d.plotjoint(H,showvalues=True)
print(H[0][0,1])
print(H[0][1,0])
print(H[0][1,1])
plt.show()
#%%
print('plotting')
plt.clf()
c1.plot()
c2.plot()
d1=fs1.accumframes()
d2=fs2.accumframes()
plt.imshow(d)
plt.show()
#%%
print('coinc')
plt.clf()
d=pp.accum.accumcoinc(fs1,fs2)
plt.imshow(np.sum(d,axis=(0,1)))
plt.show()
#%%
print('calculating statistics')
print(pp.stat2d.g2(fs1,fs2))
H=pp.stat2d.joint(fs1,fs2)
pp.stat2d.plotjoint(H,showvalues=True)
print(H[0][0,1])
print(H[0][1,0])
print(H[0][1,1])
plt.show()
#%%
d1=fs1.accumframes()
d2=fs2.accumframes()
signs=(True,False)
dc=pp.accum.coinchist(fs1,fs2,signs)
dac=pp.accum.acchist(d1,d2,signs,Nframes=fs.len())
#dac=np.array(dac,dtype=np.float64)/float(fs.len())
#dac=dac/np.sum(dac)
#d=np.array(d,dtype=np.float64)
#print np.sum(d)
print(np.sum(dc-dac))
plt.imshow(dc)
plt.show()
plt.imshow(dac)
plt.show()
plt.imshow(dc-dac)
plt.show()
#%%
plt.plot(dc[:,119])
plt.plot(dac[:,119])
#%%
bins = np.arange(np.max(fs1.N)+2)
h1=np.histogram(fs1.N, bins=bins,normed=True)
plt.bar(h1[1][:-1], h1[0],log=True)
n1=np.mean(fs1.N)
coh = lambda k: n1**k * np.exp(-n1)/factorial(k)
plt.plot(h1[1][:-1],coh(h1[1][:-1]),ls="",marker='o',color='r')
plt.show()
#%%
bins = np.arange(np.max(fs2.N)+2)
h2=np.histogram(fs2.N, bins=bins,normed=True)
plt.bar(h2[1][:-1], h2[0],log=True)
n2=np.mean(fs2.N)
coh = lambda k: n2**k * np.exp(-n2)/factorial(k)
plt.plot(h2[1][:-1],coh(h2[1][:-1]),ls="",marker='o',color='r')
plt.show()
#%%
hj=np.tensordot(h1[0],h2[0],axes=0)
X, Y = np.meshgrid(h2[1][:-1], h1[1][:-1])
plt.pcolormesh(X, Y, hj)
plt.colorbar()
plt.show()
bins1 = np.arange(np.max(fs1.N)+2)
bins2 = np.arange(np.max(fs2.N)+2)
hj2=np.histogram2d(fs1.N,fs2.N,bins = [bins1,bins2],normed=True)
X, Y = np.meshgrid(hj2[2][:-1], hj2[1][:-1])
plt.pcolormesh(X, Y, hj2[0])
plt.colorbar()
plt.show()
plt.pcolormesh(X, Y, (hj2[0]-hj)*fs.len())
plt.colorbar()
plt.show()
#%%
xpos, ypos = X, Y
xpos = xpos.flatten('F')
ypos = ypos.flatten('F')
zpos = np.zeros_like(xpos)

dx = 0.5 * np.ones_like(zpos)
dy = dx.copy()
dz = (hj2[0]).flatten()
ax=plt.gca(projection='3d')
ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
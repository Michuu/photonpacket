import sys
sys.path.append('/Users/michal/Repozytoria')
from matplotlib import pyplot as plt
import numpy as np

import photonpacket as pp
#%%
nph = 10
p1 = 0.8
p2 = 0.96
d = 80
shape = (d,d)
Nframes = 10000
frames1 = []
frames2 = []
Nphot = np.random.poisson(lam = nph, size = Nframes)
for i in np.arange(Nframes):
    frame1 = np.random.randint(0,d,size=(Nphot[i],2),dtype=np.uint16)
    mask1 = np.random.choice([False, True],size=Nphot[i],p=[p1,1-p1])
    frame2 = frame1 + np.random.normal(0,5,size=(Nphot[i],2))
    mask2 = np.random.choice([False, True],size=Nphot[i],p=[p2,1-p2])
    frames1.append(frame1[mask1])
    frames2.append(frame2[mask2])

fs1 = pp.frameseries(frames1,shape)
fs2 = pp.frameseries(frames2,shape)
#%%
# accumulating
d=fs1.accumframes()
plt.clf()
plt.imshow(d)
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
signs=(False,False)
d=pp.accum.coinchist(fs1,fs2,signs)
dac=pp.accum.acchist(d1,d2,signs)
#if not signs[0]:
#    d2=np.flip(d2,axis=0)
#if not signs[1]:
#    d2=np.flip(d2,axis=1)
#dac=convolve2d(d1,d2)
dac=dac/float(fs1.len())
print(np.sum(d-dac))
plt.imshow(d)
plt.show()
plt.imshow(dac)
plt.show()
plt.imshow(d-dac)
plt.show()
#%%
np.mean(fs1.N*fs2.N-np.mean(fs1.N)*np.mean(fs2.N))/(np.std(fs1.N)*np.std(fs2.N))
#%%
print('coinc')
plt.clf()
d=pp.accum.accumcoinc(fs1,fs2,method='bincount')
plt.imshow(np.sum(d,axis=(0,1)))
plt.show()
#%%
h=pp.stat1d.stat(fs1)
pp.stat1d.plotstat(h)
import sys
sys.path.append('C:\\Users\\Hamamatsu\\Documents\\Repozytoria\\analiza\\')
from matplotlib import pyplot as plt
import numpy as np

import photonpacket as pp
#%%
Nframes=10000
f=pp.file.read(r"H:\dane\1606 EPR korelacje fotonowe\0603 pomiary cross-corr\pom1_farSfarAS_Raman-AOMw441-nf300k-las11.0-tg4.55u-tw2.00u-tr2.00u-tmem250n-fs250x600-sr0.dat",Nframes=Nframes)
fs=f.getframeseries()

#%%
print 'accumulating'
d=fs.accumframes()
plt.clf()
plt.imshow(d)
plt.show()
#%%
print 'selecting'
c1 = pp.ring(10,40,(55,107))
fs1 = c1.getframeseries(fs)

c2 = pp.ring(10,40,(56,449))
fs2 = c2.getframeseries(fs)
#%%
c1.plot()
c2.plot()
plt.imshow(d)
plt.show()
#%%
# select with reshaping
c1 = pp.ring(15,40,(55,107))
fs1 = c1.getframeseries(fs, reshape=True)

c2 = pp.ring(15,40,(56,449))
fs2 = c2.getframeseries(fs, reshape=True)
#%%
# select with reshaping
c1 = pp.circle(40,(130,160))
fs1 = c1.getframeseries(fs, reshape=False)

c2 = pp.circle(40,(135,440))
fs2 = c2.getframeseries(fs, reshape=False)
#%%
print 'plotting'
plt.clf()
c1.plot()
c2.plot()
d1=fs1.accumframes()
d2=fs2.accumframes()
plt.imshow(d1)
plt.show()
#%%
print 'coinc'
plt.clf()
d=pp.accum.accumcoinc(fs1,fs2)
plt.imshow(np.sum(d,axis=(0,1)))
plt.show()
#%%
print 'calculating statistics'
print pp.stat2d.g2(fs1,fs2)
H=pp.stat2d.joint(fs1,fs2)
pp.stat2d.plotjoint(H)
print H[0][0,1]
print H[0][1,0]
print H[0][1,1]
plt.show()
#%%
d1=fs1.accumframes()
d2=fs2.accumframes()
signs=(True,True)
d=pp.accum.coinchist(fs1,fs2,signs)
dac=pp.accum.acchist(d1,d2,signs)
dac=np.array(dac,dtype=np.float64)/float(fs.len())
#dac=dac/np.sum(dac)
d=np.array(d,dtype=np.float64)
print np.sum(d)
print np.sum(dac)
plt.imshow(d)
plt.show()
plt.imshow(dac)
plt.show()
plt.imshow(d-dac)
plt.show()

#%%
'''
cc=f.accumcoinc((100,600))
cc=np.mean(cc,axis=(2,3))
plt.imshow(cc)
plt.show()
'''
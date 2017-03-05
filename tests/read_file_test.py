import sys
sys.path.append('/Users/michal/Repozytoria')
from matplotlib import pyplot as plt
import numpy as np

import photonpacket as pp
#%%
f=pp.file.read('/Users/michal/Repozytoria/photonpacket/pom2-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw0.00G-dr6.02G-pw0.0m-pr0.0m-fs100x600-nf50k-T0-fB0-fT0k-II2.70-sr1.dat')
fs=f.getframeseries()

#%%
print 'accumulating'
d=fs.accumframes()
plt.clf()
plt.imshow(d)
plt.show()
#%%
print 'selecting'
c1 = pp.ring(10,40,(50,130))
fs1 = c1.getframeseries(fs)

c2 = pp.ring(10,40,(50,483))
fs2 = c2.getframeseries(fs)
#%%
# select with reshaping
c1 = pp.ring(3,40,(50,130))
fs1 = c1.getframeseries(fs, reshape=True)

c2 = pp.ring(3,40,(50,483))
fs2 = c2.getframeseries(fs, reshape=True)
#%%
print 'plotting'
plt.clf()
#c1.plot()
#c2.plot()
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
signs=(False,True)
d=pp.accum.coinchist(fs1,fs2,signs)
dac=pp.accum.acchist(d1,d2,signs)
dac=dac/np.sum(dac)
d=d/np.sum(d)
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
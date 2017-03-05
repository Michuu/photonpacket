import sys
sys.path.append('/Users/michal/Repozytoria')
from matplotlib import pyplot as plt
import numpy as np

import PhotonPacket as pp
f=pp.file.readall('/Users/michal/Repozytoria/PhotonPacket/pom2-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw0.00G-dr6.02G-pw0.0m-pr0.0m-fs100x600-nf50k-T0-fB0-fT0k-II2.70-sr1.dat')
fs=f.getframeseries()

#%%
print 'accumulating'
d=fs.accumframes()
plt.clf()
plt.imshow(d)
plt.show()
#%%
print 'selecting'
c1 = pp.ring(10,50,(50,130))
fs1 = c1.getframeseries(fs)

c2 = pp.ring(10,50,(50,483))
fs2 = c2.getframeseries(fs)

#%%
print 'plotting'
plt.clf()
c1.plot()
c2.plot()
d=fs1.accumframes()+fs2.accumframes()
plt.imshow(d)
plt.show()
#%%
print 'coinc'
plt.clf()
d=pp.accum.accumcoinc(fs1,fs2)
plt.imshow(np.sum(d,axis=(2,3)))
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
'''
cc=f.accumcoinc((100,600))
cc=np.mean(cc,axis=(2,3))
plt.imshow(cc)
plt.show()
'''
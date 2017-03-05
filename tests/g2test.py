import sys
sys.path.append('/Users/michal/Repozytoria')
from matplotlib import pyplot as plt
import numpy as np

import PhotonPacket as pp
print 'reading'
f=pp.file.readall('/Users/michal/Repozytoria/PhotonPacket/pom2-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw0.00G-dr6.02G-pw0.0m-pr0.0m-fs100x600-nf50k-T0-fB0-fT0k-II2.70-sr1.dat')
fs=f.getframeseries()

print 'accumulating'
d=fs.accumframes()

r=20
print 'selecting'
Na=np.empty((r,r,len(fs.frames)))
for i in range(r):
    print i
    for j in range(r):
        c1 = pp.circle(11,(56+i,132+j))
        c1.plot()
        Na[i,j,:] = c1.getcounts(fs)

c2 = pp.circle(11,(29,483))
c2.plot()
N2 = c2.getcounts(fs)

print 'plotting'
plt.imshow(d)
plt.show()

res=np.empty((r,r))
print 'calculating statistics'
for i in range(r):
    for j in range(r):
        res[i,j]=pp.stat2d.g2fromcounts(Na[i,j],N2)

print res

plt.imshow(res,interpolation='none')
plt.show()

'''
cc=f.accumcoinc((100,600))
cc=np.mean(cc,axis=(2,3))
plt.imshow(cc)
plt.show()
'''
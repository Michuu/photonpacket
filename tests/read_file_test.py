import sys
sys.path.append('/Users/michal/Repozytoria')
from matplotlib import pyplot as plt
import numpy as np
import time

import photonpacket as pp
pp.settings.verbose = 2
pp.settings.overwrite = True
#%%
Nframes=10000
f=pp.file.read('/Users/michal/data/pom1_farSfarAS_Raman-AOMw441-nf300k-las11.0-tg4.55u-tw2.00u-tr2.00u-tmem250n-fs250x600-sr0.dat',Nframes=Nframes)
# pom1_nearSnearAS-Raman-AOMw441-nf300k-las11.0-tg5.55u-tw3.00u-tr2.00u-tmem-250n-fs250x600-sr0.dat
#f=pp.file.read('/Volumes/E/pom1_farSfarAS_Raman-AOMw441-nf300k-las11.0-tg4.55u-tw2.00u-tr2.00u-tmem250n-fs250x600-sr0.dat',Nframes=10000)
fs=f.getframeseries()


#%%
# accumulating
d=fs.accumframes()
plt.clf()
plt.imshow(d)
plt.show()
#%%
# selecting circles
c1 = pp.circle(40,(130,160))
fs1 = c1.getframeseries(fs)

c2 = pp.circle(40,(135,440))
fs2 = c2.getframeseries(fs)
#%%
# selecting rings
c1 = pp.ring(10,40,(50,125))
fs1 = c1.getframeseries(fs)

c2 = pp.ring(10,40,(50,283))
fs2 = c2.getframeseries(fs)
#%%
# selecting rings with reshaping
c1 = pp.ring(40,45,(50,125))
fs1 = c1.getframeseries(fs, reshape=True)

c2 = pp.ring(40,45,(50,283))
fs2 = c2.getframeseries(fs, reshape=True)
#%%
# selecting circles with reshaping
c1 = pp.circle(5,(130,160))
fs1 = c1.getframeseries(fs, reshape=True)

c2 = pp.circle(5,(135,440))
fs2 = c2.getframeseries(fs, reshape=True)
#%%
# plotting with reshaping
plt.clf()
c1.plot(reshaped = True)
c2.plot(reshaped = True)
d1=fs1.accumframes()
d2=fs2.accumframes()
plt.imshow(d2)
plt.show()
#%%
# selecting rectangle
# na razie totalnie nie dziala
# TODO: naprawic rectangle - patrz plik region.py
r1 = pp.rect((50,110),(60,130))
r1.plot()
fs1 = r1.getframeseries(fs)
plt.imshow(fs1.accumframes())
plt.show()
#%%
# plotting (without reshaping)
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
m1=int(round(time.time() * 1000))
d=pp.accum.accumcoinc(fs1,fs2,method='bincount')
m2=int(round(time.time() * 1000))
plt.imshow(np.sum(d,axis=(0,1)))
plt.show()

plt.clf()
m3=int(round(time.time() * 1000))
d=pp.accum.accumcoinc(fs1,fs2,method='accum')
m4=int(round(time.time() * 1000))
plt.imshow(np.sum(d,axis=(0,1)))
plt.show()

print m2-m1
print m4-m3
#%%
#print 'coinc'
#c1 = pp.circle(40,(130,160))
#c2 = pp.circle(40,(135,440))

#m1=int(round(time.time() * 1000))
#fs1 = c1.getframeseries(fs, reshape=True)
#fs2 = c2.getframeseries(fs, reshape=True)
d=pp.accum.accumcoinc(fs1,fs1)
#m2=int(round(time.time() * 1000))

plt.imshow(np.sum(d,axis=(0,1)))
plt.show()
#%%

m3=int(round(time.time() * 1000))
d=pp.accum.accumcoincinplace(fs,c1,c2)
m4=int(round(time.time() * 1000))

plt.imshow(np.sum(d,axis=(0,1)))
plt.show()

print m2-m1
print m4-m3
#%%

c1 = pp.circle(5,(135,160))
fs1 = c1.getframeseries(fs, reshape=True)

c2 = pp.circle(5,(135,440))
fs2 = c2.getframeseries(fs, reshape=True)

print 'calculating statistics'
print pp.stat2d.g2(fs1,fs2)
H=pp.stat2d.joint(fs1,fs2)
pp.stat2d.plotjoint(H,showvalues=False)
print H[0][0,1]
print H[0][1,0]
print H[0][1,1]
plt.show()
#%%
d1=fs2.accumframes()
d2=fs2.accumframes()
signs=(0,0)
d=pp.accum.coinchist(fs2,fs2,signs)
dac=pp.accum.acchist(d1,d2,signs)
#if not signs[0]:
#    d2=np.flip(d2,axis=0)
#if not signs[1]:
#    d2=np.flip(d2,axis=1)
#dac=convolve2d(d1,d2)
dac=dac/float(fs1.len())
#plt.imshow(d-dac)
plt.plot(np.sum(d-dac,axis=0))
plt.show()
#%%
plt.imshow(dac)
plt.show()
#%%
plt.imshow(d)
plt.show()

#%%
'''
cc=f.accumcoinc((100,600))
cc=np.mean(cc,axis=(2,3))
plt.imshow(cc)
plt.show()
'''
#%%
t1=int(round(time.time() * 1000))
i=0
cframes = []
for frame in fs1.frames:
    if i%10000==0:
        print i
    frame2 = fs2.frames[i]
    if len(frame2) != 0 and len(frame) != 0:
        #cframe = np.hstack((
        #                np.dstack(np.meshgrid(frame[:,0], frame2[:,0])).reshape(-1, 2),
        #                np.dstack(np.meshgrid(frame[:,1], frame2[:,1])).reshape(-1, 2)
        #                ))
        cfx=np.meshgrid(frame[:,0],frame2[:,0])
        cfy=np.meshgrid(frame[:,1],frame2[:,1])
        cframe2 = np.zeros(shape=(len(cfx[0].flatten()),2),dtype=np.uint16)
        if signs[0]:
            cframe2[:,0] = cfx[0].flatten() + cfx[1].flatten()
        else:
            cframe2[:,0] = cfx[0].flatten() - cfx[1].flatten() + fs2.shape[0]
        if signs[1]:
            cframe2[:,1] = cfy[0].flatten() + cfy[1].flatten()
        else:
            cframe2[:,1] = cfy[0].flatten() - cfy[1].flatten() + fs2.shape[1]
        cframes.append(cframe2)
    i = i + 1
t2=int(round(time.time() * 1000))
accum = bincountnd(np.concatenate(cframes),(fs1.shape[0]+fs2.shape[0]-1,fs1.shape[1]+fs2.shape[1]-1))
t3=int(round(time.time() * 1000))
print t2-t1
print t3-t2
#%%
h=pp.stat1d.stat(fs2)
pp.stat1d.plotstat(h)
#%%
plt.plot(np.sum(d,axis=0))
plt.plot(np.sum(dac,axis=0))
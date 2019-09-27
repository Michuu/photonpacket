import sys
sys.path.append('C:\\Users\\Hamamatsu\\Documents\\Repozytoria\\analiza\\')
from matplotlib import pyplot as plt
import numpy as np

import photonpacket as pp
#%%
pp.settings.overwrite = False
#%%
Nframes=1000000
f=pp.file.read(r"H:\dane\1703 testy MOTa\11 04\pom2-tw10.00u-tmem0.00u-tr10.00u-tg35.00u-dw0.00G-dr6.02G-pw0.0m-pr0.0m-fs150x700-nf300k-T0-fB0-fT0k-II0.00-sr0.dat",Nframes=Nframes)
fs=f.getframeseries()
#%%
print('accumulating')
d=fs.accumframes()
c2 = pp.circle(5,(55,550))
#c2.plot()
N2 = c2.getcounts(fs)

r=10
print('selecting')
res=np.empty((r,r))
#Na=np.empty((r,r,len(fs.frames)))
for i in range(r):
    for j in range(r):
        c1 = pp.circle(5,(46+2*(i-r/2),251+2*(j-r/2)))
        print(str(i)+','+str(j))
        res[i,j] = pp.stat2d.g2(c1.getcounts(fs),N2)

#%%
print('plotting')
plt.imshow(d)
plt.show()
#%%
res=np.empty((r,r))
print('calculating statistics')
for i in range(r):
    for j in range(r):
        res[i,j]=pp.stat2d.g2(Na[i,j],N2)
        
print(res)
#%%
print(res)
plt.imshow(res[:,:],interpolation='none')
plt.colorbar()
plt.show()
#%%
'''
cc=f.accumcoinc((100,600))
cc=np.mean(cc,axis=(2,3))
plt.imshow(cc)
plt.show()
'''
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:45:48 2019

@author: wwasil
"""


#%%
from photonpacket.lvjson3 import getAlljsons
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
alljsons=getAlljsons(folder,'3.05')
#% %
from photonpacket.lvjson3 import jsonToClass
t,d=jsonToClass('305_autogen',alljsons[1][1])    
print('-'*4)
print(t)
#print(d)
#%%
o=alljsons[1][1]['ctrl_params'][0]
t,d=jsonToClass('ctrl_param',o)    
print('-'*4)
print(t)

#%%
import numpy as np
from photonpacket.lvjson3 import LV305, getAlljsons        
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
#jsobjs=[LV305(js) for jn, js in getAlljsons(folder+"ciemne2",'3.05')]
jsobjs=[LV305(js) for jn, js in getAlljsons(folder+"305a",'3.05')]
#% %
for o in jsobjs[0:]:
    #print('pxy',o.file_names.positions)
    #print('pnn',o.file_names.indexes)
    #o.pathreplace(r'F:\dane',r"\\Astrosciema\f\dane") 
    o.pathshift(r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu\305a-sr0.pxy")
    dtype = np.dtype('>u2')  
    with open(o.file_names.positions,'rb') as f:
            data=np.frombuffer(f.read(), dtype) 
            print(data[:14])
            #r=(data.reshape((data.shape[0]//2,2),order='C'))
            r=(data.reshape((-1,2),order='C'))
            print(np.transpose(r))
            #file.photons=data.reshape((-1,2),order='F')
#%%            
    file=o.loadPhotons(div=1)
    print(file.photons.shape,file.idxs)
    print(np.transpose(file.photons[150:150+12,:]))
#%%
import photonpacket as pp
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
Nframes=10000000
files = [r"ciemne2-sr0.pxy"]
fnames = [folder+s for s in files]
files2=[pp.file.read(fname,Nframes=Nframes,rounding=True, shapedetect0=True) for fname in fnames]
fs2=pp.fsconcat([f.getframeseries() for f in files2])
print(fs2.N[:12])
#%%
import numpy as np
print(fs2.shape,files2[0].params['ROI'])
k=10 
for i in range(1,15):
    shape = np.max(fs2.photons[k*i:k*i+k,0:2], axis=0)
    print(shape)
    #print(fs2[i].photons,i)
#%%
fs2.imshow()
#%%
import matplotlib.pyplot as plt
plt.plot(fs2.N)
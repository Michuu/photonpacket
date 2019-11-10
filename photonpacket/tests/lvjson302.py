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
from photonpacket.lvjson3 import LV305
        
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
jsobjs=[LV305(js) for jn, js in getAlljsons(folder,'3.05')]
#% %
for o in jsobjs[0:1]:
    #print('pxy',o.file_names.positions)
    #print('pnn',o.file_names.indexes)
    #o.pathreplace(r'F:\dane',r"\\Astrosciema\f\dane") 
    o.pathshift(r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu\305a-sr0.pxy")
    file=o.loadPhotons(div=1)
    print(file.photons.shape,file.idxs)
    
#%%
import photonpacket as pp
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
Nframes=10000000
files = [r"305a-sr1.pxy"]
fnames = [folder+s for s in files]
files2=[pp.file.read(fname,Nframes=Nframes,rounding=True, shapedetect=True) for fname in fnames]
fs2=pp.fsconcat([f.getframeseries() for f in files2])
print(fs2.N[:12])
#%%
fs2.imshow()
#%%
import matplotlib.pyplot as plt
plt.plot(fs2.N)
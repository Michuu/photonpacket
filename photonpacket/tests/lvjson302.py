# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:45:48 2019

@author: wwasil
"""


#%%
from photonpacket.lvjson303 import getAlljsons
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
alljsons=getAlljsons(folder,'3.04')
#% %
from photonpacket.lvjson303 import jsonToClass
t,d=jsonToClass('302_autogen',alljsons[1][1])    
print('-'*4)
print(t)
#print(d)
#%%
o=alljsons[1][1]['ctrl_params'][0]
t,d=jsonToClass('ctrl_param',o)    
print('-'*4)
print(t)

#%%
from photonpacket.lvjson303 import LV303
        
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
jsobjs=[LV303(js) for jn, js in getAlljsons(folder,'3.04')]
#% %
for o in jsobjs[1:]:
    print('pxy',o.file_names.positions)
    print('pnn',o.file_names.indexes)
    o.pathreplace(r'F:\dane',r"\\Astrosciema\f\dane") 
    file=o.loadPhotons(div=1)
    print(file.photons.shape,file.idxs)
    

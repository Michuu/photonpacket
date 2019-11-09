# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 19:45:48 2019

@author: wwasil
"""


#%%
import glob, json
#os.chdir("/mydir")
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
def getAlljsons(folder):
    lst=[]
    for file in glob.glob(folder+"*.json"):
        #print(file)
        with open(file, "r") as f:
            s=f.read()
            jsondata1, end1 = json.JSONDecoder().raw_decode(s)
            if type(jsondata1)==dict and jsondata1.get('version',None)=='3.02':
                #print(file)
                jsondata2, end2 = json.JSONDecoder().raw_decode(s[end1:])
                jsondata1.update(jsondata2)
                lst.append(jsondata1)
    return lst

alljsons=getAlljsons(folder)
#%%
def jsonToClass(name,data):
    pretab=' '*4
    npretab='\n'+pretab
    typlst=[]
    declst=[]
    if type(data)==dict:
        for k,v in data.items():     
            kn=k.replace(' ','_')
            subt, subd=jsonToClass(k,v)
            sd='self.{k}={subd}'.format(k=kn,subd=subd)            
            typlst.append(subt)
            declst.append(sd)
        t0='class LV'+name+'(object):\n'
        t1=''.join(typlst)
        d=('def __init__(self,_data):\n'+pretab+
           npretab.join(declst))
        ssd="self.LV{k}(_data['{k}'])".format(k=name)
        return (t0+t1+d).replace('\n',npretab)+'\n', ssd
    # elif type(data)==list:        
    #     ss=set(jsonToClass('subListElement',v) for v in data)
    #     if len(ss)==1:
    #         subt, subd=list(ss)[0]
    #         return subt, "[%s for subListElement in _data['%s']"%(subd,name)
    #     else:
    #         print('list',len(data),name,len(ss))
    ssd="_data['{k}'] # {typ}".format(k=name,typ=type(data).__name__)
    return '',ssd
        
t,d=jsonToClass('302_autogen',alljsons[1])    
print('-'*4)
print(t)
#print(d)
#%%
# autogen using above
class LV302_autogen(object):
    class LVsave_params(object):
        def __init__(self,_data):
            self.krok_sekwencji=_data['krok sekwencji'] # int
            self.poczatek_nazwy=_data['poczatek_nazwy'] # str
            self.ROI=_data['ROI'] # list
            self.nf=_data['nf'] # int
    class LVfile_names(object):
        def __init__(self,_data):
            #self.positions=_data['positions'] # str
            #self.indexes=_data['indexes'] # str
            self.indexes=_data['positions'] # str
            self.positions=_data['indexes'] # str
            self.json=_data['json'] # str
            self.sequence=_data['sequence'] # str
    def __init__(self,_data):
        self.version=_data['version'] # str
        self.ctrl_params=_data['ctrl_params'] # list
        self.save_params=self.LVsave_params(_data['save_params'])
        self.file_names=self.LVfile_names(_data['file_names'])
        self.start=_data['seconds since 1Jan1904'] # str
        self.end=_data['end'] # str
        self.Nph=_data['Nph'] # int
        self.nframes=_data['nframes'] # int

class LV302(LV302_autogen):        
    def pathreplace(self,old,new):
        for k,v in self.file_names.__dict__.items():
            nn=v.replace(old,new)
            self.file_names.__dict__[k]=nn
    def createfileclass(self):
        ' compatibility with photonpacket'
        import os
        from photonpacket import file
        path=self.file_names.positions
        # extract name of file from path        
        (directory, name) = os.path.split(path)
        # remove file extension
        name = os.path.splitext(name)[0]
        # create file instance
        return file(path, name)        
    def loadPhotons(self):
        import numpy as np
        # create file instance
        file=self.createfileclass()
        dtype = np.dtype('>i4')        
        with open(self.file_names.indexes,'rb') as f:
            data=np.frombuffer(f.read(), dtype) 
            self.list_nph,file.idxs=data.reshape((2,-1),order='F')
        dtype = np.dtype('>u2')   
        with open(self.file_names.positions,'rb') as f:
            data=np.frombuffer(f.read(), dtype) 
            file.photons=data.reshape((-1,2),order='F')
        file.params=self
        #TODO: file.shape, rounding
        return file
        
folder = r"\\Astrosciema\f\dane\1909 BELL\09_11_test_nowego_formatu"+"\\"
jsobjs=[LV302(js) for js in getAlljsons(folder)]
#% %
for o in jsobjs[1:]:
    #print('pxy',o.file_names.positions)
    #print('pnn',o.file_names.indexes)
    o.pathreplace(r'F:\dane',r"\\Astrosciema\f\dane")
    file=o.loadPhotons()
    

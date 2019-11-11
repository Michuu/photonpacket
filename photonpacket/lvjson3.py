# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 15:21:40 2019

@author: wwasil
"""


import glob, json
def getAlljsons(folder,version='3.03'):
    lst=[]
    for jsonfile in glob.glob(folder+"*.json"):
        #print(file)
        with open(jsonfile, "r") as f:
            s=f.read()
            jsondata1, end1 = json.JSONDecoder().raw_decode(s)
            if type(jsondata1)==dict and jsondata1.get('version',None)==version:
                #print(file)
                jsondata2, end2 = json.JSONDecoder().raw_decode(s[end1:])
                jsondata1.update(jsondata2)
                lst.append((jsonfile,jsondata1))
    return lst

def jsonToClass(name,data):
    "automatyczny generator klasy odpowiadajacej jsonowi"
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

# autogen using above test/lvjson302.py
    
class LV305_autogen(object):
    class LVsave_params(object):
        def __init__(self,_data):
            self.element_sekwencji=_data['element sekwencji'] # str
            self.krok_sekwencji=_data['krok sekwencji'] # int
            self.poczatek_nazwy=_data['poczatek_nazwy'] # str
            self.ROI=_data['ROI'] # list
            self.nf=_data['nf'] # int
    class LVfile_names(object):
        def __init__(self,_data):
            self.positions=_data['positions'] # str
            self.indexes=_data['indexes'] # str
            self.json=_data['json'] # str
            self.sequence=_data['sequence'] # str
        def getAllFiles(self):
            kk='positions,indexes,json,sequence'.split(',')
            return [(k,getattr(self,k)) for k in kk]
    # dodane            
    class LVctrl_param(object):
        def __init__(self,_data):
            self.ctrl_path=_data['ctrl_path'] # str
            self.Value=_data['Value'] # int
    def __init__(self,_data):
        self.version=_data['version'] # str
        self.ctrl_params=[self.LVctrl_param(e) for e in _data['ctrl_params']] 
        self.save_params=self.LVsave_params(_data['save_params'])
        self.file_names=self.LVfile_names(_data['file_names'])
        self.seconds_since_1Jan1904=_data['seconds since 1Jan1904'] # str
        try:
            self.end=_data['end'] # str
            self.Nph=_data['Nph'] # int
            self.nframes=_data['nframes'] # int
            self.Nf=self.nframes
        except:
            pass
        self.ROI=self.save_params.ROI
        self.ctrl_dict={e.ctrl_path:e.Value for e in self.ctrl_params}
        

class LV305(LV305_autogen):        
    def pathreplace(self,old,new):
        for k,v in self.file_names.getAllFiles():
            nn=v.replace(old,new)
            setattr(self.file_names,k,nn)
    def pathshift(self,path):
        import os
        kk='positions,indexes,jsons,sequence'.split(',')        
        (d1, name) = os.path.split(path)
        for _,v in self.file_names.getAllFiles():
            (d2, n2) = os.path.split(v)
            ite=enumerate(zip(reversed(d1),reversed(d2)))
            for i,(a,b) in ite:
                if a!=b: 
                    if i>2:                
                        self.pathreplace(d2[:-i],d1[:-i])
                        print('pathshift "%s"->"%s"'%(d2[:-i],d1[:-i]),self.file_names.positions)
                        return
                    else:
                        break
            print('fail')
                
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
    
    def loadPhotons(self,**kwargs):    
        import numpy as np
        div=kwargs.get('div',10)
        # create file instance
        file=self.createfileclass()
        self.loadToFile(file)
        roi = self.save_params.ROI
        shape = np.array([roi[0], roi[2]])
        if False:
            shape = np.max(self.photons[:,0:2], axis=0)
        file.shape = np.array((np.round(shape*10/div)),dtype=int)        
        if kwargs.get('rounding',False):
            file.photons = np.array(np.round(np.array(file.photons,dtype=np.float)/div),dtype=np.uint16)
        else:
            file.photons = np.array(file.photons//div,dtype=np.uint16)
        #TODO: file.shape, rounding
        return file    
    
    def loadToFile(self, file, path=None, maxframes=-1):
        if path:
            self.pathshift(path)
        print('loading idxs',self.file_names.indexes)
        import numpy as np
        dtype = np.dtype('>i4')        
        with open(self.file_names.indexes,'rb') as f:
            data=np.frombuffer(f.read(), dtype) 
            self.list_nph,file.idxs=data.reshape((2,-1),order='F')
        file.idxs=np.insert(file.idxs,0,0)
        print('loading photons',self.file_names.positions,'\nnframes =',len(file.idxs),'nphotons =',file.idxs[-1])
        dtype = np.dtype('>u2')   
        with open(self.file_names.positions,'rb') as f:
            data=np.frombuffer(f.read(), dtype) 
            file.photons=data.reshape((-1,2),order='F')
        file.params=self
    
    def __getitem__(self,key):
        return self.__dict__[key] #.get(key,None)
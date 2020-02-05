#%%
#tu parser jsona
import json

singledimdtypes = ('U32', 'I32', 'U16', 'I16', 'U8', 'I8', 'DBL', 'Boolean', 'String')


def dtcast(val, dtype):
    '''
    '''
    if dtype in ('U32', 'I32', 'U16', 'I16', 'U8', 'I8'):
        val = int(val)
    elif dtype in ('DBL'):
        val = float(val)
    elif dtype in ('Boolean'):
        val = strtobool(val)
    else:
        pass
    return val


def parse(jsonfile):
    '''
    '''
    try:
        with open(jsonfile, "r") as f:
            s=f.read()
            jsondata1, end1 = json.JSONDecoder().raw_decode(s)            
            if type(jsondata1)==dict:
                if str(jsondata1.get('version','xxx'))[:2]=='3.':
                    print(jsonfile)
                    try:
                        jsondata2, end2 = json.JSONDecoder().raw_decode(s[end1:])
                        jsondata1.update(jsondata2)
                    except:
                        pass   
                    if jsondata1['version']=='3.05':
                        from .lvjson3 import LV305
                        print('labviewjsonparse LV305')
                        return LV305(jsondata1)
                    print('labviewjsonparse V3 json')
                    return jsondata1    
                elif str(jsondata1.get('version','xxx'))[:3]=='20.':
                    try:
                        jsondata2, end2 = json.JSONDecoder().raw_decode(s[end1:])
                        jsondata1.update(jsondata2)
                    except:
                        pass   
                    if str(jsondata1['version'])=='20.01':
                        from .lvjson20 import LV2001
                        print('labviewjsonparse LV2001')
                        return LV2001(jsondata1)
                    print('labviewjsonparse V20 json')
                    return jsondata1  
                    
    except Exception as error:
            print('labviewjsonparse.parse:',error)
            #TODO raise exception?
   
    params = {}

    i = 0
    
    for i in jsondata1:
        
        path=i["path"]       
        val=i["Value"]
    
        params[path] = val
    
    print('labviewjsonparse params')        
    return params
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
        jsonfile=open(jsonfile, "r")  
        jsondata = json.load(jsonfile)
        jsonfile.close()
    except Exception as error:
            print(error)
            #TODO raise exception?
   
    params = {}

    i = 0
    
    for i in jsondata:
        
        path=i["path"]       
        val=i["Value"]
    
        params[path] = val
        
    return params
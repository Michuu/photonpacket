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
        
        path=i["path"][i["path"].find("::")+len("::"):]

        
        val=i["Value"]
        
        params[path] = val
    '''for cluster in root.iter('Cluster'):
        try:
            key = cluster.find('String').find('Val').text
            key = key.replace('\n',' ')
            variant = cluster.find('LvVariant')
            dtype = variant[1].tag
            if dtype in singledimdtypes:
                val = variant[1].find('Val').text
                val = dtcast(val, dtype)
            elif dtype in ('Array'):
                ds = variant[1].find('Dimsize')
                for dt in singledimdtypes:
                    if variant[1].find(dt) is None:
                        continue
                    else:
                        val = []
                        for v in variant[1].iter(dt):
                            val.append(dtcast(v[1].text, dt))
        except AttributeError:
            i+=1
            continue'''
    return params
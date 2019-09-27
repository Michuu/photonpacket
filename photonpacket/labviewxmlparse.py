import xml.etree.ElementTree as et
from distutils.util import strtobool

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

def parse(xmlfile):
    '''
    '''
    tree = et.parse(xmlfile)
    root = tree.getroot()

    params = {}

    i = 0

    for cluster in root.iter('Cluster'):
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
            continue
        params[key] = val
    return params

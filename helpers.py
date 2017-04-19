import numpy as np
#import matplotlib as mpl

nom = np.vectorize(lambda x: x.n)
std = np.vectorize(lambda x: x.s)

def siprefix(prefix):
    '''
    Obtain SI prefix factor from string prefix
    
    Parameters
    ----------
    prefix : string
        
    Returns
    ----------
    factor : double
    
    See Also
    ----------
    
    Notes
    ----------
    
    Examples
    ----------
    >>> pp.file.siprefix('n')
    1e-9
    
    '''
    # we will not be using da (deca)
    prefixes = {'y': 1e-24, 'z': 1e-21, 'a': 1e-18, 'f': 1e-15, 'p': 1e-12,
                'n': 1e-9, 'u': 1e-6, 'm': 1e-3, 'k': 1e3,
                'M': 1e6, 'G': 1e9, 'T': 1e12, 'c': 1e-2, 'd': 1e-1,
                'P': 1e15, 'E': 1e18, 'Z': 1e21, 'Y': 1e24}
    if prefix in prefixes:
        return prefixes[prefix]
    else:
        return False
    
def opcolor(rgba):
    '''
    Generate opposite color in rgba format
    '''
    if np.sum(rgba[:3])>1.5:
        return (0,0,0,1)
    else:
        return (1,1,1,1)
    #rgba = np.array(rgba)
    #rgb = rgba[:3]
    #hsv = mpl.colors.rgb_to_hsv(rgb)
    #newhsv = np.array([(hsv[0]+0.5)%1,1-hsv[1],1-hsv[2]])
    #newrgb = mpl.colors.hsv_to_rgb(newhsv)
    #newrgba = np.append(newrgb, rgba[3])
    #rgba[:-1] = 1 - rgba[:-1]

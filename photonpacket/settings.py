'''
Verbosity parameter
default value is 1
'''
verbose = 1

'''
Overwrite in messages
'''
overwrite = True

'''
matplotlib defaults
'''
import matplotlib as mpl
# map origin
mpl.rc('image', interpolation='none', origin='lower')
# colormap
mpl.rcParams['image.cmap'] = 'RdBu_r'
# fonts
mpl.rcParams["font.family"] = "STIXGeneral"
mpl.rcParams["mathtext.fontset"] = "stixsans"
mpl.rcParams['axes.linewidth'] = 0.5

'''
Params file
'''
paramsext = 'xml'
import labviewxmlparse as lxp
paramsparser = lxp.parse

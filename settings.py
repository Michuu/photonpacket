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
mpl.rcParams['image.cmap'] = 'coolwarm'
# fonts
mpl.rcParams["font.family"] = "STIXGeneral"
mpl.rcParams["mathtext.fontset"] = "stixsans"
mpl.rcParams['axes.linewidth'] = 0.5

'''
Extension for params file
'''
paramsext = 'xml'
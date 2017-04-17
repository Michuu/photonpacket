from distutils.core import setup, Extension
import numpy

# define the extension module
frameshift = Extension('frameshift', sources=['frameshift.c'],
                          include_dirs=[numpy.get_include()])

# run the setup
setup(ext_modules=[frameshift])
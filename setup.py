from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy

extensions = [
        Extension('photonpacket.frameutils.coinc',['photonpacket/frameutils/coinc.pyx']),
        Extension('photonpacket.frameutils.arraysplit',['photonpacket/frameutils/arraysplit.pyx']),
        Extension('photonpacket.frameutils.accum',['photonpacket/frameutils/accum.pyx']),
        Extension('photonpacket.index_raw_file',['photonpacket/index_raw_file.pyx'])
        ]

setup(
    ext_modules=cythonize(extensions, language_level = "3"),
    include_dirs=[numpy.get_include()]
)

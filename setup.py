from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy

extensions = [
        Extension('photonpacket.frameutils.coinc',['photonpacket/frameutils/coinc.pyx']),
        Extension('photonpacket.frameutils.coinc8',['photonpacket/frameutils/coinc8.pyx']),
        Extension('photonpacket.frameutils.coinc16',['photonpacket/frameutils/coinc16.pyx']),
        Extension('photonpacket.frameutils.coinc32',['photonpacket/frameutils/coinc32.pyx']),
        Extension('photonpacket.frameutils.arraysplit',['photonpacket/frameutils/arraysplit.pyx']),
        Extension('photonpacket.frameutils.arraysplit2',['photonpacket/frameutils/arraysplit2.pyx'])
        ]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()]
)

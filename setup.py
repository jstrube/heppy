#!/usr/bin/env python
"""Install file for example on how to use Pyrex with Numpy.

For more details, see:
http://www.scipy.org/Cookbook/Pyrex_and_NumPy
http://www.scipy.org/Cookbook/ArrayStruct_and_Pyrex
"""

from setuptools import setup, Extension

# Make this usable by people who don't have pyrex installed (I've committed
# the generated C sources to SVN).
try:
    from Cython.Distutils import build_ext
    has_pyrex = True
except ImportError:
    has_pyrex = False

import numpy

# Define a pyrex-based extension module, using the generated sources if pyrex
# is not available.
if has_pyrex:
    pyx_sources = ['src/Geometry/geometry.pyx']
    cmdclass    = {'build_ext': build_ext}
else:
    pyx_sources = ['src/Geometry/geometry.c']
    cmdclass    = {}


pyx_ext = Extension('Geometry.geometry',
                 pyx_sources,
                 include_dirs = [numpy.get_include()])

description = \
""" Compilation of modules for interop 
    between paida, numpy/scipy and pytables'
"""
# Call the routine which does the real work
setup(name         = 'heppy'
    , version      = '0.1'
    , description  =  description
    , author       = 'Jan Strube'
    , license      = 'Python Software Foundation License'
    , author_email = 'curiousjan@gmail.com'
    , url          = 'http://code.gmail.com/heppy'
    , ext_modules  = [pyx_ext]
    , cmdclass     = cmdclass
    , packages     = ['Geometry', 'PaidaUtils', 'Fitting', 'Histogram']
    , package_dir  = {'Geometry': 'src/Geometry', 'PaidaUtils': 'src/PaidaUtils', 'Fitting': 'src/Fitting', 'Histogram': 'src/Histogram'}
    , test_suite = 'nose.collector'
    )

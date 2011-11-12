#!/usr/bin/env python
"""Install file for example on how to use Pyrex with Numpy.

For more details, see:
http://www.scipy.org/Cookbook/Pyrex_and_NumPy
http://www.scipy.org/Cookbook/ArrayStruct_and_Pyrex
"""

from distutils.core import setup
from distutils.extension import Extension

# Make this usable by people who don't have pyrex installed (I've committed
# the generated C sources to SVN).
try:
    from Pyrex.Distutils import build_ext
    has_pyrex = True
except ImportError:
    has_pyrex = False

import numpy

# Define a pyrex-based extension module, using the generated sources if pyrex
# is not available.
if has_pyrex:
    pyx_sources = ['geometry.pyx']
    cmdclass    = {'build_ext': build_ext}
else:
    pyx_sources = ['geometry.c']
    cmdclass    = {}


pyx_ext = Extension('geometry',
                 pyx_sources,
                 include_dirs = [numpy.get_include()])

# Call the routine which does the real work
setup(name        = 'geometry',
      description = 'Some fundamental classes to do lorentz boosts, etc.',
      ext_modules = [pyx_ext],
      cmdclass    = cmdclass,
      )

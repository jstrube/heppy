from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
  name = 'PyMinui2',
  ext_modules=[ 
    Extension(
        "pyMinuit"
      , ["pyMinuit2.pyx"]
      , language='c++'
    ),
    ],
  cmdclass = {'build_ext': build_ext},
  include_dirs=['/Users/jstrube/lib/python2.5/site-packages/numpy/core/include/numpy'
              , '/opt/Minuit2/include']
)

from distutils.core import setup, Extension
import numpy.distutils.misc_util
import numpy as np
#from Cython.Distutils import build_ext
module1 = Extension('myfftwmpi', sources = ['myfftwmpimodule.c'],
         include_dirs = ['/Users/zhuangdvm/my_fftw/include', '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/core/include'],
         library_dirs = ['/Users/zhuangdvm/my_fftw/lib'],
         extra_link_args=["-lfftw3_mpi", "-lfftw3", "-lm"])

setup (name = 'PackageName',
       version = '1.0',
        author = 'Zhong Huang',
        author_email = 'zhuangdvm@gmail.com',
        description  = 'This is a demo package',
        ext_modules  = [module1])

#!/usr/bin/env python
#
#
#  08/26/2016
#  New version of sort3D.
#  
from __future__ import print_function

from builtins import range
import  os
import  sys
import  types
import  global_def
from    global_def import *
from    optparse   import OptionParser
from    sparx      import *
from    EMAN2      import *

import numpy as np
from time import time
N = 700
d1 = np.array(np.random.uniform(0.0, 1.0, size=N), dtype=np.float32)
print(d1)
print (type(d1))
at = time()
a= np.array([[d1 for i in range(N)] for j in range(N//2)])
print (a.shape)
at = time()
b = np.fft.fftn(a)
print('forward transform',  (time() - at)/60.)
print(b.shape)
at = time()
c = np.fft.ifftn(b)
print('backword transform', (time() - at)/60.)
print(c.shape)
"""
v = model_gauss_noise(10, 360, 360, 360)
at = time()
fv =fft(v)
print('forward transform',  (time() - at)/60.)
d = EMNumPy.em2numpy(fv)

print(type(d))
print(d.shape)
"""
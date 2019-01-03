#!/usr/bin/env python
import numpy as np
def testturple(x, *vartup):
	for var in vartup:
		print var
	return


x= np.array(range(5))
#vartup = (x*x, 2.*x)

testturple(x, x*x, 2*x)
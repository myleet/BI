#!/usr/bin/env python
import numpy as np
from scipy import interpolate
from scipy import ndimage

def sumsqe(args, *data):
        # In this version central image is not modified.
        s = EMData(data[2], data[2], 1, False)
        n = len(args)//2
        k=0
        for i in range(n+1):
                if(i == (n+1)//2):
                        Util.add_img(s,data[0][i])
                        #print("  Central  ",n,i,k)
                else:
                        Util.add_img(s,fshift(data[0][i],args[2*k],args[2*k+1]))
                        #print("  Shift  ",n,i,k,args[2*k],args[2*k+1])
                        k+=1

        outo = -Util.innerproduct(s,s,data[1])
        outo/=float(data[2]*data[2]*(n+1))
        """
        zeq = 0.0
        for q in args:  zeq+=q*q
        zeq/=len(args)
        print(max(args),min(args),zeq,outo)
        """
        print("  sumsqe   ",args,outo)
        return outo





from scipy import optimize
from random import *
n = 2
args   = [1.3,-1.7,0.0,0.0]
n = 4
args   = [1.3,-1.7,0.1,-0.49,0.0,0.0,-1.2,0.9]

e=model_gauss(3, 100, 100)

#n = 6
#args   = [1.3,-1.7,0.7,-1.1,0.1,-0.49,0.0,0.0,-0.2,0.4,-1.2,0.9]

smst=[]
for i in range(n):  smst.append(fshift(e,0.0,0.0))
mydata = (smst, fiqu, nx)
targs = [0.0]*2*(n-1)
_ = sumsqe(targs, mydata)

smst=[]
for i in range(n):  smst.append(fshift(e,-args[2*i],-args[2*i+1]))
targs = args[:]
del targs[n]
del targs[n]
print(targs)
mydata = (smst, fiqu, nx)
_ = sumsqe(targs, mydata)
#targs=[-0.20394168,  0.2206378 ,  0.8325592 , -1.34346256,  0.18188091,
#       -0.75807225, -0.1855929 ,  0.1955014 , -1.0839242 ,  0.70862652]
#optimize.minimize(sumsqe, targs, (mydata,), method='COBYLA', constraints=(), tol=None, callback=None, options={'rhobeg': 1.0, 'maxiter': 500, 'disp': True, 'catol': 0.0002})

targs = [0.0]*(2*(n-1))
targs = [1.99,-1.99,1.99,-1.99,1.99,-1.99]
bounds = [(-2.,2.),(-2.,2.),(-2.,2.),(-2.,2.),(-2.,2.),(-2.,2.)]

opo1 = optimize.minimize(sumsqe, targs, (mydata,), method='L-BFGS-B', \
jac="2-point", bounds=bounds, tol=None, callback=None, \
options={'disp': None, 'maxcor': 10, 'ftol': 2.220446049250313e-08, 'gtol': 1e-04, 'eps': 1.0e-2, 'maxfun': 150, 'maxiter': 150, 'iprint': 1, 'maxls': 20})

opo2 = optimize.minimize(sumsqe, opo1["x"], (mydata,), method='L-BFGS-B', \
jac="2-point", bounds=bounds, tol=None, callback=None, \
options={'disp': None, 'maxcor': 10, 'ftol': 2.220446049250313e-08, 'gtol': 1e-04, 'eps': 1.0e-3, 'maxfun': 150, 'maxiter': 150, 'iprint': 1, 'maxls': 20})




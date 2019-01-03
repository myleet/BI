import  os
import  sys
import  types
from    optparse   import OptionParser
from    sparx      import *
from    EMAN2      import *
nx    = 300
p1    = model_circle(110, nx,nx)
'''
p2    = model_circle(120, nx,nx)
ff    = model_circle(40, nx,nx)
fp1 =fft(p1)
fp2 =fft(p2)
#nrmref = sqrt(Util.innerproduct(fp1, fp1, None))
#Util.mul_scalar(fp1, 1.0/nrmref)
m = Util.unrollmask(nx)
a = Util.innerproduct(fp1, fp2, m)/(nx*nx)
b = Util.innerproduct(p1, p1, m)
from math import pi
print(a, b, a/b*pi**2/4.)
fp1 =fft(p1*ff)
fp2 =fft(p2)
a = Util.innerproduct(fp1, fp2, m)/(nx*nx*2)
fp1 =fft(p1)
fp2 =fft(p2*ff)
b = Util.innerproduct(fp1, fp2, m)/(nx*nx*2)
print(a, b)
print(Util.innerproduct(p1*ff, p2, None), Util.innerproduct(p1, p2*ff, None))
'''
from math import pi
mask = Util.unrollmask(nx)
for j in range(nx//2,nx): mask[j]= 0.0
m = Util.unrollmask(nx)
fp1=fft(Util.mulnclreal(fft(p1),mask))
print(Util.innerproduct(p1,p1,m)/(nx*nx*2))
print(Util.innerproduct(fp1, fp1, None))
exit()


#####
p1    = model_circle(110, nx,nx)
p2    = model_circle(120, nx,nx)
ff    = model_circle(40, nx,nx)
fp1 =fft(p1*ff)
fp2 =fft(p2)
fp1=fft(Util.mulnclreal(fp1,mask))
fp2=fft(Util.mulnclreal(fp2,mask))
a = Util.innerproduct(fp1, fp2, None)/(nx*nx*2)
fp1 =fft(p1)
fp2 =fft(p2*ff)
fp1=  fft(Util.mulnclreal(fp1,mask))
fp2 = fft(Util.mulnclreal(fp2,mask))

b = Util.innerproduct(fp1, fp2, None)/(nx*nx*2)
print(a, b)
print(Util.innerproduct(p1*ff, p2, m), Util.innerproduct(p1, p2*ff, m))

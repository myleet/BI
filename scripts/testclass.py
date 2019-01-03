#!/usr/bin/env python

def scale_data(data, scale, stream):
	cdata= []
	cdata[:] = data[:]
	for i in range(len(data)):
		cdata[i] *=scale
	scale =10.
	stream(scale)
	return cdata
	
def print_some(a):
	print("print ", a)
	return
"""
a = [i for i in range(10)]
print('initial a', a)
scale =2.

stream = print_some

b = scale_data(a, scale, stream)
print('after call')
print('a',a)
print('b',b)
print('scale',scale)
print(divmod(10, 3))
#print('iter', iter(a))
print("--------------------------------")
for x, y in [ {7, 2}, {5, 8}, {6, 4} ]:
	print(x, y)
from random import seed

seed()
"""
a =range(10)
for i in range(len(a)-1, -1, -1):
	print(a[i])
	




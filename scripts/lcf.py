#!/usr/bin/env python
from __future__ import print_function
#
#
# naive solution
def lcf(N1, N2, m):
	if (N1%m == 0) and (N2%m==0): return m
	else: return lcf(N1, N2, m-1)

def lcf_iter(N1, N2):
	m = min(N1, N2)
	do_mod = True
	while do_mod:
		if N1%m !=0 or N2%m !=0:
			m = m-1
		else:
			do_mod = False
	return m
"""	
N1 = 24
N2 = 32
m = 24
a = lcf_iter(N1, N2)
print(a)
"""
a =1
b =2
print((a<b?a:b))

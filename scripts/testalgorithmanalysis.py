#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import os

# Chapter 3. Algorithm analysis
 
# Reinforcement
"""
R-3.1
Graph the functions 8n, 4nlogn, 2n2, n3, and 2n using a logarithmic scale 
for the x- and y-axes; that is, if the function value f (n) is y, plot this as
 a point with x-coordinate at logn and y-coordinate at logy.
"""

from math import log

nlist = [2, 4, 6, 8, 10, 12, 18, 100]
'''
for i in range(len(nlist)):
	print('-----------------------')
	print (8*nlist[i])
	print(4*nlist[i]*log(nlist[i]))
	print(2*(nlist[i]**2))
	print(nlist[i]**3)
	print(2**nlist[i])
	
cn<nlogn<n^2<n^3<2^n
'''

"""
R-3.2 
The number of operations executed by algorithms A and B is 8*n*logn and 2n^2, respectively.
 Determine n0 such that A is better than B for n>=n0.
 
 4*logn<n
 n = 9
 R-3.6
 What is the sum of all the even numbers from 0 to 2n, for any positive integer n?
 2*n*n
"""
#n  = 5
#print(sum([k for k in range(0, 2*n+2, 2)]))
#print([k for k in range(0, 2*n+2, 2)])

"""
R-3.8
Order the following functions by asymptotic growth rate.

2^10<(3*n+100logn)<4*n<(n*logn)<4nlogn+2n<n^2+10n<n^3<2^n
"""

"""
C-3.41
Describe an algorithm for finding both the minimum and maximum of n numbers using 
fewer than 3n/2 comparisons. (Hint: First, construct a group of candidate 
minimums and a group of candidate maximums.)
a loop of n/2 : select min candidates and max candidates
a loop of n/2: find max, min each has two comparison 

C-3.35
Assuming it is possible to sort n numbers in O(nlogn) time, show that it is possible to 
solve the three-way set disjointness problem in O(nlogn) time.
Sort them all, and then check if there is any identical elements.
nlogn+n

C-3.36
Describe an efficient algorithm for finding the ten largest elements in a sequence of size 
n. What is the running time of your algorithm?
n*10log10

C-3.38
Show that sumi^2 is O(n3).
C-3.39
Show sum(i/2^i)<2
C-3.40
Show that logb^f(n) is theta(logf(n))if b > 1 is a constant.

logb^f(n)=logf(n)/logb
C-3.45

A sequence S contains n-1 unique integers in the range [0,n-1], that
is, there is one number from this range that is not in S. Design an O(n)
time algorithm for finding that number. You are only allowed to use O(1)
additional space besides the sequence S itself.

C-3.54
AsequenceScontainsnintegerstakenfromtheinterval[0,4n],with repetitions allowed. 
Describe an efficient algorithm for determining an integer value k that occurs 
the most often in S. What is the running time of your algorithm?
O(n). 
one loop over n
Check dictionary
if x in dict: k+1
else:         k = 1
"""





	

#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import os

def fibonacci(n):
	if n<=1:
		return (n, 0)
	else:
		(a, b)= fibonacci(n-1)
		return (a+b, a)

def pow(x, n):
	if n==0: return 1
	elif n>0: return x*pow(x, n-1)
	else: return 1./x*pow(x, n+1)
		
#### dynamic array
import ctypes
class DynamicArray:
	def __init__(self):
		self._n        = 0
		self._capacity = 1
		self._A = self._make_array(self._capacity)
		
	def __len__(self):
		return self._n
		
	def __getitem__(self, k):
		if not 0<= k<self._n:
			raise IndexError('invalid index')
		return self._A[k]
		
	def append(self, obj):
		if self._n == self._capacity:
			self._resize(2*self._capacity)
		self._A[self._n] = obj
		self._n +=1
		
	def _resize(self, c):
		B = self._make_array(c)
		for k in range(self._n):
			B[k] == self._A[k]
		self._A = B
		self._capacity = c
	
	def _make_array(self, c):
		return (c*ctypes.py_object)()
		
class ArrayStack:
	def __init__(self):
		self._data = []
	def __len__(self):
		return len(self._data)
	def is_empty(self):
		return len(self._data) == 0
	def push(self, e):
		self._data.append(e)
	def top(self):
		if self.is_empty(): raise Empty('Stack is empty')
		return self._data[-1]
	def pop(self):
		if self.is_empty(): raise Empty('Stack is empty')
		return self._data.pop()
	
"""
#for i in range(30):
#	print('fibonacci, %d   %d'%(i, fibonacci(i)[0]))
x = 1.2
print('x^n = ', pow(x, -1))
da = DynamicArray()
print ('_n is ', da._n)
for i in range(10):
	da._A[i] = i+5
print( da.__getitem__(4))
document=['a', 'b', 'w', './']
letters = ''.join(c for c in document if c.isalpha())
print(letters)

def test_dict(d):
	for a,b in d.items():
		print (a, b)
		d[a] = b+1
	return
dict = {}
dict["a"] = 1
dict["b"] = 2
test_dict(dict)
print(dict)
"""
# loop fibonacci






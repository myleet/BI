#!/usr/bin/env python

from __future__ import print_function
from builtins import range
### Chapter 5 - 6
##  Code Fragment 5.3
import ctypes
class DynamicArray:
	def __init__(self):
		self._n        = 0
		self._capacity = 1
		self._A = self._make_array(self._capacity)
		
	def __len__(self):
		return self._n
		
	def __getitem__(self, k):
		if k<0:
			while k<0:
				k +=self._capacity # Now support negative index
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
		
	def insert(self, k, value):
		if self._n ==self._capacity:
		 	self._resize(2*self._capacity)
		for j in range(self._n, k+1, -1):
			self._A[j] = self._A[j-1]
		 	if j ==k:
		 		self._A[k] =value
		 		self._n   +=1

class ArrayStack: # list: the first in, the last out
	def __init__(self):
		self._data = []
	def __len__(self):
		return len(self._data)
	def is_empty(self):
		return (len(self._data) == 0)
	def push(self, e):
		self._data.append(e)
	def top(self):
		if self.is_empty():
			raise Empty( 'Stack is empty' )
		return self._data[-1]
	def pop(self):
		if self.is_empty():
			raise Empty( 'Stack is empty' )
		return self._data.pop()
	def transer(self, T):
		for i in range(len(self._data)):
			T.append(self._data.pop())
	def recursive_remove(self):
		if self.is_empty():return
		else:
			self.pop()
			self.recursive_remove()
	def __getitem__(self, k):
		if k<0:
			while k<0:
				k += len(self._data)# Now support negative index
		return self._data[k]
	
	
	
			
DEFAULT_CAPACITY = 1000
class ArrayQueue:
	def __init__(self):
		self._data  = [None]*DEFAULT_CAPACITY
		self._size  = 0
		self._front = 0
		
	def __len__(self):
		return self._size
	def is_empty(self):
		return self._size == 0 
	def first(self):
		if self.is_empty():
			raise ValueError('Queue is empty')
		return self._data[self._front]
		
	def dequeue(self):
		if self.is_empty():
			raise ValueError('Queue is empty')
		value = self._data[self._front]
		self._data[self._front] = None
		self._front =(self._front+1)%len(self._data)
		self._size  -=1
		return value
		
	def enqueue(self, value):
		if self._size == len(self._data):
			self._resize(2*len(self._data))
		avail = (self._front + self._size)%len(self._data)
		self._data[avail] = value
		self._size +=1
			
	def _resize(self, cap):
		old = self._data
		self._data = [None]*cap
		walk = self._front
		for k in range(self._size):
			self._data[k] = old[walk]
			walk = (1 + walk) % len(old)
		self._front = 0
####
"""
R-5.4 
OurDynamicArrayclass,asgiveninCodeFragment5.3,doesnotsupport use of negative 
indices with __getitem__ . Update that method to better match the semantics 
of a Python list.

R-5.6
Our implementation of insert for the DynamicArray class, as given in Code 
Fragment 5.5, has the following inefficiency. In the case when a re- size occurs,
 the resize operation takes time to copy all the elements from an old array to a 
 new array, and then the subsequent loop in the body of insert shifts many of 
 those elements. Give an improved implementation of the insert method, so that, 
 in the case of a resize, the elements are shifted into their final position during 
 that operation, thereby avoiding the subsequent shifting.
R-5.7
Let A be an array of size n >=2 containing integers from 1 to n - 1, inclusive, with 
exactly one repeated. Describe a fast algorithm for finding the integer in A that is repeated.
Create a dictionary with elements 1 - n-1 as key.
loop over A and each time delete one element from dictinoary.
The one cannot find its match is the repeated element.

R-6.1
What values are returned during the following series of stack operations,
if executed upon an initially empty stack? 5
push(5), 
push(3), 
pop(), 
push(2), 
push(8), 
pop(), 
pop(), 
push(9), 
push(1), 
pop(), 
push(7), 
push(6), 
pop(), 
pop(),
push(4), 
pop(), 
pop().
5

R-6.2
18
R-6.3
Implement a function with signature transfer(S, T) that transfers all elements from 
stack S onto stack T, so that the element that starts at the top of S is the first to 
be inserted onto T, and the element at the bottom of S ends up at the top of T
from collections import deque
"""
def is_matched_html(raw):
	S = ArrayStack()
	j = raw.find('<')
	while j !=-1:
		k = raw.find('>', j+1)
		if k==-1:
			return False
		tag = raw[j+1:k]
		if not tag.startswith('/'):
			S.push(tag)
		else:
			if S.is_empty():     return False
			if tag[1:]!=S.pop(): return False
		j = raw.find('<', k+1)
	print(S)
	return S.is_empty()
	
def get_a_piece(raw):
	S = ArrayStack()
	Q = ArrayStack()
	W = ArrayStack()
	j = raw.find('<')
	while j !=-1:
		k = raw.find('>', j+1)
		if k ==-1: return
		tag = raw[j+1:k]
		if not tag.startswith('/'):
			S.push(tag)
			m = k+1
		else:
			if tag[1:]== S[-1]:
				Q.push(raw[m:j])
				W.push(S.pop())
		j = raw.find('<', k+1)
	return Q, W
	
from urllib import urlopen
url = "https://www.bbc.com/news"
html_doc = urlopen(url).read()
raw =''
for a in html_doc:
	raw +=a
#print(raw)
#print(is_matched_html(raw))
with open('tmp.txt', 'w') as fout:
	fout.write(raw)
fout.close()

s,w = get_a_piece(raw)
print(len(s))
for i in range(len(s)):
	print('TAG', w.pop(), s.pop())

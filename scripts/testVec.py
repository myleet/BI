#!/usr/bin/env python

class Vector:
	def __init__(self, d): self._coords=[0]*d
	def __len__(self): return len(self._coords)
	def __getitem__(self, j): return self._coords[j]
	def __setitem__(self, j, val):
		self._coords[j] = val
	def __add__(self, other):
		if len(self)!=len(other): raise ValueError('dimensions must agree')
		results  = Vector(len(self))
		for j in range(len(self)):
			results[j] = self[j]+other[j]
		return results
	def __eq__(self, other):
		return self._coords == other._coords
	def __str__(self):
		return '<' +str(self._coords)[1:-1]+'>'

class SequenceIterator:
	def __init__(self, sequence):
		self._seq = sequence
		self._k   = -1
	def __next__(self):
		self._k+=1
		try:
			return (self._seq[self._k])
		except:
			print('Number of calling next exceeds the size of sequence')
	def __iter__(self): return self

class Range:
	def __init__(self, start, stop = None, step = 1):
		if step == 0: raise ValueError('step cannot be 0')
		if step is None: start, stop = 0, start
		self._length = max(0, (stop - start + step -1)//step)
		self._start  = start
		self._step   = step
	def __len__(self): return self._length
	def __getitem__(self, k):
		if k<0: k+=len(self)
		if not 0<=k<self._length: raise IndexError('index out of bound')
		return self._start +k*self._step
		
if __name__=='__main__':
	v = Vector(3)
	print(str(v))
	print(len(v))
	c =[1, 2, 3]
	print(v.__setitem__(1, 2.))
	print('getitem', v.__getitem__(1))
	print(v.__add__(c))
	s     = [1, 2, 3, 4]
	its = SequenceIterator(s)
	print(its._seq, its._k)
	print(its.__next__())
	print(its.__next__())
	print(its.__next__())
	print(its.__next__())
	print(its.__next__())
	r = Range( 0, 10, 2)
	print(len(r))
	print(r.__getitem__(3))
	
	
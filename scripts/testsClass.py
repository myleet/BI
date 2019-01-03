#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import os

# Chapter 2. Class
 
# Reinforcement
"""
R-2.1
Give three examples of life-critical software applications.
R-2.2
Give an example of a software application in which adaptability can mean
the difference between a prolonged lifetime of sales and bankruptcy.
R-2.3
Describe a component from a text-editor GUI and the methods that it encapsulates.
"""

"""
R-2.4
Write a Python class, Flower, that has three instance variables of type str, int, and float, 
that respectively represent the name of the flower, its number of petals, and its price. 
Your class must include a constructor method that initializes each variable to an
appropriate value, and your class should include methods for setting the value of each type,
 and retrieving the value of each type.
"""
class Flower:
	def __init__(self, name = 'flower', npetals = 1 , price = 10.0):
		self._name    = name
		self._npetals = npetals
		self._price   = price
		
	def get_name(self):
		return self.name
	def get_npetals(self):
		return self.npetals
	def get_price(self):
		return self.price

	def set_name(self, name):
		self.name = name
	def set_npetals(self, npetals):
		self.npetals = npetals
	def set_price(self, price):
		self.price = price
'''
a = Flower()
print(a.name, a.npetals, a.price)
print(a.get_name())
print(a.get_price())
a.set_price(20.)
print(a.price)
'''
"""
R-2.5
Use the techniques of Section 1.7 to revise the charge and make payment methods of the 
CreditCard class to ensure that the caller sends a number as a parameter.
"""
class CreditCard:
	def __init__(self, customer, bank, acnt, limit, current_balance):
		self._customer = customer
		self._bank     = bank
		self._account  = acnt
		self._limit    = limit
		self._balance  = current_balance
		def get_customer(self):
			return self._customer
		
	def get_bank(self):
		return self._bank
	def get_account(self):
		return self._account
	def get_limit(self):
		return self._limit
	def get_balance(self):
		return self._balance
	def charge(self, price):
		if not isinstance(price, (int, float)):
			raise ValueError('Price is not a number')
		if self._balance+price>self._limit:
			return False
		else:
			self._blance+=price
			return True
	def make_payment(self, amount):
		if amount<0.0:raise ValueError('Negative Payment')
		self._blance -=amount
"""
R-2.6
If the parameter to the make payment method of the CreditCard class were a negative 
number, that would have the effect of raising the balance on the account. Revise 
the implementation so that it raises a ValueError if a negative value is sent.
R-2.7
The CreditCard class of Section 2.3 initializes the balance of a new account to zero.
 Modify that class so that a new account can be given a nonzero balance using an optional 
 fifth parameter to the constructor. The four-parameter constructor syntax should continue 
 to produce an account with zero balance.
R-2.8
Modify the declaration of the first for loop in the CreditCard tests, from Code Fragment 2.3,
 so that it will eventually cause exactly one of the three credit cards to go over 
 its credit limit. Which credit card is it? 
R-2.9
Implement the __sub__  method for the Vector class of Section 2.3.3, so that the 
expression u-v returns a new vector instance representing the difference
between two vectors.

R-2.10 
Implement the __neg__  method for the Vector class of Section 2.3.3, so that the 
expression -v returns a new vector instance whose coordinates are all the negated values 
of the respective coordinates of v.

R-2.11
In Section 2.3.3, we note that our Vector class supports a syntax such as 
v = u + [5, 3, 10, -2, 1], in which the sum of a vector and list returns a new vector. 
However, the syntax v = [5, 3, 10, -2, 1] + u is illegal. Explain how the Vector class 
definition can be revised so that this syntax generates a new vector. ???

R-2.12
Implement the __mul__ method for the Vector class of Section 2.3.3, so that the \
expression v*3 returns a new vector with coordinates that are 3 times the 
respective coordinates of v.

R-2.13
Exercise R-2.12 asks for an implementation of __mul__ , for the Vector class of 
Section 2.3.3, to provide support for the syntax v 3. Implement the __rmul__ method, 
to provide additional support for syntax 3*v.???
R-2.14: dot multipliation
R-2.15: expand initialization to sequence
"""
class Vector:
	def __init__(self, d):
		if isinstance(d, int):self._coords=[0]*d
		if isinstance(d, (list, tuple)):
			self._coords =[0]*len(d)
			for i in range(len(d)):self._coords[i] = d[i]
	def __len__(self): 
		return len(self._coords)
	def __getitem__(self, j):
		return self._coords[j]
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
	def __sub__(self, nvec):
		if len(self)!=len(nvec): raise ValueError('dimensions must agree')
		res =  Vector(len(self))
		for j in range(len(self._coords)):
			res[j] = self._coords[j] - nvec[j]
		return res
	def __neg__(self):
		res =  Vector(len(self))
		for j in range(len(self._coords)):
			res[j] = self._coords[j]*(-1.)
		return res
	def __mul__(self, scalar):
		if not isinstance(scalar, (int, float)):
			raise ValueError('The multiplier is not a number')
		res =  Vector(len(self))
		for j in range(len(self._coords)):
			res[j] = self._coords[j]*scalar
		return res
	def __dot_mul__(self, nvec):
		if len(self)!=len(nvec): 
			raise ValueError('The multiplier is not a number')
		res = 0.0
		for j in range(len(self._coords)):
			res  += self._coords[j]*nvec[j]
		return res

a = Vector([3, 2, 5])
print('size', a.__len__())
c = a.__mul__(3.)

print(c._coords)
print(a.__dot_mul__(c))
	

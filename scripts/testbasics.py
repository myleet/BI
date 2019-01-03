#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import os

# Chapter 1. Python basics
 
# Reinforcement
"""
R-1.1
Write a short Python function, is multiple(n, m), that takes two integer
values and returns True if n is a multiple of m, that is, n = mi for some
integer i, and False otherwise.
"""

def multiple(n, m):
	if (n//m>=1) and (n%m)==0: return True
	else: return False
#print(multiple(6, 2))

"""
R-1.2
Write a short Python function, is even(k), that takes an integer value and
returns True if k is even, and False otherwise. However, your function
cannot use the multiplication, modulo, or division operators.
"""
def is_even(k):
	if k==1:  return False
	elif k==2:return True
#print('is even', is_even(9))

"""
R-1.3
Write a short Python function, minmax(data), that takes a sequence of
one or more numbers, and returns the smallest and largest numbers, in the
form of a tuple of length two. Do not use the built-in functions min or
max in implementing your solution.
"""
def find_min_max_from_a_sequence(slist, index, min_max_tuple):
	if len(slist)  == 1:
		return (slist[0], slist[0])
	elif len(slist) ==2:
		if slist[0]<=slist[1]:return (slist[0], slist[1])
		else: return (slist[1], slist[0])
	else:
		if index >=len(slist): return (min_max_tuple[0], min_max_tuple[1])
		else:
			if slist[index] >min_max_tuple[1]: min_max_tuple[1] =  slist[index]
			if slist[index] <min_max_tuple[0]: min_max_tuple[0] =  slist[index]
			return find_min_max_from_a_sequence(slist, index+1, min_max_tuple)
#slist  = [1, 3, 4, 2, 9, -1, 5]
#min_max_tuple = [slist[0], slist[0]]
#index = 1
#a = find_min_max_from_a_sequence(slist, index, min_max_tuple)
#print('min max', a)
"""
R-1.4 
Write a short Python function that takes a positive integer n and return
the sum of the squares of all the positive integers smaller than n.
"""
def sum_of_squares_of_small_integers(num, sum_of_squares):
	if num == 0: return sum_of_squares
	else:
		num -=1
		sum_of_squares +=num*num
		return sum_of_squares_of_small_integers(num, sum_of_squares)
num            = 5
sum_of_squares = 0
#print('sum_of_squares', sum_of_squares_of_small_integers(num, sum_of_squares))
"""
R-1.5 
Give a single command that computes the sum from Exercise R-1.4, relying on
Python's comprehension syntax and the built-in sum function.
"""
num = 5
sum_of_squares = sum([k*k for k in range(0, num)])
#print('sum_of_squares', sum_of_squares)
"""
R-1.6 
Write a short Python function that takes a positive integer n and returns the 
sum of the squares of all the odd positive integers smaller than n.
"""
num = 5
sum_of_squares = sum([k*k for k in range(1, num, 2)])
#print('sum_of_squares', sum_of_squares)

"""
R-1.7
Give a single command that computes the sum from Exercise R-1.6, relying on Python's 
comprehension syntax and the built-in sum function.
"""	
"""
R-1.8
Python allows negative integers to be used as indices into a sequence,
such as a string. If string s has length n, and expression s[k] is used for index-n<<k<0
what is the equivalent index j>=0 such that s[j] references the same element?
j = index + n

R-1.9
What parameters should be sent to the range constructor, to produce a
range with values 50, 60, 70, 80?
"""
#print(list(range(50, 90, 10)))
#print(list(range(8, -10, -2)))
#print( [2**k for k in range(0, 8)])

"""
R-1.12
Python's random module includes a function choice(data) that returns a
random element from a nonempty sequence. The random module includes a more basic function
 randrange, with parameterization similar to the built-in range function, that return a 
 random choice from the given range. Using only the randrange function, implement your own 
 version of the choice function.
"""
def my_choice(data):
	from random import randrange
	return data[randrange(0, len(data))]
"""
C-1.13
Write a pseudo-code description of a function that reverses a list of n
integers, so that the numbers are listed in the opposite order than they
were before, and compare this method to an equivalent Python function
for doing the same thing.
"""
def reverse(dlist, index):
	if (len(dlist)%2==0) and index == len(dlist)//2-1: 
		return dlist
	elif (len(dlist)%2==1) and index == len(dlist)//2:
		return dlist
	else:
		dlist[index], dlist[len(dlist)-index-1] = dlist[len(dlist)-index-1], dlist[index]
		return reverse(dlist, index+1)
alist = list(range(8))
index = 0
#print('before',alist)
#print('reverse', reverse(alist, index))

"""
C-1.14
Write a short Python function that takes a sequence of integer values and
determines if there is a distinct pair of numbers in the sequence whose
product is odd.
"""
def find_odd_pair(dlist, i, j): # recursion 
	if (i==len(dlist)-2) and (j ==len(dlist)-1):
		if dlist[i] !=dlist[j]:
			return (dlist[i]%2==1) and (dlist[j]%2==1)
		else: return False
	else:
		if (dlist[i]%2==1) and (dlist[j]%2==1) and (dlist[i] !=dlist[j]): 
			return True
		else:
			if j==len(dlist)-1:return find_odd_pair(dlist, i+1, i+2)
			else: return find_odd_pair(dlist, i, j+1)
	
dlist =[1, 2, 4, 1]
i, j = 0, 1
#a = find_odd_pair(dlist, i, j)
#print(a)

"""
C-1.15
Write a Python function that takes a sequence of numbers and determines 
if all the numbers are different from each other (that is, they are distinct).
"""
def check_unique(dlist, i, j):
	if (i==len(dlist)-2) and (j ==len(dlist)-1):
		if (dlist[i] != dlist[j]): return True
		else: False
	else:
		if (dlist[i] ==dlist[j]): return False
		else:
			if j == len(dlist)-1: return check_unique(dlist, i+1, i+2)
			else: return check_unique(dlist, i, j+1)
dlist =list(range(20))
i, j = 0, 1
#print('unique', check_unique(dlist, i, j))
def check_unique2(dlist):
	unique = True
	for i in range(len(dlist)-1):
		for j in range(i, len(dlist)):
			if dlist[i] == dlist[j]:
				unique =  False
				break 
	return unique
"""
C-1.16
No.It won't change data
C-1.17
No. val is a created new instance.
"""
#print([2*k for k in range(0, 10)])
#[chr(ord('a')+k) for k in range(26)]
"""
C-1.21
Write a Python program that repeatedly reads lines from standard input
until an EOFError is raised, and then outputs those lines in reverse order 
(a user can indicate end of input by typing ctrl-D).
"""
def reverse_lines(file_name):
	lines = []
	keepreading =  True
	fout = open(file_name, 'r')
	while keepreading:
		try:
			a = fout.readline()
			print(a)
			lines.append(a)
		except EOFError as e:
			print('End of file')
			keepreading = False
	fout.close()
	for i in range(-1, -len(lines)+1, -1):
		print(lines[i])
	return

#reverse_lines("test.txt")
"""
C-1.24
Write a short Python function that counts the number of vowels in a given
character string.
"""

def find_vowels(slist):
	vowels_dict = ['a','e','i','o','u']
	nvowels = 0
	for a in slist:
		if ord(a)<97:a = chr(ord(a)+32)
		if a in vowels_dict: nvowels+=1
	return nvowels

"""
C-1.26
takes as input three integers, a, b, and c, from the console 
"""

"""
C-1.27
Modify the generator so that it reports factors in increasing order, 
while maintaining its general performance advantages.
"""
def factors(n):
	k = 1
	while k*k<n:
		if n%k==0:
			yield k
			yield n//k
		k +=1
		if k*k ==n:
			yield k
n = 10 
#print(list(factors(n)))

"""
P-1.31
Write a Python program that can make change. Your program should
take two numbers as input, one that is a monetary amount charged and the
other that is a monetary amount given. It should then return the number
of each kind of bill and coin to give back as change for the difference
between the amount given and the amount charged. The values assigned
to the bills and coins can be based on the monetary system of any current
or former government. Try to design your program so that it returns as
few bills and coins as possible.
"""
def make_changes(charged_amount, monetary_amount):
	bills  = [100, 50, 20, 10, 5, 2, 1]
	coins  = [25, 10, 5, 1]
	if monetary_amount<charged_amount:
		print('monetary_amount is not sufficient to make payment')
		return
	else:
		nbills       = len(bills)
		ncoins       = len(coins)
		fractions    = (charged_amount - int(charged_amount))*100.
		fractions    = int(fractions)
		integer_part = int(charged_amount)
		pbills  = [0 for i in range(nbills)]
		pcoins  = [0 for i in range(ncoins)]
		
		for i in range(nbills):
			keepgong = True
			nc       = 0 
			while integer_part>=bills[i]:
				integer_part = integer_part-bills[i]
				nc +=1
			pbills[i] = nc
		print('fractions', fractions)
		for i in range(ncoins):
			nc       = 0
			while fractions>=coins[i]:
				fractions = fractions-coins[i]
				nc +=1
			print(fractions, nc)
			pcoins[i] = nc
		for i in range(nbills):
			print('%d  dollars:  %d'%(bills[i], pbills[i]))
		for i in range(ncoins):
			print('%d  Cents:  %d'%(coins[i], pcoins[i]))
		return 
		
charged_amount  = 121.73
monetary_amount = 130. 
#print('charged_amount', charged_amount)
#make_changes(charged_amount, monetary_amount)
	
	
	

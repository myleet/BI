#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import os

# Chapter 4. Recursion
 
# Reinforcement
"""
R-4.1
Describe a recursive algorithm for finding the maximum element in a sequence, S, of n 
elements. What is your running time and space usage?
"""
def find_max(dlist, index, max_val):
	if index == len(dlist): return max_val
	else: return find_max(dlist, index+1, max(dlist[index], max_val))
'''
from random import shuffle
dlist = list(range(30))
shuffle(dlist)
max_val = dlist[0]
index   = 1
m = find_max(dlist, index, max_val)
print('max', m)
'''

"""
R-4.2 
Draw the recursion trace for the computation of power(2,5), using the traditional function 
implemented in Code Fragment 4.11.
R-4.3
Draw the recursion trace for the computation of power(2,18), using the repeated squaring 
algorithm, as implemented in Code Fragment 4.12.
R-4.4
Draw the recursion trace for the execution of function reverse(S, 0, 5) 
(Code Fragment 4.10) on S = [4, 3, 6, 2, 6].
R-4.5
DrawtherecursiontracefortheexecutionoffunctionPuzzleSolve(3,S,U) (Code Fragment 4.14), 
where S is empty and U = {a, b, c, d}.
R-4.6
Describe a recursive function for computing the nth Harmonic number
R-4.7
Describe a recursive function for converting a string of digits into the in- teger it
represents. For example,   13531   represents the integer 13,531.
R-4.8
Isabel has an interesting way of summing up the values in a sequence A of n integers, 
where n is a power of two. She creates a new sequence B of half the size of A and sets
Otherwise, she replaces A with B, and repeats the process.
What is the running time of her algorithm?
"""

"""
C-4.9 Write a short recursive Python function that finds the minimum and max- imum values 
in a sequence without using any loops.
"""
def find_min_max(dlist, index, min_val, max_val):
	if index == len(dlist): return min_val, max_val
	else: return find_min_max(dlist, index+1, min(dlist[index], min_val), \
	   max(dlist[index], max_val))
"""	
from random import shuffle
dlist = list(range(30))
shuffle(dlist)
min_val = dlist[0]
max_val = dlist[0]
index = 1
print(dlist)
min_val, max_val = find_min_max(dlist, index, min_val, max_val)
print('min', min_val, 'max', max_val)
"""

"""
C-4.10
Describe a recursive algorithm to compute the integer part of the base-two logarithm of n
using only addition and integer division.
"""

def get_integer_part(inum, linum):
	if   inum ==1: return linum
	else:
		inum = inum//2+inum%2
		return get_integer_part(inum, linum+1)

#inum  = 97
#linum = 0
#b = get_integer_part(inum, linum)
#print(b)

"""
C-4.11
Describe an efficient recursive function for solving the element uniqueness problem, 
which runs in time that is at most O(n2) in the worst case without using sorting.
"""
def find_uniqueness(dlist, i, j):
	if (i == len(dlist)-2) and (j==len(dlist)-1):
		if dlist[i] == dlist[j]:
			return False
		else: return True
	else:
		if dlist[i] == dlist[j]:
			return False
		else:
			if (j == len(dlist)-1):
				return find_uniqueness(dlist, i+1, i+2)
			else:
				return find_uniqueness(dlist, i, j+1)
	
#from random import shuffle
#dlist = list(range(30))
#dlist.append(19)
#shuffle(dlist)
#i  = 0
#j  = 1
#a = find_uniqueness(dlist, i, j)
#print(a)
"""
C-4.12 
Give a recursive algorithm to compute the product of two positive integers,
m and n, using only addition and subtraction.
"""
def get_product_recurr(m, n, product):
	if n==0: return product
	else:    return get_product_recurr(m, n-1, product+m)

#product = 0
#m = 5
#n = 8
#p = get_product_recurr(m, n, product)
#print('p', p)
"""
C-4.14
In the Towers of Hanoi puzzle,we are given a plat form with three pegs,a, b, and c, 
sticking out of it. On peg a is a stack of n disks, each larger than the next, so that 
the smallest is on the top and the largest is on the bottom. The puzzle is to move all 
the disks from peg a to peg c, moving one disk at a time, so that we never place a larger
disk on top of a smaller one. See Figure 4.15 for an example of the case n = 4. 
Describe a recursive algorithm for solving the Towers of Hanoi puzzle for arbitrary n. 
(Hint: Consider first the subproblem of moving all but the nth disk from peg a to another 
peg using the third as temporary storage.)
"""
def hanoi_tower(alist, blist, clist):

	if len(alist) ==1: 
		clist.append(alist[0])
		del alist[0]
		return alist, blist, clist
		
	if len(alist) == 2:
		blist.append(alist[0])
		del alist[0]
		clist.append(alist[0])
		del alist[0]
		clist.insert(0, blist[0])
		del blist[0]
		return alist, blist, clist
	
"""
C-4.15
Write a recursive function that will output all the subsets of a set of n
elements (without repeating any subsets). Combination ;
"""
def get_sub(nset_list, out):
	if len(nset_list) <= 2:
		out.append(nset_list)
		out.append([nset_list[0]])
		out.append([nset_list[1]])
		return out
	else:
		a = nset_list[0]
		del nset_list[0]
		myout = get_sub(nset_list, out)
		for i in range(len(myout)):
			out.append(myout[i]+[a])
		out.append([a])
		return out
"""
solution
out = [] 
nset_list = ['a', 'b', 'c', 'd', 'e']
get_sub(nset_list, out)
nc = 0
while nc <=5:
	for i in range(len(out)):
		if len(out[i]) == nc:
			print (i, out[i])
	nc +=1
"""
"""
C-4.16, C-4.17
Write a short recursive Python function that takes a character string s and outputs its reverse. For example, the reverse of pots&pans would be
snap&stop 
"""
slist = 'abcdefg'

def reverse_string(slist):
	if len(slist) == 2: return slist[1]+ slist[0]
	else: return reverse_string(slist[1:])+ slist[0]

def is_a_palindrome(slist):       # palindrome is a string that is equivalent to its reverse
	rlist = reverse_string(slist)
	if rlist == slist: return True
	else:              return False

"""
C-4.19
Write a short recursive Python function that rearranges a sequence of integer 
values so that all the even values appear before all the odd values.
"""
def move_all_even_to_front(slist, index):
	if (index == len(slist)-1):
		return
	else:
		if slist[index]%2 == 1:
			nswap = 1
			while  (slist[index+nswap]%2 ==1) and (index+nswap <len(slist)-1): 
				nswap +=1
			if index+nswap > len(slist)-1: return
			else:
				slist[index], slist[index+nswap] = slist[index+nswap], slist[index]
		index +=1
		return move_all_even_to_front(slist, index)

#slist = list(range(23))
#index = 0
#move_all_even_to_front(slist, index)
#print(slist)

"""
C-4.20
Given an unsorted sequence, S, of integers and an integer k, describe a recursive 
algorithm for rearranging the elements in S so that all elements less than or equal 
to k come before any elements larger than k. What is the running time of your 
algorithm on a sequence of n values? linear of N
"""
def move_elements_less_than_k_to_front(slist, k, curr_index, k_pos):
	if (curr_index == len(slist) -1):
		if slist[curr_index] <=k:
			slist[curr_index], slist[k_pos+1] = slist[k_pos+1], slist[curr_index]
		return
	else:
		if slist[curr_index]<=k:
			slist[curr_index], slist[k_pos+1] = slist[k_pos+1], slist[curr_index]
			return move_elements_less_than_k_to_front(slist, k, curr_index+1, k_pos+1)
		else:
			return move_elements_less_than_k_to_front(slist, k, curr_index+1, k_pos)
"""
# solution of C-4.20
from random import shuffle
slist =list(range(20))
shuffle(slist)
k     = 10
k_pos = -1
print(slist)
curr_index = 0
move_elements_less_than_k_to_front(slist, k, curr_index, k_pos)
print(slist)
"""

"""
C-4.21
Suppose you are given an n-element sequence, S, 
containing distinct integers that are listed in increasing order. 
Given a number k, describe a recursive algorithm to find two integers in S that sum to k, 
if such a pair exists. What is the running time of your algorithm?
"""
def sum_equal_to_k(slist, k):
	if len(slist) == 2:
		if sum(slist) ==k:
			return slist[0], slist[1]
		else: 
			return None, None
	else:
		for i in range(1, len(slist)):
			if slist[i] == k - slist[0]:
				return slist[i], slist[0]
		return sum_equal_to_k(slist[1:], k)
'''
# solution, N*(N-1) 	
slist = [2, 3, 4, 6, 7, 9, 20, 27]
k = 11
a, b = sum_equal_to_k(slist, k)
print(a, b)
'''

"""
C-4.22
Develop a nonrecursive implementation of the version of power from Code 
Fragment 4.12 that uses repeated squaring.
"""
def pow_sqare(x, n):
	if n == 0:
		return 1.
	else:
		p = 1.0
		for i in range(1, n+1):
			p *=x
		return p
"""
x = 2.
for i in range(4):
	print (i, pow_sqare(x, i))
"""
###---------------------------Example
"""
Example: English ruler
"""
def draw_line(tick_length, tick_label=''):
	line ='-'*tick_length
	if tick_label:
		line +=' '+tick_label
	print(line)

def draw_interval(center_length):
	if center_length>0:
		draw_interval(center_length - 1)
		draw_line(center_length)
		draw_interval(center_length - 1)
		
def draw_ruler(num_inches, major_length):
	draw_line(major_length, '0')
	for j in range(1, 1+num_inches):
		draw_interval(major_length - 1)
		draw_line(major_length, str(j))
		
if __name__=='__main__':
	num_inches   = 2
	major_length = 4
	draw_ruler(num_inches, major_length)
	
#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import os

def disk_usage(path):
	total = os.path.getsize(path)
	if os.path.isdir(path):
		for filename in os.listdir(path):
			childpath = os.path.join(path, filename)
			total += disk_usage(childpath)
	print('{0:<7}'.format(total), path)
	return total
path ='/Volumes' 
t = disk_usage(path)
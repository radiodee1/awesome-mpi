#!/usr/bin/env python

import array_setup as mp
import numpy

print
for x in range (0,12):
	if x < 11:
		print '#',
	else:
		print '#'

for y in range (0 , 10):
	print '#',
	for x in range (0, 10):
		if mp.main[ (y * 10) + x] == mp.FREE :
			print y,#' ',
		if mp.main[ (y * 10) + x] == mp.START :
			print 'S',
		if mp.main[ (y * 10) + x] == mp.END :
			print 'X',
		if mp.main[ (y * 10) + x] == mp.WALL :
			print '#',
	print '#',
	print

for x in range (0,12):
	print '#',
print

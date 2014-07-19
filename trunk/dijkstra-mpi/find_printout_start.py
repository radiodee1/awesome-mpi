#!/usr/bin/env python

import array_setup as mp
import numpy

print
for x in range (0, mp.width +2):
	if x < mp.width +1:
		print '#',
	else:
		print '#'

for y in range (0 , mp.height):
	print '#',
	for x in range (0, mp.width):
		if mp.main[ (y * mp.width) + x] == mp.FREE :
			print ' ',
		if mp.main[ (y * mp.width) + x] == mp.START :
			print 'S',
		if mp.main[ (y * mp.width) + x] == mp.END :
			print 'X',
		if mp.main[ (y * mp.width) + x] == mp.WALL :
			print '#',
	print '#',
	print

for x in range (0, mp.width + 2):
	print '#',
print

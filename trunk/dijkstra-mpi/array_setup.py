#!/usr/bin/python

#from mpi4py import MPI
import numpy
import math
import sys


	
main = [0] * 100 
visited = [] #[0]  * 100 
prev = [0] * 100 
dist = [999] * 100

for i in range(100) :
	visited.append(0)

startx = 1
starty = 0
endx = 5
endy = 9

#enum
OPEN = 1
WALL = 2
START = 3
END = 4
VISITED = 1
FREE = 0

for y in range (0 , 10):
	for x in range (0, 10):
		main[ (y * 10) + x] = FREE
		if startx == x and starty == y :
			main[ (y * 10) + x] = START
		if endx == x and endy == y :
			main[ (y * 10) + x] = END
			
visited[(starty * 10) + startx] = VISITED

			
#non-random walls

for i in range (0, 7) :
	main[ (4 * 10) + i] = WALL
	
for i in range (4, 10) :
	main[ (7 * 10) + i] = WALL
	

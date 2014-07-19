#!/usr/bin/python

import sys
import fileinput

width = 15#10
height = 10

## make csv file import-able ##
dim = []
wall = []
csv = False
i = 0
if len(sys.argv) > 1:
	csv = True
	#print sys.argv[1]
	for line in fileinput.input(sys.argv[1]):
		if not '#' in line[0] :
			i += 1
			if i == 1:
				#print 'dim:', line
				dim = line.split(',')
				width = int(dim[0])
				height = int(dim[1])
			if i == 2:
				#print 'wall-csv:', line
				wall = line.split(',')
			

starttime = 0
endtime = 0

startx = 1
starty = 9#0
endx = 13
endy = 0#9

#enum
OPEN = 1
WALL = 2
START = 3
END = 4
PATH = 5
VISITED = 1
FREE = 0
UNDEFINED = 999

main = [0] * (width * height) 
visited = [0] * (width * height)
prev = [-1] * (width * height)
dist = [UNDEFINED] * (width * height)
found = []


for y in range (0 , height):
	for x in range (0, width):
		main[ (y * width) + x] = FREE
		if startx == x and starty == y :
			main[ (y * width) + x] = START
		if endx == x and endy == y :
			main[ (y * width) + x] = END
			
visited[(starty * width) + startx] = 0
dist[(starty * width) + startx] = 0
prev[(starty * width) + startx] = 0

main[(starty * width) + startx] = START

# wall from file input
if csv == True:
	for i in wall :
		#print int(i)
		main[int(i)] = WALL

# non-random walls

for i in range (0, 7) : #(0,7)
	main[ (4 * width) + i] = WALL
	
for i in range (4, width) :
	main[ (7 * width) + i] = WALL
	


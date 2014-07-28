#!/usr/bin/python


# comment in for csv file
import sys, math
import fileinput
import pyopencl as cl

width = 8#30
height = 8#30

## make csv file import-able ##
dim = []
wall = []
csv = False
gui = True

# comment in for csv file

if len(sys.argv) > 1:
	for j in range(0, len(sys.argv)):
		if sys.argv[j] == '-nogui':
			gui = False
		
if gui == True:
	# 5 is the number of buffers (maze, dist, prev, visited, mutex)
	dimension = int(math.sqrt(cl.device_info.MAX_WORK_GROUP_SIZE / 5))
	width = dimension
	height = dimension

i = 0
k = 0
if len(sys.argv) > 1 : 
	#csv = True
	
	for j in range(0, len(sys.argv)):
		if sys.argv[j].endswith('.txt'):
			csv = True
			k = j
			for line in fileinput.input(sys.argv[k]):
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

startx = 3
starty = 0#height - 1
endx = width - 3
endy =  height - 1

#enum for maze
OPEN = 1
WALL = 2
START = 3
END = 4
PATH = 5

#enum for visited
VISITED = 1
FREE = 0

#enum for distance
UNDEFINED = -1


maze = [0] * (width * height) 
#visited = [0] * (width * height)
#prev = [-1] * (width * height)
dist = [UNDEFINED] * (width * height)
#found = []


for y in range (0 , height):
	for x in range (0, width):
		maze[ (y * width) + x] = FREE
		if startx == x and starty == y :
			maze[ (y * width) + x] = START
		if endx == x and endy == y :
			maze[ (y * width) + x] = END
			

dist[(starty * width) + startx] = 0
#prev[(starty * width) + startx] = -1

maze[(starty * width) + startx] = START

# wall from file input
if csv == True:
	for i in wall :
		#print int(i)
		if int(i) < width * height:
			#print 'add wall'
			maze[int(i)] = WALL

# non-random walls
onethird = int(height / 3)
twothirds = int(height * 2 / 3 )
for i in range (0, 6) : #(0,7)
	maze[ (onethird * width) + i] = WALL
	
for i in range (4, width) :
	maze[ (twothirds * width) + i] = WALL
	
# test for unreachable goal	
#for i in range (0, width) :
#	maze[ (twothirds * width) + i] = WALL


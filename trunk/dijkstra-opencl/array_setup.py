#!/usr/bin/python


# comment in for csv file
import sys
import fileinput


width = 10#20
height = 10#10

## make csv file import-able ##
dim = []
wall = []
csv = False


# comment in for csv file
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
		if i < width * height:
			maze[int(i)] = WALL

# non-random walls
onethird = int(height / 3)
twothirds = int(height * 2 / 3 )
for i in range (0, 7) : #(0,7)
	maze[ (onethird * width) + i] = WALL
	
for i in range (4, width) :
	maze[ (twothirds * width) + i] = WALL
	
# test for unreachable goal	
#for i in range (0, width) :
#	maze[ (twothirds * width) + i] = WALL


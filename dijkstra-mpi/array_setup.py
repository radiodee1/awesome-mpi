#!/usr/bin/python

width = 15#10
height = 10

starttime = 0
endtime = 0

startx = 1
starty = 0
endx = 5
endy = 9

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
visited = [] 
prev = [-1] * (width * height)
dist = [UNDEFINED] * (width * height)
found = []

for i in range(width * height) :
	visited.append(0)

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

#non-random walls

for i in range (0, 7) : #(0,7)
	main[ (4 * width) + i] = WALL
	
for i in range (4, width) :
	main[ (7 * width) + i] = WALL
	


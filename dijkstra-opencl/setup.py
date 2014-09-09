#!/usr/bin/python


import sys, math
import fileinput
import pyopencl as cl
from PIL import Image

class SU(object):

	def __init__(self) :
		self.mapname = ''

		self.width = 8#30
		self.height = 8#30

		self.window_w = 480
		self.window_h = 480

		self.dim = []
		self.wall = []
		self.wallout = []
		self.csv = False
		self.gui = True
		self.output = False
		self.dim_input = 0
		self.single_kernel = False
		self.use_diag = True

		if len(sys.argv) > 1:
			for j in range(0, len(sys.argv)):
				if sys.argv[j] == '-single-kernel':
					print 'must try single kernel!'
					self.single_kernel = True

		if len(sys.argv) > 1:
			for j in range(0, len(sys.argv)):
				if sys.argv[j] == '-size':
					self.dim_input = int(sys.argv[j+1])
					if self.dim_input > 480 : self.dim_input = 480

		if len(sys.argv) > 1:
			for j in range(0, len(sys.argv)):
				if sys.argv[j] == '-output':
					self.output = True

		if len(sys.argv) > 1:
			for j in range(0, len(sys.argv)):
				if sys.argv[j] == '-no-diagonal':
					print 'no diagonals!'
					self.use_diag = False

		if len(sys.argv) > 1:
			for j in range(0, len(sys.argv)):
				if sys.argv[j] == '-nogui':
					self.gui = False
		
		if self.gui == True:
			## 5 is the number of buffers (maze, dist, prev, visited, mutex) ##
			self.dimension = int(math.sqrt(cl.device_info.MAX_WORK_GROUP_SIZE / 5))
			## if double kernel is used, 'dimension' is less important!! ##
			self.dimension = 60
			if self.dim_input != 0 : self.dimension = self.dim_input
			self.width = self.dimension
			self.height = self.dimension
			### choose map, etc.
			self.choose_opts()

		i = 0
		k = 0
		m = 0
		tstartx = 0
		tstarty = 0
		tendx = 0
		tendy = 0
		if len(sys.argv) > 1 : 
			#csv = True
	
			for j in range(0, len(sys.argv)):
				if sys.argv[j].endswith('.txt'):
					self.csv = True
					k = j
					for line in fileinput.input(sys.argv[k]):
						if not '#' in line[0] :
							i += 1
							if i == 1:
								#print 'dim:', line
								dim = line.split(',')
								self.width = int(dim[0])
								self.height = int(dim[1])
							if i == 2:
								#print 'wall-csv:', line
								self.wall = line.split(',')
							if i > 2 and i < 7:
								m += 1
							if i == 3:
								tstartx = int(line)
							if i == 4:
								tstarty = int(line)
							if i == 5:
								tendx = int(line)
							if i == 6:
								tendy = int(line)
								
					if m == 4 :
						self.startx = tstartx
						self.starty = tstarty
						self.endx = tendx
						self.endy = tendy

		self.starttime = 0
		self.endtime = 0

		if self.csv == False :
			self.startx = 3
			self.starty = 0# height - 1
			self.endx = self.width - 3
			self.endy =  self.height - 1

		#enum for maze
		self.OPEN = 1
		self.WALL = 2
		self.START = 3
		self.END = 4
		self.PATH = 5

		#enum for visited
		self.VISITED = 1
		self.FREE = 0

		#enum for distance
		self.UNDEFINED = 16000000#-1


		self.maze = [0] * (self.width * self.height) 
		self.dist = [self.UNDEFINED] * (self.width * self.height)


		for y in range (0 , self.height):
			for x in range (0, self.width):
				self.maze[ (y * self.width) + x] = self.FREE
				if self.startx == x and self.starty == y :
					self.maze[ (y * self.width) + x] = self.START
				if self.endx == x and self.endy == y :
					self.maze[ (y * self.width) + x] = self.END
			

		self.dist[(self.starty * self.width) + self.startx] = 0

		self.maze[(self.starty * self.width) + self.startx] = self.START

		# wall from file input
		if self.csv == True:
			for i in self.wall :
				#print int(i)
				
				if i != '' and i.isdigit() :
					if int(i) < self.width * self.height:
						#print 'add wall'
						self.maze[int(i)] = self.WALL

		# non-random walls
		if self.csv == False:
			onethird = int(self.height / 3)
			twothirds = int(self.height * 2 / 3 )
			for i in range (0, 6) : #(0,7)
				self.maze[ (onethird * self.width) + i] = self.WALL
	
			for i in range (4, self.width) :
				self.maze[ (twothirds * self.width) + i] = self.WALL
	
	def choose_opts(self):
		print '----------options: window/size/map----------'
		print '''
The 'map.png' works best with a large window size and 
a smaller selection size. That way the content is
magnified.
		
The 'maze.png' works best if you select the defaults
on all inputs. Just hit the return key for window
size and selection size.
		'''
		i = 0
		mapname = ['map.png','maze.png']
		for line in mapname : 
			i += 1
			print '[', i, ']', line
		mapmessage = str('map number ( 1 to '+str(i)+' ) :')
		mapnum = raw_input(mapmessage)
		if mapnum == '':
			mapnum = 1
		self.mapname = mapname[int(mapnum )-1]
		
		surface = Image.open(self.mapname)
		w , h = surface.size
		if (h > w) : image_size = h
		else : image_size = w
		
		print 'image stats: ', self.mapname
		print 'width x height', w,'x',h
		
		win = raw_input('window size = 480 to 600 :')
		if (win == '') :
			print 'set window size default -', image_size
			self.window_w = int(image_size)
			self.window_h = int(image_size)
		else:
			print 'set window size selected -', win 
			self.window_w = int (win)
			self.window_h = int (win)
		
		size = raw_input( 'selection size = 100 to window-size :')
		if size == '' :
			sizeint = int(self.window_w)
		else :
			sizeint = int(size)
		self.width = sizeint
		self.height = sizeint
		#cl.width = sizeint
		#cl.height = sizeint
		
	def get_y(ii):
		return int (ii / self.width)

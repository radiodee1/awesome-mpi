#!/usr/bin/env python

import pyopencl as cl
import numpy
import time, math

import fileinput
import pygame as pg
import pygame.gfxdraw as pgd
import pygame
import sys

import setup as ar

class CL(object):


	def __init__(self, array):
		self.mz = array
		self.width = self.mz.width
		self.height = self.mz.height
		self.size = self.mz.width * self.mz.height
		self.prev = []
		self.maze = self.mz.maze
		self.found = []
		self.oo_ex = False
		
		self.DIM_WIDTH = 0
		self.DIM_HEIGHT = 1
		self.DIM_DONE = 2
		self.DIM_USE_DIAG = 3
		
		#print cl.device_info.LOCAL_MEM_SIZE, 'local mem size'
		print cl.device_info.MAX_WORK_GROUP_SIZE, 'max work group size'
		#print cl.device_info.QUEUE_PROPERTIES, 'queue properties'
		#print cl.kernel_work_group_info.WORK_GROUP_SIZE, 'work group size'
		#print cl.kernel_work_group_info.PREFERRED_WORK_GROUP_SIZE_MULTIPLE , 'preferred size'
		
		print self.mz.width * self.mz.height * 5 , 'calculated use'# 5 is num of full buffers!
		
		#print 'estimated:' , int(math.sqrt(cl.device_info.MAX_WORK_GROUP_SIZE / 5))
		
		self.ctx = cl.create_some_context()
		
		try: 
			if self.mz.single_kernel == True :
				self.queue = cl.CommandQueue(self.ctx,
					properties = cl.command_queue_properties.OUT_OF_ORDER_EXEC_MODE_ENABLE)
				self.oo_ex = True
			else :
				self.queue = cl.CommandQueue(self.ctx, properties = 0)#
				self.oo_ex = False
		except:
			self.queue = cl.CommandQueue(self.ctx, properties = 0)#
			self.oo_ex = False

	def load_kernel(self):
		fstr = ''
		for line in fileinput.input('find.cl'):
			fstr += line

		self.program = cl.Program(self.ctx, fstr).build()

	def set_buffers(self):
		#
		mf = cl.mem_flags

		startvisited = [self.mz.FREE] * self.size
		startdist = [self.mz.UNDEFINED] * self.size
		startprev = [self.mz.UNDEFINED] * self.size
		
		startvisited[(self.mz.starty * self.width) + self.mz.startx] = self.mz.VISITED 
		startdist[(self.mz.starty * self.width) + self.mz.startx] = 0
		self.maze[(self.mz.starty * self.width) + self.mz.startx] = self.mz.START 
		
		
		self.maze = numpy.array(self.maze, dtype=numpy.int32)
		self.visited = numpy.array((startvisited), dtype=numpy.int32)
		self.dist = numpy.array((startdist), dtype=numpy.float32)
		self.prev = numpy.array((startprev), dtype=numpy.int32)
		self.mutex = numpy.array(([self.mz.FREE] * self.size), dtype=numpy.int32)
		
		prepdim = [0] * 4#self.size
		prepdim[self.DIM_WIDTH] = self.width
		prepdim[self.DIM_HEIGHT] = self.height
		
		if self.mz.use_diag : prepdim[self.DIM_USE_DIAG] = 1
		else : prepdim[self.DIM_USE_DIAG] = 0
		
		self.dimension = numpy.array((prepdim), dtype=numpy.int32)
			           
		self.maze_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR,
					           hostbuf=self.maze)   
	
		self.visited_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
								hostbuf=self.visited)
		self.dist_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
								hostbuf=self.dist)
		self.prev_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
								hostbuf=self.prev)
		self.dimension_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
								hostbuf=self.dimension)

		self.mutex_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
								hostbuf=self.mutex)


	def execute(self):
	
		visited = numpy.empty_like(self.maze)
		dist = numpy.empty_like(self.dist)
		prev = numpy.empty_like(self.maze)
		dimension = numpy.empty_like(self.dimension)
		loop = 0
		j = 0
		
		while loop == 0 and j < self.size * 15:
			j += 1
			print j,
			#print 'here',
			if self.oo_ex: ## out-of-order execution -- single kernel
				self.program.find(self.queue, self.maze.shape,None,#self.maze.shape, 
					self.maze_buf, 
					self.visited_buf, 
					self.dist_buf, 
					self.prev_buf, 
					self.mutex_buf,
					self.dimension_buf)
			else:
				self.program.part0(self.queue, self.maze.shape,None,#self.maze.shape, 
					self.maze_buf, 
					self.visited_buf, 
					self.dist_buf, 
					self.prev_buf, 
					self.mutex_buf,
					self.dimension_buf)
				
				
				self.program.part1(self.queue, self.maze.shape,None,#self.maze.shape, 
					self.maze_buf, 
					self.visited_buf, 
					self.dist_buf, 
					self.prev_buf, 
					self.mutex_buf,
					self.dimension_buf)
				
			
			
			cl.enqueue_read_buffer(self.queue, self.dimension_buf, dimension).wait()        
			
			loop = dimension[self.DIM_DONE]
		
		'''
			at some point may remove 'wait' on visited_buf and dist_buf!!
		'''
		print 'loop end', loop
		#cl.enqueue_read_buffer(self.queue, self.visited_buf, visited).wait()
		#self.visited = visited
		
		cl.enqueue_read_buffer(self.queue, self.dist_buf, dist).wait()
		self.dist = dist
		
		cl.enqueue_read_buffer(self.queue, self.prev_buf, prev).wait()        
		self.prev = prev
		
		
		
	
	def follow_path(self) :
		
		dim = self.width * self.height
		if True: 
			if self.mz.gui == False:
				print self.prev, 'prev'
			i = 0 
			self.found = []
		
			found = self.prev[(self.mz.endy * self.width) + self.mz.endx]

			while (found != self.mz.UNDEFINED) and i < self.width * self.height :
				if found != self.mz.UNDEFINED:
					self.found.append(int(found))
				else :
					print int( found / width), found - (int(found / width) * width), 'y,x'
				found = self.prev[found]
				i += 1
			print self.found, 'found', len(self.found)
			
			i = 0
			while (i < dim) :
				if ( i in self.found) and self.maze[i] != self.mz.START:
					self.maze[i] = self.mz.PATH
					
				i += 1	
		
	def get_prev(self):
		return self.prev

	def get_visited(self):
		return self.visited

	def get_dist(self):
		return self.dist

	def get_width(self):
		return self.width
	
	def get_height(self):
		return self.height
		
	def get_maze(self):
		return self.maze	
			
	def set_map(self, maze, width=-1, height=-1):
		self.maze = maze
		if width == -1:
			self.width = self.mz.width
		else:
			self.width = width
			self.mz.width = width
			
		if height == -1:
			self.height = self.mz.height
		else:
			self.height = height
			self.mz.width = width
		

class Interface(object) :

	def __init__(self, array):
		self.mz = array
		self.mapname = 'map.png'
		self.iconname = 'icon.png'
		self.map  =[]
		self.w = 480
		self.h = 480
		self.quit = 0	
		
	def choose_opts(self, cl):
		print 'options: window/size/map'
		print 'window size = 480 - 600 '
		
		print 'selection size = 10 - window size'
		print 'map = choose map'
		 
		
		
	def solve_png(self , cl):
	
		if self.mz.gui == False:
			cl.set_map(self.mz.maze, self.mz.width, self.mz.height)
			return
	
		x = 0
		y = 0
		white = (64, 64, 64)
		#self.w = 480 
		#self.h = 480 
		self.startx = -1
		self.starty = -1
		self.endx = -1
		self.endy = -1
		
		self.guiwidth = cl.width
		self.guiheight = cl.height
		
		surface = pg.image.load(self.mapname)
		icon = pg.image.load(self.iconname)
		
		pg.display.set_icon(icon)
		
		## initialize control components ##
		gray = (16,16,16)
		red =(255,0,0)
		green = (0,255,0)
		blue = (0,0,255)
		self.boxborder = 5
		self.boxwidth = 48
		self.boxheight = 16
		self.box = pg.Surface((self.boxwidth + (self.boxborder * 2), 
			self.boxheight + (self.boxborder * 2)))
		self.box.fill(gray)
		boxred = pg.Surface((16,16))
		boxred.fill(red)
		boxgreen = pg.Surface((16,16))
		boxgreen.fill(green)
		boxblue = pg.Surface((16,16))
		boxblue.fill(blue)
		self.box.blit(boxgreen, (0 + self.boxborder,0 + self.boxborder))
		self.box.blit(boxred, (16 + self.boxborder,0 + self.boxborder))
		self.box.blit(boxblue, (32 + self.boxborder, 0 + self.boxborder))
		self.mousex = 0
		self.mousey = 0
		self.boundtop = self.h - (self.box.get_height() - self.boxborder)
		self.boundbottom = self.h - self.boxborder
		self.boundgreenleft = self.w - (self.box.get_width() -  self.boxborder)
		self.boundgreenright = self.w - (self.box.get_width() -  self.boxborder) + 16
		self.boundredleft = self.w - (self.box.get_width() -  self.boxborder) + 16
		self.boundredright = self.w - (self.box.get_width() -  self.boxborder) + 32
		self.boundblueleft = self.w - (self.box.get_width() -  self.boxborder) + 32
		self.boundblueright = self.w - (self.box.get_width() -  self.boxborder) + 48
		blocksize = (self.w /cl.width) -2
		if blocksize <= 2 : blocksize = 4
		self.startblock = pg.Surface((blocksize,blocksize))
		self.startblock.fill(green)
		self.endblock = pg.Surface((blocksize,blocksize))
		self.endblock.fill(red)
		self.pathblock = pg.Surface((blocksize,blocksize))
		self.pathblock.fill(blue)
		self.blockoffset = 0#blocksize / 2 
		
		self.fixscale = (float  ( self.w - (int ( self.w/ cl.width  ) * cl.width ))/ self.w) + 1
		#print self.fixscale, 'fixme'
		self.wallbox = pg.Surface( (  math.ceil((self.w/cl.width) * self.fixscale), 
			math.ceil((self.h/cl.height ) * self.fixscale)))
		self.wallbox.fill((0,0,0))
		
		
		screensurf = surface
		screen = pg.display.set_mode((self.w , self.h ))
		pg.display.set_caption('dijkstra-opencl', 'dijkstra-opencl')
		screen.fill((white))
		
		self.quit = 0
		running = 1
		
		if self.mz.csv != True:
			## display first screen ##
			while running:

				for event in pg.event.get():
					if event.type == pg.QUIT:
						running = 0
						self.quit = 1	
					if event.type == pg.KEYUP:
						if event.key == pg.K_RETURN:
							running = 0
						if event.key == pg.K_UP:
							y -= 5
							if y < 0 : 
								y = 0
						if event.key == pg.K_DOWN:
							y += 5
							if y + cl.height > screen.get_height() : 
								y = screen.get_height() - cl.height 
							
						if event.key == pg.K_LEFT:
							x -= 5
							if x < 0 : 
								x = 0
						if event.key == pg.K_RIGHT:
							x += 5
							if x + cl.width > screen.get_width() : 
								x = screen.get_width() - cl.width 			
			
				screensurf = surface.copy()
				screen.fill(white)
				screen.blit(screensurf,(0,0))
				pgd.rectangle(screen, ((x,y),(cl.width,cl.height)), (255,0,0))
				pg.display.flip()
			
			## display second screen ##
			screen.fill((white))
			self.smallsurf = pg.Surface((cl.width, cl.height))
			bwsurf = pg.Surface((cl.width, cl.height))
			self.smallsurf.blit(surface,(0,0),((x,y), (cl.width, cl.height)))
		
		
			pg.transform.threshold(bwsurf, self.smallsurf,
				(0,0,0,0),(20,20,20,0), (255,255,255,0), 1)	
		
		screensurf = pg.Surface((self.w, self.h))
		screensurf.fill((255,255,255))
		screen.fill((255,255,255))
		
		if self.mz.csv == True:
			self.sa = self.mz.maze
			cl.width = self.mz.width
			cl.height = self.mz.height
			
		else:
			## convert to array representation ##
			self.sa = [0] * cl.width * cl.height
			pxarray = pygame.PixelArray(self.smallsurf)
		
		for yy in range (0, cl.width):
			for xx in range (0, cl.height):
				
				
				if self.mz.csv == True:
					p = self.sa[(yy * cl.width ) + xx]
				else:
					p =  pxarray[xx,yy]

					if p == 0 : p = self.mz.WALL
					else : p = 0
					self.sa[(yy * cl.width) + xx] = p
					
				if p == self.mz.WALL:
					self.mz.wallout.append((yy * cl.width) + xx)
				
					## print walls to screen ! ##
					xxx = float(xx * ( self.fixscale)) 
					yyy = float(yy * ( self.fixscale)) 
					screensurf.blit(self.wallbox, 
						(float(xxx * float (self.w  / cl.width))   ,
						float(yyy * float (self.h  / cl.height))   ))
	
		self.gui_state = 0
	
		self.PLACE_START = 1
		self.PLACE_END = 2
		self.FIND_PATH = 3
		self.HOLD_START = 4
		self.HOLD_END = 5
	
		self.running = 1
		while self.running == 1 and self.quit == 0:
		
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = 0
					self.quit = 1	
		
			# skip input if text file is used
			if self.mz.csv == True: 
				self.running = 0
		
			screen.fill((white))
			screen.blit(screensurf,(0,0))
			self.gui_controls(screen, event, self.w, self.h)
			pg.display.flip()
	

		if self.mz.csv == False :
			self.mz.endx = self.endx
			self.mz.endy = self.endy
	
			self.mz.startx = self.startx
			self.mz.starty = self.starty
	
		elif self.mz.csv == True :
			self.startx = self.mz.startx
			self.starty = self.mz.starty
			self.endx = self.mz.endx
			self.endy = self.mz.endy
			self.quit = 0
		
		if self.quit != 1:
			#print len(sa)
			self.sa[int((self.starty * cl.width) + self.startx)] = self.mz.START
			self.sa[int((self.endy * cl.width) + self.endx)] = self.mz.END
			cl.set_map(self.sa, cl.width, cl.height)
			starttime = time.clock()
			cl.load_kernel()
			cl.set_buffers()
			cl.execute()
			endtime = time.clock()
			print  endtime - starttime , 'time on gpu'
			cl.follow_path()
		
		## print screen with solution ##
		self.running = 1
		while self.running == 1 and self.quit == 0:
			
			
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = 0
					self.quit = 1	
			
				if self.mz.csv == False :
					if event.type == pg.KEYUP:
						if event.key == pg.K_RETURN:
							self.running = 0
			
					if event.type == pg.MOUSEBUTTONDOWN:
			
						left , middle, right = pg.mouse.get_pressed() 
						if left == True:
							self.running = 0
				
			
			screen.fill((white))
			screen.blit(screensurf,(0,0))
			for i in cl.found :
				xx = i - ( cl.get_width() * (int(i / cl.get_width() )))
				yy = int(i / cl.get_width())
			
				xxx = float(xx * ( self.fixscale)) 
				yyy = float(yy * ( self.fixscale)) 
				
				screen.blit(self.pathblock,
					(float(xxx * float(screen.get_width() / cl.width)) + self.blockoffset,
					float(yyy * float(screen.get_width() / cl.width)) + self.blockoffset))
				screen.blit(self.startblock,
					(self.startx * (screen.get_width() / cl.width) * self.fixscale, 
					self.starty * (screen.get_width() / cl.width) * self.fixscale))
				screen.blit(self.endblock,
					(self.endx * (screen.get_width() / cl.width) * self.fixscale,
					self.endy * (screen.get_width() / cl.width) * self.fixscale))
			pg.display.flip()

	def gui_controls(self, screen, event, w , h):
		# this helper function puts controls on the screen
		screen.blit(self.box ,( w -  (self.box.get_width()), 
			h - (self.box.get_height())) )
		# detect mouse
		self.mousex , self.mousey = pg.mouse.get_pos()
		self.mousex = self.mousex - (self.wallbox.get_width() / 2)
		self.mousey = self.mousey - (self.wallbox.get_height() / 2)
		if event.type == pg.MOUSEBUTTONDOWN:
			#print 'here mouse'
			left , middle, right = pg.mouse.get_pressed() 
			if left == True:
				
				if self.mousey > self.boundtop \
						and self.mousey < self.boundbottom :
					if self.mousex > self.boundredleft and self.mousex < self.boundredright:
						self.gui_state = self.HOLD_END
						self.endx = -1
						self.endy = -1
					if self.mousex > self.boundgreenleft and self.mousex < self.boundgreenright:
						self.gui_state = self.HOLD_START
						self.startx = -1
						self.starty = -1
					if self.mousex > self.boundblueleft and self.mousex < self.boundblueright:
						self.running = 0
						self.gui_state = self.FIND_PATH

				elif self.gui_state == self.PLACE_START:
					if self.mousex < self.wallbox.get_width() * self.mz.width and \
							self.mousey < self.wallbox.get_height() * self.mz.height :
						startx = self.mousex / (screen.get_width() / self.smallsurf.get_width()) 
						starty = self.mousey / (screen.get_height()/ self.smallsurf.get_height())
						
						self.startx, self.starty = self.dot_not_on_wall(startx, starty)
						
				elif self.gui_state == self.PLACE_END:
					if self.mousex < self.wallbox.get_width() * self.mz.width and \
							self.mousey < self.wallbox.get_height() * self.mz.height :
						endx = self.mousex / (screen.get_width() / self.smallsurf.get_width()) 
						endy = self.mousey / (screen.get_height()/ self.smallsurf.get_height())
						
						self.endx, self.endy = self.dot_not_on_wall(endx, endy)
						
				elif self.gui_state == self.HOLD_START:
					self.gui_state = self.PLACE_START
				elif self.gui_state == self.HOLD_END:
					self.gui_state = self.PLACE_END
		
		
		
		if self.gui_state == self.HOLD_START:
			screen.blit(self.startblock,(self.mousex , self.mousey ))
					
		if self.gui_state == self.HOLD_END:
			screen.blit(self.endblock,(self.mousex, self.mousey))
					
		if (self.startx != -1 and self.starty != -1) :
		
			screen.blit(self.startblock,
				(self.startx * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale, 
				self.starty * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale))
		
		if (self.endx != -1 and self.endy != -1) :
			
			screen.blit(self.endblock,
				(self.endx * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale,
				self.endy * (screen.get_width() / self.smallsurf.get_width())  * self.fixscale))
		
	def dot_not_on_wall(self, x, y) :
		xx = -1
		yy = -1
		x = int(x / self.fixscale)
		y = int(y / self.fixscale)
		if self.sa[int((y * self.guiwidth) + x) ] != self.mz.WALL : 
			xx = x 
			yy = y 
			self.gui_state = 0
		return (xx, yy)

	def show_maze(self, maze = [], width = 10, height = 10, symbols=True):
		
		if len(maze) != height * width:
			#
			print 'bad height * width'
		
		
		if True:	
			print
			for x in range (0,width + 2):
				if x < width + 1:
					print '#',
				else:
					print '#'

			for y in range (0 , height):
				print '#',
				for x in range (0, width):
					if symbols == True:
						if maze[ (y * width) + x] == self.mz.FREE :
							print ' ',
						elif maze[ (y * width) + x] == self.mz.START :
							print 'S',
						elif maze[ (y * width) + x] == self.mz.END :
							print 'X',
						elif maze[ (y * width) + x] == self.mz.WALL :
							print '#',
						elif maze[ (y * width) + x] == self.mz.PATH :
							print 'O',
						elif maze[ (y * width) + x] == self.mz.UNDEFINED :
							print 'U',
					else:
						print maze[ (y * width) + x] ,
				
				print '#',
				print

			for x in range (0,width + 2):
				print '#',
			print
			print
		


if __name__ == '__main__': 

	setup = ar.SU()
	
	matrixd = CL(setup)
	
	iface = Interface(setup)

	iface.choose_opts(matrixd)

	if setup.gui == True:
		while iface.quit == 0:
			iface.solve_png(matrixd)
	

	
	if setup.gui == False:
		matrixd.set_map(setup.maze, setup.width, setup.height)
		starttime = time.clock()	
		matrixd.load_kernel()
		matrixd.set_buffers()
		matrixd.execute()
		endtime = time.clock()
		
		matrixd.follow_path()
		
		a = matrixd.get_prev()
		b = matrixd.get_dist()
		iface.show_maze(a, matrixd.get_width(), matrixd.get_height(), False)
		print 'prev'
		
		iface.show_maze(b, matrixd.get_width(), matrixd.get_height(), False)
		print 'dist'
		print endtime - starttime, 'time on gpu'
	
	
	if matrixd.get_width() <= 40 :
		print 'last printout'
		iface.show_maze(matrixd.get_maze() , matrixd.get_width(), matrixd.get_height())
	
	if setup.gui == True and setup.output == True :
		f = open('outifle.txt','w')
		f.close()
		f = open('outifle.txt','a')
		f.write('#written by program\n')
		f.write(str(matrixd.get_width()) )
		f.write(',')
		f.write(str(matrixd.get_height()))
		f.write('\n')
		for i in setup.wallout :
			f.write(str(i)+",")
		f.write('\n')
		f.write('#start and end follow...\n')
		f.write(str(iface.mz.startx) + '\n')
		f.write(str(iface.mz.starty) + '\n')
		f.write(str(iface.mz.endx) + '\n')
		f.write(str(iface.mz.endy) + '\n')
		f.write('\n')
		f.close()
	

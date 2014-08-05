#!/usr/bin/env python

#import pyopencl as cl
import numpy
import time, math

import fileinput
from PIL import Image
import pygame as pg
#import pygame._view
import pygame.gfxdraw as pgd
import pygame

import sys

import array_setup as mz

class CL(object):


	def __init__(self):
		self.width = mz.width
		self.height = mz.height
		self.size = mz.width * mz.height
		self.prev = []
		self.maze = mz.maze
		self.found = []
		self.oo_ex = False
		
		

	def load_kernel(self):
		print 'load kernel' 
		
		
	def set_buffers(self):
		#
		#mf = cl.mem_flags

		startvisited = [mz.FREE] * self.size
		startdist = [mz.UNDEFINED] * self.size
		startprev = [mz.UNDEFINED] * self.size
		
		startvisited[(mz.starty * self.width) + mz.startx] = mz.VISITED 
		startdist[(mz.starty * self.width) + mz.startx] = 0
		self.maze[(mz.starty * self.width) + mz.startx] = mz.START 
		
		
		self.maze = numpy.array(self.maze, dtype=numpy.int32)
		self.visited = numpy.array((startvisited), dtype=numpy.int32)
		self.dist = numpy.array((startdist), dtype=numpy.uint32)
		self.prev = numpy.array((startprev), dtype=numpy.int32)
		self.mutex = numpy.array(([mz.FREE] * self.size), dtype=numpy.int32)
		
		prepdim = [0] * 3#self.size
		prepdim[0] = self.width
		prepdim[1] = self.height
		
		self.dimension = numpy.array((prepdim), dtype=numpy.int32)
			
		

	def execute(self):
	
		visited = numpy.empty_like(self.maze)
		dist = numpy.empty_like(self.maze)
		prev = numpy.empty_like(self.maze)
		dimension = numpy.empty_like(self.dimension)
		loop = 0
		j = 0
		
		#print self.maze.shape, 'shape'
		
		#for i in range(0,42): #self.size*5 ):
		while loop == 0 and j < self.size * 15:
			j += 1
			print j,
			#print 'here',
			
			
			
			#cl.enqueue_read_buffer(self.queue, self.dimension_buf, dimension).wait()        
			#print dimension[2],
			loop = dimension[2]
		
		'''

		self.prev = prev
		self.visited = visited
		self.dist = dist
		'''
	
	def must_check(self, test, direction):
	
		if mz.visited[direction] != mz.VISITED and mz.main[rank] != mz.WALL:
			if mz.dist[rank] + 1 <= mz.dist[test] :
				if mz.main[test] != mz.START  :
					mz.prev[test] = rank 
					mz.dist[test] = mz.dist[rank] + 1
	
	def find(self) :

		
	
		if flag == 0 and ii < mz.width * mz.height:
	
			#if rank == 0:
			#	print ii
		
		
			if mz.visited[mz.CENTER] == mz.FREE and mz.main[rank] != mz.WALL :
						
				if get_y(rank) == get_y(rank + 1) and rank + 1 < dim and near_visited() :
					must_check(rank + 1, mz.RIGHT)

				if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited() :
					must_check(rank - 1, mz.LEFT)

				if rank + mz.width < dim and near_visited() :
					must_check(rank + mz.width, mz.DOWN)

				if rank - mz.width >= 0 and near_visited() :
					must_check(rank - mz.width, mz.UP)

				if mz.main[rank] == mz.START :
					must_check(rank, mz.CENTER)
				

				if near_visited() :
					mz.visited[mz.CENTER] = mz.VISITED
	
	def near_visited(self) :
	
		if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
			if mz.visited[mz.RIGHT] == mz.VISITED:
				return True
		if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :
			if mz.visited[mz.LEFT] == mz.VISITED:
				return True
		if rank + mz.width < dim:
			if mz.visited[mz.DOWN] == mz.VISITED:
				return True
		if rank - mz.width >= 0:
			if mz.visited[mz.UP] == mz.VISITED:
				return True
		if rank == get_rank(mz.startx, mz.starty)  :
			return True
		return False
		
	def get_x(self,rank) :
		return rank - (mz.width * int(rank / mz.width))
	
	def get_y(self, rank) :
		return int(rank / mz.width)
	
	def get_rank(self, x,y) :
		return (y * mz.width) + x

	
	def follow_path(self) :
		
		dim = self.width * self.height
		if True: 
			if mz.gui == False:
				print self.prev, 'prev'
			i = 0 
			self.found = []
		
			found = self.prev[(mz.endy * self.width) + mz.endx]

			while (found != mz.UNDEFINED) and i < self.width * self.height :
				if found != mz.UNDEFINED:
					self.found.append(int(found))
				else :
					print int( found / width), found - (int(found / width) * width), 'y,x'
				found = self.prev[found]
				i += 1
			print self.found, 'found', len(self.found)
			
			i = 0
			while (i < dim) :
				if ( i in self.found) and self.maze[i] != mz.START:
					self.maze[i] = mz.PATH
					
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
			self.width = mz.width
		else:
			self.width = width
			mz.width = width
			
		if height == -1:
			self.height = mz.height
		else:
			self.height = height
			mz.width = width
		

class Interface(object) :

	def __init__(self):
		self.mapname = 'map.png'
		self.iconname = 'icon.png'
		self.map  =[]
		self.quit = 0	
		
	def solve_png(self , cl):
	
		if mz.gui == False:
			cl.set_map(mz.maze, mz.width, mz.height)
			return
	
		x = 0
		y = 0
		white = (64, 64, 64)
		w = 480
		h = 480
		self.startx = -1
		self.starty = -1
		self.endx = -1
		self.endy = -1
		
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
		self.boundtop = h - (self.box.get_height() - self.boxborder)
		self.boundbottom = h - self.boxborder
		self.boundgreenleft = w - (self.box.get_width() -  self.boxborder)
		self.boundgreenright = w - (self.box.get_width() -  self.boxborder) + 16
		self.boundredleft = w - (self.box.get_width() -  self.boxborder) + 16
		self.boundredright = w - (self.box.get_width() -  self.boxborder) + 32
		self.boundblueleft = w - (self.box.get_width() -  self.boxborder) + 32
		self.boundblueright = w - (self.box.get_width() -  self.boxborder) + 48
		blocksize = (w /cl.width) -2
		if blocksize <= 2 : blocksize = 4
		self.startblock = pg.Surface((blocksize,blocksize))
		self.startblock.fill(green)
		self.endblock = pg.Surface((blocksize,blocksize))
		self.endblock.fill(red)
		self.pathblock = pg.Surface((blocksize,blocksize))
		self.pathblock.fill(blue)
		self.blockoffset = 0#blocksize / 2 
		
		self.fixscale = ( float  ( w - (int ( w/ cl.width  ) * cl.width ))/cl.width *2 ) + 1
		#print self.fixscale, 'fixme'
		self.wallbox = pg.Surface( (math.ceil(w/cl.width), 
			math.ceil(h/cl.height )))
		self.wallbox.fill((0,0,0))
		
		
		## display first screen ##
		screensurf = surface
		screen = pg.display.set_mode((w, h))
		screen.fill((white))
		
		self.quit = 0
		running = 1
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
						if y + cl.height > screensurf.get_height() : 
							y = screensurf.get_height() - cl.height 
							
					if event.key == pg.K_LEFT:
						x -= 5
						if x < 0 : 
							x = 0
					if event.key == pg.K_RIGHT:
						x += 5
						if x + cl.width > screensurf.get_width() : 
							x = screensurf.get_width() - cl.width 			
			
			screensurf = surface.copy()
			pgd.rectangle(screensurf, ((x,y),(cl.width,cl.height)), (255,0,0))
			screen.blit(screensurf,(0,0))
			pg.display.flip()
			
		## display second screen ##
		screen.fill((white))
		self.smallsurf = pg.Surface((cl.width, cl.height))
		bwsurf = pg.Surface((cl.width, cl.height))
		self.smallsurf.blit(surface,(0,0),((x,y), (cl.width, cl.height)))
		
		
		pg.transform.threshold(bwsurf, self.smallsurf,
			(0,0,0,0),(20,20,20,0), (255,255,255,0), 1)	
		
		screensurf = pg.Surface((w,h))
		screensurf.fill((255,255,255))
		screen.fill((255,255,255))
		
		## convert to array representation ##
		sa = [0] * cl.width * cl.height
		pxarray = pygame.PixelArray(self.smallsurf)
		for yy in range (0, cl.width):
			for xx in range (0, cl.height):
				p =  pxarray[xx,yy]

				if p == 0 : p = mz.WALL
				else : p = 0
				sa[(yy * cl.width) + xx] = p
				if p == mz.WALL:
					mz.wallout.append((yy * cl.width) + xx)
					
					## print walls to screen ! ##
					#xxx = float(xx * ( self.fixscale)) 
					#yyy = float(yy * ( self.fixscale)) 
					screensurf.blit(self.wallbox, 
						(float(xx * float (w  / cl.width))   ,
						float(yy * float (h  / cl.height))   ))
		
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
			
			screen.fill((white))
			screen.blit(screensurf,(0,0))
			self.gui_controls(screen, event, w,h)
			pg.display.flip()
		
	
		
		mz.endx = self.endx
		mz.endy = self.endy
		
		mz.startx = self.startx
		mz.starty = self.starty
		
		if self.quit != 1:
			#print len(sa)
			sa[(self.starty * cl.width) + self.startx] = mz.START
			sa[(self.endy * cl.width) + self.endx] = mz.END
			cl.set_map(sa, cl.width, cl.height)
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
			
				#xxx = float(xx * ( self.fixscale)) #/ cl.width
				#yyy = float(yy * ( self.fixscale)) #/ cl.width
				screen.blit(self.pathblock,
					(float(xx * float(screen.get_width() / cl.width)) + self.blockoffset,
					float(yy * float(screen.get_width() / cl.width)) + self.blockoffset))
				screen.blit(self.startblock,
					(self.startx * (screen.get_width() / cl.width) + self.blockoffset, 
					self.starty * (screen.get_width() / cl.width) + self.blockoffset))
				screen.blit(self.endblock,
					(self.endx * (screen.get_width() / cl.width) + self.blockoffset,
					self.endy * (screen.get_width() / cl.width) + self.blockoffset))
			pg.display.flip()

	def gui_controls(self, screen, event,w,h):
		# this helper function puts controls on the screen
		screen.blit(self.box ,( w- (self.box.get_width()), 
			h - (self.box.get_height())) )
		# detect mouse
		self.mousex , self.mousey = pg.mouse.get_pos()
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
					if self.mousex < self.wallbox.get_width() * mz.width and \
							self.mousey < self.wallbox.get_height() * mz.height :
						self.startx = self.mousex / (screen.get_width() / self.smallsurf.get_width())
						self.starty = self.mousey / (screen.get_height()/ self.smallsurf.get_height())
						self.gui_state = 0
					
				elif self.gui_state == self.PLACE_END:
					if self.mousex < self.wallbox.get_width() * mz.width and \
							self.mousey < self.wallbox.get_height() * mz.height :
						self.endx = self.mousex / (screen.get_width() / self.smallsurf.get_width())
						self.endy = self.mousey / (screen.get_height()/ self.smallsurf.get_height())
						self.gui_state = 0
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
				(self.startx * (screen.get_width() / self.smallsurf.get_width()) + self.blockoffset, 
				self.starty * (screen.get_width() / self.smallsurf.get_width()) + self.blockoffset))
		
		if (self.endx != -1 and self.endy != -1) :
			
			screen.blit(self.endblock,
				(self.endx * (screen.get_width() / self.smallsurf.get_width()) + self.blockoffset,
				self.endy * (screen.get_width() / self.smallsurf.get_width()) + self.blockoffset))
		

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
						if maze[ (y * width) + x] == mz.FREE :
							print ' ',
						elif maze[ (y * width) + x] == mz.START :
							print 'S',
						elif maze[ (y * width) + x] == mz.END :
							print 'X',
						elif maze[ (y * width) + x] == mz.WALL :
							print '#',
						elif maze[ (y * width) + x] == mz.PATH :
							print 'O',
						elif maze[ (y * width) + x] == mz.UNDEFINED :
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

	matrixd = CL()
	
	i = Interface()

	if mz.gui == True:
		while i.quit == 0:
			i.solve_png(matrixd)
	

	
	if mz.gui == False:
		matrixd.set_map(mz.maze, mz.width, mz.height)	
		matrixd.load_kernel()
		matrixd.set_buffers()
		matrixd.execute()
		endtime = time.clock()
		
		matrixd.follow_path()
		
		a = matrixd.get_prev()
		b = matrixd.get_dist()
		i.show_maze(a, matrixd.get_width(), matrixd.get_height(), False)
		print 'prev'
		
		i.show_maze(b, matrixd.get_width(), matrixd.get_height(), False)
		print 'dist'
	
	
	
	if matrixd.get_width() <= 80 :
		print 'last printout'
		i.show_maze(matrixd.get_maze() , matrixd.get_width(), matrixd.get_height())
	
	if mz.gui == True and mz.output == True :
		f = open('outifle.txt','w')
		f.close()
		f = open('outifle.txt','a')
		f.write('#written by program\n')
		f.write(str(matrixd.get_width()) )
		f.write(',')
		f.write(str(matrixd.get_height()))
		f.write( '\n')
		for i in mz.wallout :
			f.write(str(i)+",")
		f.close()
	

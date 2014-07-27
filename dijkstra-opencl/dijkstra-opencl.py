#!/usr/bin/env python

import pyopencl as cl
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
		
		print cl.device_info.LOCAL_MEM_SIZE, 'local mem size'
		print cl.device_info.MAX_WORK_GROUP_SIZE, 'max work group size'
		print cl.device_info.QUEUE_PROPERTIES, 'queue properties'
		print cl.kernel_work_group_info.WORK_GROUP_SIZE, 'work group size'
		print cl.kernel_work_group_info.PREFERRED_WORK_GROUP_SIZE_MULTIPLE , 'preferred size'
		
		print mz.width * mz.height * 5 , 'calculated use'# 5 is num of full buffers!
		
		print 'estimated:' , int(math.sqrt(cl.device_info.MAX_WORK_GROUP_SIZE / 5))
		
		self.ctx = cl.create_some_context()
		self.queue = cl.CommandQueue(self.ctx,
			properties = 0)#cl.command_queue_properties.OUT_OF_ORDER_EXEC_MODE_ENABLE)


	def load_kernel(self):
		fstr = ''
		for line in fileinput.input('find.cl'):
			fstr += line

		self.program = cl.Program(self.ctx, fstr).build()

	def set_buffers(self):
		#
		mf = cl.mem_flags

	
		self.maze = numpy.array(self.maze, dtype=numpy.int32)
		self.visited = numpy.array(([mz.FREE] * self.size), dtype=numpy.int32)
		self.dist = numpy.array(([mz.UNDEFINED] * self.size), dtype=numpy.int32)
		self.prev = numpy.array(([mz.UNDEFINED] * self.size), dtype=numpy.int32)
		self.mutex = numpy.array(([mz.FREE] * self.size), dtype=numpy.int32)
		
		prepdim = [0] * 3#self.size
		prepdim[0] = self.width
		prepdim[1] = self.height
		
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
		dist = numpy.empty_like(self.maze)
		prev = numpy.empty_like(self.maze)
		dimension = numpy.empty_like(self.dimension)
		loop = 0
		
		for i in range(0,self.size):
		#while loop == 0:
			print 'here',
			self.program.find(self.queue, self.maze.shape,self.maze.shape, 
				self.maze_buf, 
				self.visited_buf, 
				self.dist_buf, 
				self.prev_buf, 
				self.mutex_buf,
				self.dimension_buf)
				
			
			cl.enqueue_read_buffer(self.queue, self.dimension_buf, dimension).wait()        
			print dimension[2],
			loop = dimension[2]
		
		'''
			at some point may remove 'wait' on visited_buf and dist_buf!!
		'''
		print 'loop end'
		cl.enqueue_read_buffer(self.queue, self.visited_buf, visited).wait()
		cl.enqueue_read_buffer(self.queue, self.dist_buf, dist).wait()
		cl.enqueue_read_buffer(self.queue, self.prev_buf, prev).wait()        

		self.prev = prev
		self.visited = visited
		self.dist = dist
		
	
	def follow_path(self) :
		
		dim = self.width * self.height
		if True: 

			#print self.prev, 'prev'
			i = 0 
			self.found = []
		
			found = self.prev[(mz.endy * self.width) + mz.endx]

			while (found != -1) and i < self.width * self.height :
				if found != -1:
					self.found.append(int(found))
				else :
					print int( found / width), found - (int(found / width) * width), 'y,x'
				found = self.prev[found]
				i += 1
			#print self.found, 'found', len(self.found)
			
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
			
		if height == -1:
			self.height = mz.height
		else:
			self.height = height
		
		

class Interface(object) :

	def __init__(self):
		self.mapname = 'map.png'
		self.map  =[]	
		
	def show_png(self , cl):
	
		if mz.gui == False:
			cl.set_map(mz.maze, mz.width, mz.height)
			return
	
		x = 0
		y = 0
		white = (64, 64, 64)
		w = 480
		h = 480
		
		surface = pg.image.load(self.mapname)
		#pgd.rectangle(surface, ((0,0),(cl.width,cl.height)), (255,0,0))
		#string = pg.image.tostring(surface, 'RGB')
		#print string

		print x,y, cl.width, cl.height
		#screensurf = pg.transform.scale(smallsurf, (w,h))
		screensurf = surface
		screen = pg.display.set_mode((w, h))
		screen.fill((white))
		
		quit = 0
		running = 1
		while running:

			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = 0
					quit = 1	
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
			
			
		screen.fill((white))
		smallsurf = pg.Surface((cl.width, cl.height))
		bwsurf = pg.Surface((cl.width, cl.height))
		smallsurf.blit(surface,(0,0),((x,y), (cl.width, cl.height)))
		
		
		pg.transform.threshold(bwsurf, smallsurf,(0,0,0,0),(0,0,0,0), (255,255,255,0), 1)	
		screensurf = pg.transform.scale(bwsurf, (w,h))
		
		running = 1
		while running == 1 and quit == 0:
			#screen.blit(screensurf,(0,0))
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = 0
					quit = 1	
			
			screen.fill((white))
			screen.blit(screensurf,(0,0))
			pg.display.flip()
		
		sa = [0] * cl.width * cl.height
		pxarray = pygame.PixelArray(smallsurf)
		for yy in range (0, cl.width):
			for xx in range (0, cl.height):
				p =  pxarray[xx,yy]
				if p == 0 : p = mz.WALL
				else : p = 0
				sa[(yy * cl.width) + xx] = p
		
		print sa, 'load info'
		self.show_maze(sa, cl.width, cl.height)
		
		cl.set_map(sa, cl.width, cl.height)


	def show_maze(self, maze = [], width = 10, height = 10):
		
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
		i.show_png(matrixd)
	
	starttime = time.clock()
	
	if mz.gui == False:
		matrixd.set_map(mz.maze, mz.width, mz.height)	
	#i.show_maze(mz.maze, mz.width, mz.height)
	
	matrixd.load_kernel()
	matrixd.set_buffers()
	matrixd.execute()
	matrixd.follow_path()
	a = matrixd.get_dist()
	#print a, 'get dist'
	endtime = time.clock()
	print  endtime - starttime 

	#i.show_maze(a , matrixd.get_width(), matrixd.get_height())
	i.show_maze(matrixd.get_maze() , matrixd.get_width(), matrixd.get_height())
	
	
	

#!/usr/bin/env python

import pyopencl as cl
import numpy
import time

import fileinput
from PIL import Image
import pygame as pg

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
		
		self.ctx = cl.create_some_context()
		self.queue = cl.CommandQueue(self.ctx)


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
		
		prepdim = [0] * self.size
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

	def execute(self):
	
		visited = numpy.empty_like(self.maze)
		dist = numpy.empty_like(self.maze)
		prev = numpy.empty_like(self.maze)
		dimension = numpy.empty_like(self.dimension)
		loop = 0
		
		#for i in range(0,self.size):
		while loop == 0:
			print 'here',
			self.program.find(self.queue, self.maze.shape, self.maze.shape, 
				self.maze_buf, 
				self.visited_buf, 
				self.dist_buf, 
				self.prev_buf, 
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
		#print prev
		#print mz.maze
	
	def follow_path(self) :
		
		dim = self.width * self.height
		if True: 

			print self.prev, 'prev'
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
			
		if height == -1:
			self.height = mz.height
		else:
			self.height = height
		
		

class Interface(object) :

	def __init__(self):
		self.mapname = 'map.png'
		self.map  =[]	
		
	def show_png(self , cl):
		surface = pg.image.load(self.mapname)
		string = pg.image.tostring(surface, 'RGB')
		#print string
	
		white = (64, 64, 64)
		w = 640
		h = 480
		screen = pg.display.set_mode((w, h))
		screen.fill((white))
		running = 1

		while running:
	
			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = 0
			screen.fill((white))
			screen.blit(surface,(0,0))
			pg.display.flip()
			
		print 'load info'
		cl.set_map(mz.maze, mz.width, mz.height)


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


	i.show_png(matrixd)
	
	starttime = time.clock()
	matrixd.set_map(mz.maze, mz.width, mz.height)	
	i.show_maze(mz.maze, mz.width, mz.height)
	
	matrixd.load_kernel()
	matrixd.set_buffers()
	matrixd.execute()
	matrixd.follow_path()
	a = matrixd.get_prev()
	print a, 'get maze'
	endtime = time.clock()
	print  endtime - starttime 

	i.show_maze(a , matrixd.get_width(), matrixd.get_height())
	i.show_maze(matrixd.get_maze() , matrixd.get_width(), matrixd.get_height())
	
	
	

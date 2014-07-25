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

	
		self.maze = numpy.array(mz.maze, dtype=numpy.float32)
		self.visited = numpy.array(([mz.FREE] * self.size), dtype=numpy.float32)
		self.dist = numpy.array(([mz.UNDEFINED] * self.size), dtype=numpy.float32)
		self.prev = numpy.array(([mz.UNDEFINED] * self.size), dtype=numpy.float32)

		self.dimension = numpy.array(([self.width, self.height]), dtype=numpy.float32)
			           
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
		self.program.find(self.queue, self.maze.shape, None, 
				self.maze_buf, self.visited_buf, self.dist_buf, self.prev_buf, 
				self.dimension_buf)
				
		visited = numpy.empty_like(self.maze)
		dist = numpy.empty_like(self.maze)
		prev = numpy.empty_like(self.maze)
		'''
			at some point may remove 'wait' on visited_buf and dist_buf!!
		'''
		cl.enqueue_read_buffer(self.queue, self.visited_buf, visited).wait()
		cl.enqueue_read_buffer(self.queue, self.dist_buf, dist).wait()
		cl.enqueue_read_buffer(self.queue, self.prev_buf, prev).wait()        
		
		self.prev = prev
		#print prev
		#print mz.maze
		
	def get_prev(self):
		return self.prev

	def get_width(self):
		return self.width
	
	def get_height(self):
		return self.height

class Interface(object) :

	def __init__(self):
		self.mapname = 'map.png'	
		
	def show_png(self):
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
					sys.exit()
			screen.fill((white))
			screen.blit(surface,(0,0))
			pg.display.flip()


	def show_maze(self, maze = [], width = 10, height = 10):
		
		if len(maze) != height * width:
			#
			print 'bad height * width'
		
		
		if True:	
			print
			for x in range (0,mz.width + 2):
				if x < mz.width + 1:
					print '#',
				else:
					print '#'

			for y in range (0 , mz.height):
				print '#',
				for x in range (0, mz.width):
				
					if maze[ (y * mz.width) + x] == mz.FREE :
						print ' ',
					elif maze[ (y * mz.width) + x] == mz.START :
						print 'S',
					elif maze[ (y * mz.width) + x] == mz.END :
						print 'X',
					elif maze[ (y * mz.width) + x] == mz.WALL :
						print '#',
					elif maze[ (y * mz.width) + x] == mz.PATH :
						print 'O',
					else:
						print maze[(y * mz.width) + x],
				
				print '#',
				print

			for x in range (0,mz.width + 2):
				print '#',
			print
			print
		


if __name__ == '__main__': 
	starttime = time.clock()
	matrixd = CL()
	matrixd.load_kernel()
	matrixd.set_buffers()
	matrixd.execute()
	a = matrixd.get_prev()
	print a
	endtime = time.clock()
	print  endtime - starttime 

	i = Interface()
	i.show_maze(mz.maze, mz.width, mz.height)
	i.show_maze(a , matrixd.get_width(), matrixd.get_height())
	i.show_png()
	
	
	

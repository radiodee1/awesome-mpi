#!/usr/bin/env python

import pyopencl as cl
import numpy
import time

import fileinput
from PIL import Image
import pygame as pg

#from OpenGL.GLUT import *
#from OpenGL.GLU import *
#from OpenGL.GL import *
import sys

import array_setup as mz

class CL(object):


    def __init__(self, width=10, height=10):
    	self.width = width
    	self.height = height
        self.size = width*height
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

	'''
	self.FREE = 0
	self.WALL = 1
	self.UNDEFINED = -1
	self.VISITED = 1
 	'''
 
    def load_program(self):
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
        

        
        cl.enqueue_read_buffer(self.queue, self.visited_buf, visited).wait()
        cl.enqueue_read_buffer(self.queue, self.dist_buf, dist).wait()
        cl.enqueue_read_buffer(self.queue, self.prev_buf, prev).wait()        
        #print ( "a", self.a)
        #print ( "b", self.b)
        print prev
        print mz.maze
 
def add(s=10) :
    starttime = time.clock()
    matrixd = CL(10,10)
    matrixd.load_program()
    matrixd.set_buffers()
    matrixd.execute()
    endtime = time.clock()
    print s, endtime - starttime 

def show_png():
	surface = pg.image.load('map.png')
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
		screen.blit(surface,(0,-10))
		pg.display.flip()


def show_maze():
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
				
				if mz.maze[ (y * mz.width) + x] == mz.FREE :
					print ' ',
				if mz.maze[ (y * mz.width) + x] == mz.START :
					print 'S',
				if mz.maze[ (y * mz.width) + x] == mz.END :
					print 'X',
				if mz.maze[ (y * mz.width) + x] == mz.WALL :
					print '#',
				if mz.maze[ (y * mz.width) + x] == mz.PATH :
					print 'O',
				
				
			print '#',
			print

		for x in range (0,mz.width + 2):
			print '#',
		print
		print
		


if __name__ == '__main__': 
	add()
	show_maze()
	show_png()
	
	
	

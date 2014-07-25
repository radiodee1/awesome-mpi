#!/usr/bin/env python

import pyopencl as cl
import numpy
import time

from PIL import Image
import pygame as pg

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys


class CL(object):


    def __init__(self, size=10):
        self.size = size
        self.ctx = cl.create_some_context()
        self.queue = cl.CommandQueue(self.ctx)

	self.FREE = 0
	self.WALL = 1
	self.UNDEFINED = -1
	self.VISITED = 1
 
    def load_program(self):
        fstr="""
        float add(float a, float b)
        {
            
 			return 2*(a + b);
            
        }
         __kernel void find(__global float* maze, __global float* visited, __global float* dist, __global float* prev)
        {
            unsigned int i = get_global_id(0);
 
           c[i] = add (a[i] , b[i]);
        }
         """
        self.program = cl.Program(self.ctx, fstr).build()
 
    def popCorn(self):
    	#
        mf = cl.mem_flags
 
        self.a = numpy.array(range(self.size), dtype=numpy.float32)
        self.b = numpy.array(range(self.size), dtype=numpy.float32)
        
        self.maze = numpy.array([self.FREE] * self.size, dtype=numpy.float32)
        self.visited = numpy.array(([self.FREE] * self.size), dtype=numpy.float32)
        self.dist = numpy.array(([self.UNDEFINED] * self.size), dtype=numpy.float32)
        self.prev = numpy.array(([self.UNDEFINED] * self.size), dtype=numpy.float32)
 
        self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                               hostbuf=self.a)
                               
        self.maze_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR,
                               hostbuf=self.maze)   
                                                   
        self.b_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                               hostbuf=self.b)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.b.nbytes)
        
        self.visited_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
        						hostbuf=self.visited)
        self.dist_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
        						hostbuf=self.dist)
        self.prev_buf = cl.Buffer(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, 
        						hostbuf=self.prev)
        
 
    def execute(self):
        self.program.find(self.queue, self.a.shape, None, 
        		self.maze_buf, self.visited_buf, self.dist_buf, self.prev_buf)
        visited = numpy.empty_like(self.a)
        dist = numpy.empty_like(self.a)
        prev = numpy.empty_like(self.a)
        
        #cl.enqueue_read_buffer(self.queue, self.dest_buf, c).wait()
        
        cl.enqueue_read_buffer(self.queue, self.visited_buf, visited).wait()
        cl.enqueue_read_buffer(self.queue, self.dist_buf, dist).wait()
        cl.enqueue_read_buffer(self.queue, self.prev_buf, prev).wait()        
        #print ( "a", self.a)
        #print ( "b", self.b)
        print ( "c", c )
 
def add(s=10) :
    starttime = time.clock()
    matrixmul = CL(s)
    matrixmul.load_program()
    matrixmul.popCorn()
    matrixmul.execute()
    endtime = time.clock()
    print s, endtime - starttime 

def show():
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


if __name__ == '__main__': 
	add()
	show()

	
	#glwindow = GL()
	
	#glwindow.main()
	
	

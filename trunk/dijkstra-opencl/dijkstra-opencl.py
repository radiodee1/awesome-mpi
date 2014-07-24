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
 
    def load_program(self):
        fstr="""
        float add(float a, float b)
        {
            
 			return 2*(a + b);
            
        }
         __kernel void part1(__global float* a, __global float* b, __global float* c)
        {
            unsigned int i = get_global_id(0);
 
           c[i] = add (a[i] , b[i]);
        }
         """
        self.program = cl.Program(self.ctx, fstr).build()
 
    def popCorn(self):
        mf = cl.mem_flags
 
        self.a = numpy.array(range(self.size), dtype=numpy.float32)
        self.b = numpy.array(range(self.size), dtype=numpy.float32)
 
        self.a_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                               hostbuf=self.a)
        self.b_buf = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                               hostbuf=self.b)
        self.dest_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, self.b.nbytes)
 
    def execute(self):
        self.program.part1(self.queue, self.a.shape, None, self.a_buf, self.b_buf, self.dest_buf)
        c = numpy.empty_like(self.a)
        cl.enqueue_read_buffer(self.queue, self.dest_buf, c).wait()
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
	f = pg.image.load('map.png')
	
	white = (255, 64, 64)
	w = 640
	h = 480
	screen = pg.display.set_mode((w, h))
	screen.fill((white))
	running = 1

	while running:
		screen.fill((white))
		screen.blit(f,(0,0))
		pg.display.flip()


if __name__ == '__main__': 
	add()
	show()

	
	#glwindow = GL()
	
	#glwindow.main()
	
	

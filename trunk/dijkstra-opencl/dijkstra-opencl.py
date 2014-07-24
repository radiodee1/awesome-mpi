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


class GL(object) :
	def __init__(self, size=10):
		self.name = 'dijkstra'
		self.sometexture = None
		self.maintexture = None

	def main(self):
		self.sometexture = self.png_to_tex('map.png')
		self.maintexture = glGenTextures(1)
		
		glutInit(sys.argv)
		glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
		glutInitWindowSize(400,400)
		glutCreateWindow(self.name)

		glClearColor(0.,0.,0.,1.)
		glShadeModel(GL_SMOOTH)
		glEnable(GL_CULL_FACE)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_LIGHTING)
		lightZeroPosition = [10.,4.,10.,1.]
		lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
		glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
		glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
		glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
		glEnable(GL_LIGHT0)
		glutDisplayFunc(self.display)
		glMatrixMode(GL_PROJECTION)
		gluPerspective(40.,1.,1.,40.)
		glMatrixMode(GL_MODELVIEW)
		gluLookAt(0,0,10,
				  0,0,0,
				  0,1,0)
		glPushMatrix()
		glutMainLoop()

		return

	def display(self):
	
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		color = [1.0,0.,0.,1.]
		glMaterialfv(GL_FRONT,GL_DIFFUSE,color)

		glBegin(GL_QUADS);
		#counter clock wise
		glVertex3f(-0.5,0.5,0.0);
		glVertex3f(-0.5,-0.5,0.0);
		glVertex3f(0.5,-0.5,0.0);
		glVertex3f(0.5,0.5,0.0);

		glEnd();
		glPopMatrix()
		
		glLoadIdentity()
		glOrtho(0,1,0,1,-1,1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		#glViewport(0, 0, self.width, self.height)
		
		glEnable(GL_TEXTURE_2D)
		
		glBindTexture(GL_TEXTURE_2D, (self.sometexture))		
		
		Varray = numpy.array([[0,0],[0,256],[224,256],[224,0]],numpy.uint16)
		glVertexPointer(2,GL_SHORT,0,Varray)
		indices = [0,1,2,3]
		glDrawElements(GL_QUADS,1,GL_UNSIGNED_SHORT,indices)

		#glutSwapBuffers() 
		#glPopMatrix()
		#glBindTexture(GL_TEXTURE_2D, texture)
		#glFlush();
		#glPopMatrix()
		self.show_text("hello")
		glutSwapBuffers()
		return

	def resize(self, width, height):
		self.width = width
		self.height = height
		glutPostRedisplay()
	

	def png_to_tex( self,filename):
		img = Image.open(filename)
		img_data = numpy.array(list(img.getdata()), numpy.uint8)

		texture = glGenTextures(1)
		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glBindTexture(GL_TEXTURE_2D, texture)

		# Texture parameters are part of the texture object, so you need to 
		# specify them only once for a given texture object.
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, 
			GL_RGB, GL_UNSIGNED_BYTE, img_data)
		return texture

	 
	def loadImage(self):
		image = Image.open("map.png")

		ix = image.size[0]
		iy = image.size[1]
		#image = image.tostring("raw", "RGBX", 0, -1)

		img_data = numpy.array(list(image.getdata()), numpy.uint8)


		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

	def show_text(self,text) :
		glWindowPos2i(10, 120);
		glColor4f(0.0, 0.0, 1.0, 1.0);
		glutBitmapString(GLUT_BITMAP_HELVETICA_18, text);

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
	
	

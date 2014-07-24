#!/usr/bin/env python

import pyopencl as cl
import numpy
import time

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys

name = 'dijkstra'

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(400,400)
    glutCreateWindow(name)

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
    glutDisplayFunc(display)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    glPushMatrix()
    glutMainLoop()

    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0,0.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    #glutSolidSphere(2,20,20)
    #glutSolidCube(2,20,20)
    glBegin(GL_QUADS);
    #counter clock wise
    glVertex3f(-0.5,0.5,0.0);
    glVertex3f(-0.5,-0.5,0.0);
    glVertex3f(0.5,-0.5,0.0);
    glVertex3f(0.5,0.5,0.0);
    #glVertex3f(0.5,-0.5,0.0);
    #glVertex3f(-0.5,-0.5,0.0);
    glEnd();
    
    glFlush();
    glPopMatrix()
    show_text("hello")
    glutSwapBuffers()
    return

def show_text(text) :
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

if __name__ == '__main__': 
	add()
	main()
	

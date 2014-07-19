#!/usr/bin/python

from mpi4py import MPI
import array_setup as mp
#import numpy
#import math
#import sys
import node

com = MPI.COMM_WORLD
rank = com.Get_rank()
dim = com.Get_size()

if (dim != mp.height * mp.width and rank == 0) :
	print 'size must be', mp.height*mp.width,', (' ,mp.width, 'x',mp.height, ')!!'
#if dim != mp.height * mp.width :
#	sys.exit()
	
node.find();

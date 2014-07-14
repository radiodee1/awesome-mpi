#!/usr/bin/env python

from mpi4py import MPI
import array_setup as mp
import numpy
import math
import sys
import node

com = MPI.COMM_WORLD
rank = com.Get_rank()
dim = com.Get_size()

if (dim != 100 and rank == 0) :
	print "size must be 10x10, or 100!!"
if dim != 100 :
	sys.exit()
	
node.find();

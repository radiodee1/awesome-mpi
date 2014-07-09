#!/usr/bin/env python

#import arrays_return_mpi as rmpi
#import arrays_add_mpi as mpi
import arrays_cpu as cpu
import arrays_opencl as ocl

if True:
	print "arrays_opencl"
	ocl.add(100)
	ocl.add(1000)
	ocl.add(10000)
	ocl.add(100000)
	ocl.add(1000000)
	
if True:
	print "arrays_cpu"
	cpu.add(100)
	cpu.add(1000)
	cpu.add(10000)
	cpu.add(100000)
	cpu.add(1000000)
	

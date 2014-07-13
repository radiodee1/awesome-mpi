#!/usr/bin/env python

#import arrays_return_mpi as rmpi
#import arrays_add_mpi as mpi
import arrays_cpu as cpu
#import arrays_opencl as ocl

if False:
	print "arrays_opencl"
	#ocl.add(50)
	#ocl.add(500)
	#ocl.add(5000)
	#ocl.add(50000)
	#ocl.add(500000)
	
if True:
	print "arrays_cpu"
	cpu.add(50)
	cpu.add(500)
	cpu.add(5000)
	cpu.add(50000)
	cpu.add(500000)
	

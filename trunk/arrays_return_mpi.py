#!/usr/bin/env python

from mpi4py import MPI
import numpy
import math


com = MPI.COMM_WORLD
rank = com.Get_rank()
end = com.Get_size()



def add(size=10):
	starttime = MPI.Wtime()
	
	data = numpy.empty(shape=(size*3), dtype=numpy.int32)

	#print data, 'bcast'
	for i in range(size):
		data[i] = int(i )
		data[size + i] = int(i )
		data[(size * 2) + i] = int(0)

	com.bcast(data, root=0)
	
	k = int (math.ceil(size/float(end - 1)))
	
	# on cores...
	if rank != 0 :
		#for i in range(0, size, 1) :
		for i in range( (rank - 1) * k, (rank ) * k , 1) :
			if (i >= (rank - 1) * k ) and (i  < (rank ) * k) \
					and i >=0 and i < size : #
				data[(size * 2) + i] = data[i] + data[size + i]	
				com.send(data[(size * 2) + i], dest=0, tag=i)
	
	if rank == 0 :
		for i in range(0, size, 1) :
			src = int(math.ceil(i  /( k ))) + 1 # - 1 
			#
			dat = 0
			dat = com.recv(source=src, tag=i)
			data[(size * 2) + i] = dat
			#
			
		#print data
		endtime = MPI.Wtime()
		print size,  endtime - starttime
	

#add(5)
#add(6)
#add(7)
#add(8)
#add(9)
#add(10)

if True :
	print "arrays_return_mpi"
	add(50)
	add(500)
	add(5000)
	add(50000)
	add(500000)


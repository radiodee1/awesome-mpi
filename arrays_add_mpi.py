#!/usr/bin/env python

from mpi4py import MPI
import numpy
import math

com = MPI.COMM_WORLD
rank = com.Get_rank()
end = com.Get_size()



def add(size=10):
	starttime = MPI.Wtime()
	
	data = numpy.zeros(shape=(size*3), dtype=numpy.float64)

	#print data, 'bcast'
	for i in range(size):
		data[i] = int(i )
		data[size + i] = int(i )
		data[(size * 2) + i] = int(0)

	com.bcast(data, root=0)
	

		
	# on cores...
	if rank != 0 :
	
		k = int (math.ceil(size/float(end - 1)))
	
		for i in range(0, size, 1) :

			if (i >= (rank - 1) * k ) and (i  < (rank ) * k) : #k  +(( end)*(rank )) ) +(end ) :
				data[(size * 2) + i] = data[i] + data[size + i]	
				#com.Send(data[(size * 2) + i], dest=0, tag=i)
				#print data[(size * 2) + i], "node", rank
	
	if rank == 0 :
		endtime = MPI.Wtime()
		print size, endtime - starttime
	


if True:
	print "arrays_add_mpi"
	add(50)
	add(500)
	add(5000)
	add(50000)
	add(500000)

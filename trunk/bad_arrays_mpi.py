#!/usr/bin/env python

from mpi4py import MPI
import numpy
import math

com = MPI.COMM_WORLD
rank = com.Get_rank()
end = com.Get_size()



def add(size=10):

	
	data = numpy.zeros(shape=(size*3), dtype=numpy.float64)
	#data = numpy.arange(int (size * 3), dtype=numpy.float64)
	#print data, 'base'
	for i in range(size):
		data[i] = int(i )
		data[size + i] = int(i )
		data[(size * 2) + i] = int(0)

	com.bcast(data, root=0)
	

		
	# on cores...
	if rank != 0 :
	
		k = int (math.ceil(size/float(end - 1)))

		if False:# k != size/(end-1) :
			k += 1 
	
		print "test", rank, k, end -1, (size/float(end -1))
	
		for m in range(0  , k + ( end ) + (end -1)  , 1 ) : #
			i = m + ((end  )* (rank  -1)) 
			if (i >= 0 ) and (i  <= k  +(( end)*(rank )) ) +(end ) :
				data[(size * 2) + i] = data[i] + data[size + i]	
				#com.Send(data[(size * 2) + i], dest=0, tag=i)

			elif i < 0 :
				print "rank zero"
			else  :
				print "size"
		print data, "nodes", rank

	# only for root
	if rank == 0:
		k = int(size/(end -1))
		if k == 0:
			k = 1
		for m in range(0, k + end - 1 , 1):
			for j in range(0, end , 1):
				i = m * k + j
				if  (j != 0 ) and (i * (end -1 ) <= size ) :
					data[(size * 2) + i] = com.recv(source=j, tag=m)
					print data[(size * 2) + i], "root"
	
	#com.Disconnect()
	
add(21)

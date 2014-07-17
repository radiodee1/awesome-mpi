#!/usr/bin/python

from mpi4py import MPI
import array_setup as mp
import numpy
import math
import sys
import array

com = MPI.COMM_WORLD
rank = com.Get_rank()
dim = com.Get_size()



def find() :

	#print str(rank) +' ',
	flag = 0
	localflag = 0
	ii = 0
	
	while flag == 0 :#or ii < 10 :
	#if True:
		#visited = com.alltoall(mp.visited)
		#mp.visited[rank] = visited
		print "ii",ii

		mp.visited = com.allgather(mp.visited[rank])

		#com.Barrier()
		print "reduce", mp.visited, "rank", rank
		
		if mp.visited[rank] == mp.FREE and \
				(mp.main[rank] != mp.WALL or mp.main[rank] == mp.START ): 
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim and near_visited() :
				set_must_check(rank + 1)
			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited() :
				set_must_check(rank - 1)
			if rank + 10 < dim and near_visited() :
				set_must_check(rank + 10) 
			if rank - 10 >= 0 and near_visited() :
				set_must_check(rank - 10)
			if near_visited() and mp.visited[rank] == 0:
				mp.visited[rank] = mp.VISITED
				#mp.visited = com.allgather(mp.visited[rank])
			#print 'here (didn\'t fire check)'
		
		#fix_prev()
		mp.prev = com.allgather(mp.prev[rank])#, op=MPI.MAX)
		print mp.prev, "---"
		#com.barrier()
		ii += 1
		
			
		if mp.visited[rank] == mp.VISITED and mp.main[rank] == mp.END :
			localflag = 1
			print "end found!!" , rank
		else:
			localflag = 0
			print 'not yet', rank
			
		flag = com.allreduce(localflag, op=MPI.MAX)
		if (rank == 0) :
			print "end flag" , flag
		print 'after flag reduce' 
		#com.Barrier()
		#dist = numpy.array(mp.dist, dtype=numpy.long)
		#mp.dist = com.Bcast([dist, MPI.INT], root=rank)

	
	#print path backwards.
	#com.barrier()
	#mp.prev = com.allgather(mp.prev[rank])
	#print mp.prev, rank
	#found =com.reduce( mp.prev[(mp.endy * 10) + mp.endx], op=MPI.MAX)
	found = mp.prev[(mp.endy * 10) + mp.endx]
	print "start of chain", found
	if (rank == 0) or True:
		i = 0
		print "at start"
		found = mp.prev[(mp.endy * 10) + mp.endx]
		if found == rank:
			print rank,"found start", found
			while (found != 0) and i < 100 :
				found = mp.prev[found]
				#found = com.allreduce(mp.prev[found], op=MPI.MAX);
				i += 1
				print found," really found ",
	
	
def near_visited() :
	
	if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
		if mp.visited[rank + 1] == mp.VISITED:
			#mp.visited[rank] = mp.VISITED
			return True
	if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :
		if mp.visited[rank - 1] == mp.VISITED:
			#mp.visited[rank] = mp.VISITED
			return True
	if rank + 10 < dim:
		if mp.visited[rank + 10] == mp.VISITED:
			#mp.visited[rank] = mp.VISITED
			return True
	if rank - 10 >= 0:
		if mp.visited[rank -10] == mp.VISITED:
			#mp.visited[rank] = mp.VISITED			
			return True
	if rank == get_rank(mp.startx, mp.starty) :
		return True
	return False
		

	
def set_must_check(test):	
	mp.prev[rank] = test
	#prev = com.allgather(mp.prev)
	print mp.prev
	#mp.prev[test] = com.bcast(rank, root=rank)
	print "set prev" , rank
	return 0		
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x

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
	
	while (flag == 0) :
	#if True:
		#visited = com.alltoall(mp.visited)
		#mp.visited[rank] = visited
		
		mp.visited = com.allgather(mp.visited[rank] )
		#visited = com.allreduce(mp.visited[rank], op=MPI.MAX)
		print "reduce", mp.visited
		
		if mp.visited[rank] == mp.FREE and \
				(mp.main[rank] != mp.WALL or mp.main[rank] == mp.START ): 
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim and near_visited() :
				check(rank + 1)
			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited() :
				check(rank - 1)
			if rank + 10 < dim and near_visited() :
				check(rank + 10) 
			if rank - 10 >= 0 and near_visited() :
				check(rank - 10)
			#mp.visited[rank] = mp.VISITED
			print 'here (didn\'t fire check)'
			
		if mp.visited[rank] == mp.VISITED and mp.main[rank] == mp.END :
			localflag = 1
			print "end found!!" , rank
		else:
			localflag = 0
			print 'not yet'
			
		flag = com.reduce(localflag, op=MPI.SUM)
		if (rank == 0) :
			print "end flag" , flag
		print 'after flag reduce'
		#dist = numpy.array(mp.dist, dtype=numpy.long)
		#mp.dist = com.Bcast([dist, MPI.INT], root=rank)

	'''		
	#print path backwards.
	#com.barrier()
	if (rank == 0):# or True:
		i = 0
		found =com.allreduce( mp.prev[(mp.endy * 10) + mp.endx], op=MPI.MAX)
		print rank,"found start", found, 'test', test
		while (found != 0) and i < 100 :
			#found = mp.prev[found]
			found = com.allreduce(mp.prev[found], op=MPI.MAX);
			i += 1
			print found," ",
	'''
	
def near_visited() :
	
	if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
		if mp.visited[rank + 1] == mp.VISITED:
			mp.visited[rank] = mp.VISITED
			return True
	if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :
		if mp.visited[rank - 1] == mp.VISITED:
			mp.visited[rank] = mp.VISITED
			return True
	if rank + 10 < dim:
		if mp.visited[rank + 10] == mp.VISITED:
			mp.visited[rank] = mp.VISITED
			return True
	if rank - 10 >= 0:
		if mp.visited[rank -10] == mp.VISITED:
			mp.visited[rank] = mp.VISITED			
			return True
	if rank == get_rank(mp.startx, mp.starty) :
		return True
	return False
		
def check(test) :
	#all distances are '1' !!

	if True:
		
		print 'here 2'
		#com.barrier()
		dist = com.allreduce(mp.dist[test], op=MPI.MAX)
		print "rank",rank,"dist", dist	,'test',test	
		#if mp.dist[test] >= mp.dist[rank] + 1 :
		if dist >= mp.dist[rank] + 1:
			print "save value", rank
			mp.dist[test] = mp.dist[rank] + 1
			mp.prev[test] = rank
			
			#mp.willreceive[test] += 1;
			
			print "test here"
			
			
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x

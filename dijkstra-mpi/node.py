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
		
		mp.visited = com.allgather(mp.visited[rank] )
		#mp.dist = com.allgather(mp.dist[rank] )
		#mp.prev = com.allgather(mp.prev[rank] )
		#print "visited", mp.visited
		#mp.visited = mp.visited
		print mp.visited
		
		if mp.visited[rank] == mp.FREE and \
				(mp.main[rank] != mp.WALL or mp.main[rank] == mp.START ) \
				and near_visited() :
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
				check(rank + 1)
			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :
				check(rank - 1)
			if rank + 10 < dim :
				check(rank + 10) 
			if rank - 10 >= 0 :
				check(rank - 10)
			mp.visited[rank] = mp.VISITED
			
		if mp.visited[rank] == mp.VISITED and mp.main[rank] == mp.END :
			localflag = 1
			print "end found!!" , rank
		else:
			localflag = 0
			
		flag = com.reduce(localflag, op=MPI.MAX)
		if (rank == 0) :
			print "end flag" , flag
			
		#com.barrier()
		dist = numpy.array(mp.dist, dtype=numpy.long)
		#for i in range( 0, dim):
			#dist_buf = dist #numpy.asarray(mp.dist, numpy.int)
		mp.dist = com.Bcast([dist, MPI.INT], root=rank)
		#mp.dist = com.bcast(mp.dist, root=rank)		
			
	#print path backwards.
	#com.barrier()
	if (rank == 0):# or True:
		i = 0
		found =com.reduce( mp.prev[(mp.endy * 10) + mp.endx], op=MPI.MAX)
		print rank,"found start", found, 'test', test
		while (found != 0) and i < 100 :
			found = mp.prev[found]
			#found = com.reduce(mp.prev[found], op=MPI.MAX);
			i += 1
			print found," ",
	
	
def near_visited() :
	if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
		if mp.visited[rank + 1] == mp.VISITED:
			return True
	if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :
		if mp.visited[rank - 1] == mp.VISITED:
			return True
	if rank + 10 < dim:
		if mp.visited[rank + 10] == mp.VISITED:
			return True
	if rank - 10 >= 0:
		if mp.visited[rank -10] == mp.VISITED:
			return True
	if rank == get_rank(mp.startx, mp.starty) :
		return True
	return False
		
def check(test) :
	#all distances are '1' !!
	#test is unvisited node!!
	#if mp.visited[test] != mp.VISITED :
	if True:
		#dist = mp.dist
		#if rank != 0 :
		#	dist = com.gather(mp.dist[test], root=rank)

		#dist = mp.dist[test] #com.reduce(mp.dist[test], op=MPI.MIN)
		print "rank",rank,"dist", mp.dist[test]	,'test',test	
		if mp.dist[test] >= mp.dist[rank] + 1 :#or mp.main[test] == mp.END:
			print "save value", rank
			mp.dist[test] = mp.dist[rank] + 1
			mp.prev[test] = rank
			
			#mp.willreceive[test] += 1;
			
			print "test here"
			#mp.dist = com.bcast(mp.dist, root=rank)#, op=MPI.MAX)
			#com.send(mp.dist[test], dest=test, tag=test)
			#mp.dist[test] = com.recv(source=rank, tag=test)			
			#com.send(mp.prev[test], dest=test, tag=test+ 100)
			#mp.prev[test] = com.recv(source=rank, tag=test+100)
			
			
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x

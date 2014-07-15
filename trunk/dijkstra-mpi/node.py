#!/usr/bin/env python

from mpi4py import MPI
import array_setup as mp
import numpy
import math
import sys

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
		
		#print "visited", mp.visited
		#mp.visited = mp.visited
		
		if mp.visited[rank] == mp.FREE and \
				(mp.main[rank] != mp.WALL or mp.main[rank] == mp.START ) \
				and near_visited() :
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :#and near_visited():
				check(rank + 1)
			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :#and near_visited():
				check(rank - 1)
				#mp.dist = com.allgather(mp.dist[rank + 1])
			if rank + 10 < dim :#and near_visited() :
				check(rank + 10) 
			if rank - 10 >= 0 : #and near_visited() :
				check(rank - 10)
			mp.visited[rank] = mp.VISITED
			
		if mp.visited[rank] == mp.VISITED and mp.main[rank] == mp.END :
			localflag = 1
			print "end found!!" , rank
		else:
			localflag = 0
			
		flag = com.allreduce(localflag, op=MPI.MAX)
		if (rank == 0) :
			print "end flag" , flag
			
	#print path backwards.
	if (rank == 0):
		i = 0
		found = mp.prev[(mp.endy * 10) + mp.endx]
		print rank,"found start", found
		while (found != 0) and i < 100 :
			found = mp.prev[found]
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
	if mp.visited[test] != mp.VISITED :# and rank == 0:
		print "dist", mp.dist[test]
		if mp.dist[test] >= mp.dist[rank] + 1 :#or mp.main[test] == mp.END:
			print "save value", rank
			mp.dist[test] = mp.dist[rank] + 1
			mp.prev[test] = rank
			
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

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

	flag = 0
	localflag = 0
	ii = 0
	directions = []
	while flag == 0 and ii < 20:
	#if True:
		print ii
		
		mp.visited = com.allgather(mp.visited[rank])
		mp.prev = com.allgather(mp.prev[rank])
		mp.dist = com.allgather(mp.dist[rank])

		
		if mp.visited[rank] == mp.FREE and \
				(mp.main[rank] != mp.WALL or mp.main[rank] == mp.START ): 
			if mp.main[rank] == mp.START :
				set_must_check(rank)
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim and near_visited() :
				set_must_check(rank + 1)

			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited() :
				set_must_check(rank - 1)

			if rank + 10 < dim and near_visited() :
				set_must_check(rank + 10)

			if rank - 10 >= 0 and near_visited() :
				set_must_check(rank - 10)

			#if near_visited() and mp.visited[rank] == 0:
			#	mp.visited[rank] = mp.VISITED
			
		## send and recv of 4 dist and prev
		if get_y(rank) == get_y(rank + 1) and rank + 1 < 100 :
			com.send(mp.prev[rank+1], dest=rank+1, tag=rank+1)
		
		if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0:
			mp.prev[rank] = com.recv(source=rank-1, tag=rank)
			
		if get_y(rank) == get_y(rank - 1) and rank -1 >= 0 :
			com.send(mp.prev[rank-1], dest=rank-1, tag=rank-1)
			
		if get_y(rank) == get_y(rank + 1) and rank + 1 < 100 :
			mp.prev[rank] = com.recv(source=rank+1, tag=rank)
		
		if rank + 10 < 100 :
			com.send(mp.prev[rank+10], dest=rank+10, tag=rank+10)
			
		if rank - 10 >= 0 :
			mp.prev[rank] = com.recv(source=rank-10, tag=rank)
		
		if rank - 10 >= 0 :
			com.send(mp.prev[rank-10], dest=rank-10, tag=rank-10)
			
		if rank + 10 < 100:
			mp.prev[rank] = com.recv(source=rank+10, tag=rank)

		
		## send and recv of 4 dist and prev
		if get_y(rank) == get_y(rank + 1) and rank + 1 < 100 :
			com.send(mp.dist[rank+1], dest=rank+1, tag=rank+1 + dim)
		
		if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0:
			mp.dist[rank] = com.recv(source=rank-1, tag=rank + dim)
			
		if get_y(rank) == get_y(rank - 1) and rank -1 >= 0 :
			com.send(mp.dist[rank-1], dest=rank-1, tag=rank-1 + dim)
			
		if get_y(rank) == get_y(rank + 1) and rank + 1 < 100 :
			mp.dist[rank] = com.recv(source=rank+1, tag=rank + dim)
		
		if rank + 10 < 100 :
			com.send(mp.dist[rank+10], dest=rank+10, tag=rank+10 + dim)
			
		if rank - 10 >= 0 :
			mp.dist[rank] = com.recv(source=rank-10, tag=rank + dim)
		
		if rank - 10 >= 0 :
			com.send(mp.dist[rank-10], dest=rank-10, tag=rank-10 + dim)
			
		if rank + 10 < 100:
			mp.dist[rank] = com.recv(source=rank+10, tag=rank + dim)
		
		'''
		#fix_prev()
		mp.prev = com.allgather(mp.prev[rank])
		mp.dist = com.allgather(mp.dist[rank])
		'''
	
		#com.barrier()
		ii += 1
		
			
		if mp.visited[rank] == mp.VISITED and mp.main[rank] == mp.END :
			localflag = 1
			#print "end found!!" , rank
		else:
			localflag = 0
			#print 'not yet', rank
			
		flag = com.allreduce(localflag, op=MPI.MAX)
		#if (rank == 0) :
		#	print "end flag" , flag
		
	
	#print path backwards.
	
	found = mp.prev[(mp.endy * 10) + mp.endx]
	if (rank == 0) or True:
		i = 0
		found = mp.prev[(mp.endy * 10) + mp.endx]
		if rank == 0 : #found == rank or True:
			print rank,"found start", found,
			while (found != 0) and i < 100 :
				found = mp.prev[found]
				i += 1
				print "and ",found," really found ",
			print mp.prev, 'prev'
			print mp.dist, 'dist'
			print mp.visited, 'visited'
			print mp.main, 'main'
	
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
		
		
def set_must_check(test):
	
	if mp.visited[test] != mp.VISITED and mp.main[rank] != mp.WALL:
		print 'before', mp.dist[rank] , rank
		if mp.dist[rank] + 1 <= mp.dist[test] :
			print 'change', mp.dist[rank] + 1, mp.dist[test]
			mp.prev[test] = rank #fr
			mp.dist[test] = mp.dist[rank] + 1
	mp.visited[rank] = mp.VISITED
	return 0		
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x

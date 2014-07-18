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


directions = []

def find() :

	flag = 0
	localflag = 0
	ii = 0
	directions = []
	while flag == 0 :
	#if True:
		print ii
		mp.visited = com.allgather(mp.visited[rank])

		if mp.visited[rank] == mp.FREE and \
				(mp.main[rank] != mp.WALL or mp.main[rank] == mp.START ): 
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim and near_visited() :
				set_must_check(rank + 1, rank)
				#directions.append(rank + 1)
			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited() :
				set_must_check(rank - 1, rank)
				#directions.append(rank - 1)
			if rank + 10 < dim and near_visited() :
				set_must_check(rank + 10, rank)
				#directions.append(rank + 10) 
			if rank - 10 >= 0 and near_visited() :
				set_must_check(rank - 10, rank)
				#directions.append(rank - 10)
			if near_visited() and mp.visited[rank] == 0:
				mp.visited[rank] = mp.VISITED
				
				'''
				print directions
				if len(directions) != 0:
					mp.prev[rank] = min(directions) #test
				directions = []
				'''
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
		
		
		#fix_prev()
		mp.prev = com.allgather(mp.prev[rank])
		mp.dist = com.allgather(mp.dist[rank])

		#mp.prev = com.allgather(mp.prev[0])
		#mp.dist = com.allgather(mp.dist[0])
		
		
		
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
			print mp.prev
	
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
		
		
def set_must_check(test, fr):
	#directions.append(test)
	if  mp.main[test] != mp.WALL:
		if mp.dist[fr] + 1 < mp.dist[test] :
			mp.prev[test] = fr
			mp.dist[test] = mp.dist[fr] + 1
			#mp.tocheck[test].append( test)
	return 0		
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x

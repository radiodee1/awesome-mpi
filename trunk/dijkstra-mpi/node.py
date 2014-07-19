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

	show_maze()
	mp.starttime = MPI.Wtime()
	
	flag = 0
	localflag = 0
	ii = 0
	directions = []
	while flag == 0 and ii < 100:
	
		#if rank == 0:
		#	print ii
		
		mp.visited = com.allgather(mp.visited[rank])
		
		
		if mp.visited[rank] == mp.FREE and mp.main[rank] != mp.WALL : 
			if mp.main[rank] == mp.START :
				must_check(rank)
			
			if get_y(rank) == get_y(rank + 1) and rank + 1 < dim and near_visited() :
				must_check(rank + 1)

			if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited() :
				must_check(rank - 1)

			if rank + 10 < dim and near_visited() :
				must_check(rank + 10)

			if rank - 10 >= 0 and near_visited() :
				must_check(rank - 10)

			if near_visited() :
				mp.visited[rank] = mp.VISITED
			
		## send and recv of 4 dist and prev ##
		prev = 0
		if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
			com.send(mp.prev[rank+1], dest=rank+1, tag=rank+1)
	
		if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0:
			prev = com.recv(source=rank-1, tag=rank)
			directions.append(prev)
		
		if get_y(rank) == get_y(rank - 1) and rank -1 >= 0 :
			com.send(mp.prev[rank-1], dest=rank-1, tag=rank-1)
			
		if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
			prev = com.recv(source=rank+1, tag=rank)
			directions.append(prev)		
		
		if rank + 10 < dim :
			com.send(mp.prev[rank+10], dest=rank+10, tag=rank+10)
			
		if rank - 10 >= 0 :
			prev = com.recv(source=rank-10, tag=rank)
			directions.append(prev)		
		
		if rank - 10 >= 0 :
			com.send(mp.prev[rank-10], dest=rank-10, tag=rank-10)
			
		if rank + 10 < dim:
			prev = com.recv(source=rank+10, tag=rank)
			directions.append(prev)
		
		if mp.main[rank] != mp.START:	
			mp.prev[rank] = max(directions)
		else :
			mp.prev[rank] = -1
		dist = 0 
		
		## send and recv of 4 dist and prev ##
		if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
			com.send(mp.dist[rank+1], dest=rank+1, tag=rank+1 + dim)
		
		if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0:
			dist = com.recv(source=rank-1, tag=rank + dim)
			if dist != mp.UNDEFINED :
				mp.dist[rank] = dist
			
		if get_y(rank) == get_y(rank - 1) and rank -1 >= 0 :
			com.send(mp.dist[rank-1], dest=rank-1, tag=rank-1 + dim)
			
		if get_y(rank) == get_y(rank + 1) and rank + 1 < dim :
			dist = com.recv(source=rank+1, tag=rank + dim)
			if dist != mp.UNDEFINED :
				mp.dist[rank] = dist
		
		if rank + 10 < dim :
			com.send(mp.dist[rank+10], dest=rank+10, tag=rank+10 + dim)
			
		if rank - 10 >= 0 :
			dist = com.recv(source=rank-10, tag=rank + dim)
			if dist != mp.UNDEFINED :
				mp.dist[rank] = dist
		
		if rank - 10 >= 0 :
			com.send(mp.dist[rank-10], dest=rank-10, tag=rank-10 + dim)
			
		if rank + 10 < dim:
			dist = com.recv(source=rank+10, tag=rank + dim)
			if dist != mp.UNDEFINED :
				mp.dist[rank] = dist
		
		
		#fix_prev()
		mp.prev = com.allgather(mp.prev[rank])
		mp.dist = com.allgather(mp.dist[rank])
		
		ii += 1
		
			
		if mp.visited[rank] == mp.VISITED and mp.main[rank] == mp.END :
			localflag = 1
		else:
			localflag = 0	
		flag = com.allreduce(localflag, op=MPI.MAX)
		
	follow_path()
	show_maze()
	if rank == 0:
		mp.endtime = MPI.Wtime()
		print mp.endtime - mp.starttime
	return 
	#end of 'find'
	
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
		
		
def must_check(test):
	
	if mp.visited[test] != mp.VISITED and mp.main[rank] != mp.WALL:
		if mp.dist[rank] + 1 <= mp.dist[test] :
			if mp.main[test] != mp.START:
				mp.prev[test] = rank 
			mp.dist[test] = mp.dist[rank] + 1
					
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x
	
	
def follow_path() :

	if rank == 0 :
		i = 0 
		mp.found = []
		
		found = mp.prev[(mp.endy * 10) + mp.endx]
		
		mp.found.append(found)			
		while (found != -1) and i < 100 :
			if found != -1:
				mp.found.append(found)
			found = mp.prev[found]
			i += 1

		i = 0
		while (i < dim) :
			if ( i in mp.found) and mp.main[i] != mp.START:
				mp.main[i] = mp.PATH
			i += 1
		
def show_maze():
	if rank == 0:	
		print
		for x in range (0,10 + 2):
			if x < 10 + 1:
				print '#',
			else:
				print '#'

		for y in range (0 , 10):
			print '#',
			for x in range (0, 10):
				if mp.main[ (y * 10) + x] == mp.FREE :
					print ' ',
				if mp.main[ (y * 10) + x] == mp.START :
					print 'S',
				if mp.main[ (y * 10) + x] == mp.END :
					print 'X',
				if mp.main[ (y * 10) + x] == mp.WALL :
					print '#',
				if mp.main[ (y * 10) + x] == mp.PATH :
					print 'O',
			print '#',
			print

		for x in range (0,10 + 2):
			print '#',
		print
		print

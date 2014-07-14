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
	print str(rank) +' ',
	
	rankx = get_x(rank)
	ranky = get_y(rank)
	
	if mp.main[rank] == mp.END and mp.visited[rank] == mp.VISITED :
		#check()
		print 'end found'
		sys.exit()
	if mp.visited[rank] == mp.FREE and mp.main[rank] != mp.WALL :
		if get_y(rank) == get_y(rank + 1) and rank + 1 < 100 and near_visited():
			check(rank + 1)
		if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 and near_visited():
			check(rank - 1)
		if rank + 10 < 100 and near_visited() :
			check(rank + 10) 
		if rank - 10 >= 0 and near_visited() :
			check(rank - 10)
	
def near_visited() :
	if get_y(rank) == get_y(rank + 1) and rank + 1 < 100 :
		if mp.visited[rank + 1] == mp.VISITED:
			return True
	if get_y(rank) == get_y(rank - 1) and rank - 1 >= 0 :
		if mp.visited[rank - 1] == mp.VISITED:
			return True
	if rank + 10 < 100:
		if mp.visited[rank + 10] == mp.VISITED:
			return True
	if rank - 10 >= 0:
		if mp.visited[rank -10] == mp.VISITED:
			return True
	return False
		
def check(test) :
	#do stuff here
	mp.visited[rank] = mp.VISITED
	
	
def get_x(rank) :
	return rank - (10 * int(rank / 10))
	
def get_y(rank) :
	return int(rank / 10)
	
def get_rank(x,y) :
	return (y * 10) + x

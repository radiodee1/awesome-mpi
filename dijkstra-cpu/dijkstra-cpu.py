#!/usr/bin/env python

import numpy
import time, math
#import fileinput
import pygame as pg
import pygame.gfxdraw as pgd
import pygame
import sys

import setup as ar

class CPU(object):


	def __init__(self, array):
		self.mz = array
	
		self.width = self.mz.width
		self.height = self.mz.height
		self.size = self.mz.width * self.mz.height

		self.maze = self.mz.maze
		self.found = []
		self.oo_ex = False
		
		self.visited = [0] * self.size
		self.dist = self.mz.dist 
		self.prev = self.mz.prev 

	
	def execute(self):
		## control loop for each node !! ##
		j = 0
		self.found = 0
		
		while self.found == 0 and j < self.size * 15:
			j += 1
			
			for i in range (0, self.size):
				self.find(i)	
		
	
	def must_check(self, test, rank):
		## part of each node !! ##
		if self.visited[rank] != self.mz.VISITED and self.maze[rank] != self.mz.WALL:
			if self.dist[rank] + 1 <= self.dist[test] or self.dist[test] == self.mz.UNDEFINED :
				if self.maze[test] != self.mz.START  :
					self.prev[test] = rank 
					self.dist[test] = self.dist[rank] + 1
	
	def find(self, rank ) :
		## central part of node !! ##
		flag = 0;
	
		if flag == 0 and rank < self.width * self.height:
	
			if self.visited[rank] == self.mz.FREE and self.maze[rank] != self.mz.WALL :
						
				if self.get_y(rank) == self.get_y(rank + 1) and \
						rank+1 < self.size and self.near_visited(rank) :
					self.must_check(rank + 1, rank)

				if self.get_y(rank) == self.get_y(rank - 1) and \
						rank - 1 >= 0 and self.near_visited(rank) :
					self.must_check(rank - 1, rank)

				if rank + self.width < self.size and self.near_visited(rank) :
					self.must_check(rank + self.width, rank)

				if rank - self.width >= 0 and self.near_visited(rank) :
					self.must_check(rank - self.width, rank)

				if self.maze[rank] == self.mz.START :
					self.must_check(rank, rank)
				

				if self.near_visited(rank) :
					self.visited[rank] = self.mz.VISITED
					
				if self.maze[rank] == self.mz.END and self.visited[rank] == self.mz.VISITED:
					self.found = 1
				
				
	
	def near_visited(self, rank) :
		## part of each node !! ##
		if self.get_y(rank) == self.get_y(rank + 1) and rank + 1 < self.size :
			if self.visited[rank + 1] == self.mz.VISITED:
				return True
		if self.get_y(rank) == self.get_y(rank - 1) and rank - 1 >= 0 :
			if self.visited[rank - 1] == self.mz.VISITED:
				return True
		if rank + self.width < self.size:
			if self.visited[rank + self.width] == self.mz.VISITED:
				return True
		if rank - self.width >= 0:
			if self.visited[rank - self.width] == self.mz.VISITED:
				return True
		if rank == self.get_rank(self.mz.startx, self.mz.starty)  :
			return True
		return False
		
	def get_x(self,rank) :
		## node helper ##
		return rank - (self.width * int(rank / self.width))
	
	def get_y(self, rank) :
		## node helpre ##
		return int(rank / self.width)
	
	def get_rank(self, x,y) :
		## node helper ##
		return (y * self.width) + x

	
	def follow_path(self) :
		## call this after end is found!! ##
		dim = self.size 
		if True: 
			if self.mz.gui == False:
				print self.prev, 'prev'
			i = 0 
			self.found = []
		
			found = self.prev[(self.mz.endy * self.width) + self.mz.endx]

			while (found != self.mz.UNDEFINED) and i < self.width * self.height :
				if found != self.mz.UNDEFINED:
					self.found.append(int(found))
				else :
					print int( found / width), found - (int(found / width) * width), 'y,x'
				found = self.prev[found]
				i += 1
			print self.found, 'found', len(self.found)
			
			i = 0
			while (i < dim) :
				if ( i in self.found) and self.maze[i] != self.mz.START:
					self.maze[i] = self.mz.PATH
					
				i += 1	
		
	def get_prev(self):
		## class helper ##
		return self.prev

	def get_visited(self):
		## class helper ##
		return self.visited

	def get_dist(self):
		## class helper ##
		return self.dist

	def get_width(self):
		## class helper ##
		return self.width
	
	def get_height(self):
		## class helper ##
		return self.height
		
	def get_maze(self):
		## class helper ##
		return self.maze	
			
	def set_dist_start(self, x, y):
		## class helper, use before 'execute' ##
		self.dist[(y * self.width) + x] = 0
	
	def set_map(self, maze, width=-1, height=-1):
		## class helper ##
		self.maze = maze
		self.mz.maze = maze
		if width == -1:
			self.width = self.mz.width
		else:
			self.width = width
			self.mz.width = width
			
		if height == -1:
			self.height = self.mz.height
		else:
			self.height = height
			self.mz.height = height
		

class Interface(object) :

	def __init__(self, array):
		self.mz = array
		self.mapname = 'map.png'
		self.iconname = 'icon.png'
		self.map  = []
		self.quit = 0	
		
	def solve_png(self , cpu):
	
		if self.mz.gui == False:
			cpu.set_map(self.mz.maze, self.mz.width, self.mz.height)
			return
	
		x = 0
		y = 0
		white = (64, 64, 64)
		w = 480
		h = 480
		self.startx = -1
		self.starty = -1
		self.endx = -1
		self.endy = -1
		
		self.guiwidth = cpu.width
		self.guiheight = cpu.height
		
		surface = pg.image.load(self.mapname)
		icon = pg.image.load(self.iconname)

		pg.display.set_icon(icon)
		
		## initialize control components ##
		gray = (16,16,16)
		red =(255,0,0)
		green = (0,255,0)
		blue = (0,0,255)
		self.boxborder = 5
		self.boxwidth = 48
		self.boxheight = 16
		self.box = pg.Surface((self.boxwidth + (self.boxborder * 2), 
			self.boxheight + (self.boxborder * 2)))
		self.box.fill(gray)
		boxred = pg.Surface((16,16))
		boxred.fill(red)
		boxgreen = pg.Surface((16,16))
		boxgreen.fill(green)
		boxblue = pg.Surface((16,16))
		boxblue.fill(blue)
		self.box.blit(boxgreen, (0 + self.boxborder,0 + self.boxborder))
		self.box.blit(boxred, (16 + self.boxborder,0 + self.boxborder))
		self.box.blit(boxblue, (32 + self.boxborder, 0 + self.boxborder))
		self.mousex = 0
		self.mousey = 0
		self.boundtop = h - (self.box.get_height() - self.boxborder)
		self.boundbottom = h - self.boxborder
		self.boundgreenleft = w - (self.box.get_width() -  self.boxborder)
		self.boundgreenright = w - (self.box.get_width() -  self.boxborder) + 16
		self.boundredleft = w - (self.box.get_width() -  self.boxborder) + 16
		self.boundredright = w - (self.box.get_width() -  self.boxborder) + 32
		self.boundblueleft = w - (self.box.get_width() -  self.boxborder) + 32
		self.boundblueright = w - (self.box.get_width() -  self.boxborder) + 48
		blocksize = (w /cpu.width) -2
		if blocksize <= 2 : blocksize = 4
		self.startblock = pg.Surface((blocksize,blocksize))
		self.startblock.fill(green)
		self.endblock = pg.Surface((blocksize,blocksize))
		self.endblock.fill(red)
		self.pathblock = pg.Surface((blocksize,blocksize))
		self.pathblock.fill(blue)
		self.blockoffset = 0#blocksize / 2 
		
		## fixscale not used ##
		self.fixscale = ( float  ( w - (int ( w/ cpu.width  ) * cpu.width ))/w ) + 1
		
		## all walls ##
		self.wallbox = pg.Surface( (math.ceil((w/cpu.width)* self.fixscale), 
			math.ceil((h/cpu.height) * self.fixscale )))
		self.wallbox.fill((0,0,0))
		
		
		## display first screen ##
		screensurf = surface
		screen = pg.display.set_mode((w, h))
		pg.display.set_caption('dijkstra-cpu', 'dijkstra-cpu')
		screen.fill((white))
		
		self.quit = 0
		running = 1
		while running:

			for event in pg.event.get():
				if event.type == pg.QUIT:
					running = 0
					self.quit = 1	
				if event.type == pg.KEYUP:
					if event.key == pg.K_RETURN:
						running = 0
					if event.key == pg.K_UP:
						y -= 5
						if y < 0 : 
							y = 0
					if event.key == pg.K_DOWN:
						y += 5
						if y + cpu.height > screen.get_height() : 
							y = screen.get_height() - cpu.height 
							
					if event.key == pg.K_LEFT:
						x -= 5
						if x < 0 : 
							x = 0
					if event.key == pg.K_RIGHT:
						x += 5
						if x + cpu.width > screen.get_width() : 
							x = screen.get_width() - cpu.width 			
			
			screensurf = surface.copy()
			screen.fill(white)
			screen.blit(screensurf,(0,0))
			pgd.rectangle(screen, ((x,y),(cpu.width,cpu.height)), (255,0,0))
			pg.display.flip()
			
		## display second screen ##
		screen.fill((white))
		self.smallsurf = pg.Surface((cpu.width, cpu.height))
		bwsurf = pg.Surface((cpu.width, cpu.height))
		self.smallsurf.blit(surface,(0,0),((x,y), (cpu.width, cpu.height)))
		
		
		pg.transform.threshold(bwsurf, self.smallsurf,
			(0,0,0,0),(20,20,20,0), (255,255,255,0), 1)	
		
		screensurf = pg.Surface((w,h))
		screensurf.fill((255,255,255))
		screen.fill((255,255,255))
		
		## convert to array representation ##
		self.sa = [0] * cpu.width * cpu.height
		pxarray = pygame.PixelArray(self.smallsurf)
		for yy in range (0, cpu.width):
			for xx in range (0, cpu.height):
				p =  pxarray[xx,yy]

				if p == 0 : p = self.mz.WALL
				else : p = 0
				self.sa[(yy * cpu.width) + xx] = p
				if p == self.mz.WALL:
					self.mz.wallout.append((yy * cpu.width) + xx)
					
					## print walls to screen ! ##
					xxx = float(xx * ( self.fixscale)) 
					yyy = float(yy * ( self.fixscale)) 
					screensurf.blit(self.wallbox, 
						(float(xxx * float (w  / cpu.width))   ,
						float(yyy * float (h  / cpu.height))   ))
		
		self.gui_state = 0
		
		self.PLACE_START = 1
		self.PLACE_END = 2
		self.FIND_PATH = 3
		self.HOLD_START = 4
		self.HOLD_END = 5
		
		self.running = 1
		while self.running == 1 and self.quit == 0:
			
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = 0
					self.quit = 1	
			
			screen.fill((white))
			screen.blit(screensurf,(0,0))
			self.gui_controls(screen, event, w,h)
			pg.display.flip()
		
	
		
		self.mz.endx = self.endx
		self.mz.endy = self.endy
		
		self.mz.startx = self.startx
		self.mz.starty = self.starty
		
		if self.quit != 1:
			## run cpu calculation ##
			self.sa[(self.starty * cpu.width) + self.startx] = self.mz.START
			self.sa[(self.endy * cpu.width) + self.endx] = self.mz.END
			
			cpu.set_dist_start(self.startx, self.starty)
			
			cpu.set_map(self.sa, cpu.width, cpu.height)
			starttime = time.clock()
			
			cpu.execute()
			endtime = time.clock()
			print  endtime - starttime , 'time on cpu'
			cpu.follow_path()
		
		## print screen with solution ##
		self.running = 1
		while self.running == 1 and self.quit == 0:
			
			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = 0
					self.quit = 1	
			
				if event.type == pg.KEYUP:
					if event.key == pg.K_RETURN:
						self.running = 0
			
				if event.type == pg.MOUSEBUTTONDOWN:
			
					left , middle, right = pg.mouse.get_pressed() 
					if left == True:
						self.running = 0
			
			screen.fill((white))
			screen.blit(screensurf,(0,0))
			for i in cpu.found :
				xx = i - ( cpu.get_width() * (int(i / cpu.get_width() )))
				yy = int(i / cpu.get_width())
			
				xxx = float(xx * ( self.fixscale)) 
				yyy = float(yy * ( self.fixscale)) 
				
				screen.blit(self.pathblock,
					(float(xxx * float(screen.get_width() / cpu.width)) + self.blockoffset,
					float(yyy * float(screen.get_width() / cpu.width)) + self.blockoffset))
				screen.blit(self.startblock,
					(self.startx * (screen.get_width() / cpu.width) * self.fixscale, 
					self.starty * (screen.get_width() / cpu.width) * self.fixscale))
				screen.blit(self.endblock,
					(self.endx * (screen.get_width() / cpu.width) * self.fixscale,
					self.endy * (screen.get_width() / cpu.width) * self.fixscale))
			pg.display.flip()

	def gui_controls(self, screen, event,w,h):
		# this helper function puts controls on the screen
		screen.blit(self.box ,( w- (self.box.get_width()), 
			h - (self.box.get_height())) )
		# detect mouse
		self.mousex , self.mousey = pg.mouse.get_pos()
		self.mousex = self.mousex - (self.wallbox.get_width() / 2)
		self.mousey = self.mousey - (self.wallbox.get_height() / 2)
		if event.type == pg.MOUSEBUTTONDOWN:
			#print 'here mouse'
			left , middle, right = pg.mouse.get_pressed() 
			if left == True:
				
				if self.mousey > self.boundtop \
						and self.mousey < self.boundbottom :
					if self.mousex > self.boundredleft and self.mousex < self.boundredright:
						self.gui_state = self.HOLD_END
						self.endx = -1
						self.endy = -1
					if self.mousex > self.boundgreenleft and self.mousex < self.boundgreenright:
						self.gui_state = self.HOLD_START
						self.startx = -1
						self.starty = -1
					if self.mousex > self.boundblueleft and self.mousex < self.boundblueright:
						self.running = 0
						self.gui_state = self.FIND_PATH

				elif self.gui_state == self.PLACE_START:
					if self.mousex < self.wallbox.get_width() * self.mz.width and \
							self.mousey < self.wallbox.get_height() * self.mz.height :
						self.startx = self.mousex / (screen.get_width() / self.smallsurf.get_width())
						self.starty = self.mousey / (screen.get_height()/ self.smallsurf.get_height())
						#self.gui_state = 0
						self.startx, self.starty = self.dot_not_on_wall(self.startx, self.starty)
					
				elif self.gui_state == self.PLACE_END:
					if self.mousex < self.wallbox.get_width() * self.mz.width and \
							self.mousey < self.wallbox.get_height() * self.mz.height :
						self.endx = self.mousex / (screen.get_width() / self.smallsurf.get_width())
						self.endy = self.mousey / (screen.get_height()/ self.smallsurf.get_height())
						#self.gui_state = 0
						self.endx, self.endy = self.dot_not_on_wall(self.endx, self.endy)
						
				elif self.gui_state == self.HOLD_START:
					self.gui_state = self.PLACE_START
				elif self.gui_state == self.HOLD_END:
					self.gui_state = self.PLACE_END
		
		
		
		if self.gui_state == self.HOLD_START:
			screen.blit(self.startblock,(self.mousex , self.mousey ))
					
		if self.gui_state == self.HOLD_END:
			screen.blit(self.endblock,(self.mousex, self.mousey))
					
		if (self.startx != -1 and self.starty != -1) :
		
			screen.blit(self.startblock,
				(self.startx * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale, 
				self.starty * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale))
		
		if (self.endx != -1 and self.endy != -1) :
			
			screen.blit(self.endblock,
				(self.endx * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale,
				self.endy * (screen.get_width() / self.smallsurf.get_width()) * self.fixscale))
		
	def dot_not_on_wall(self, x, y) :
		xx = -1
		yy = -1
		x = int(x / self.fixscale)
		y = int(y / self.fixscale)
		if self.sa[(y * self.guiwidth) + x ] != self.mz.WALL : 
			xx = x
			yy = y  
			self.gui_state = 0
		return (xx,yy)

	def show_maze(self, maze = [], width = 10, height = 10, symbols=True):
		
		if len(maze) != height * width:
			#
			print 'bad height * width'
		
		
		if True:	
			print
			for x in range (0,width + 2):
				if x < width + 1:
					print '#',
				else:
					print '#'

			for y in range (0 , height):
				print '#',
				for x in range (0, width):
					if symbols == True:
						if maze[ (y * width) + x] == self.mz.FREE :
							print ' ',
						elif maze[ (y * width) + x] == self.mz.START :
							print 'S',
						elif maze[ (y * width) + x] == self.mz.END :
							print 'X',
						elif maze[ (y * width) + x] == self.mz.WALL :
							print '#',
						elif maze[ (y * width) + x] == self.mz.PATH :
							print 'O',
						elif maze[ (y * width) + x] == self.mz.UNDEFINED :
							print 'U',
					else:
						print maze[ (y * width) + x] ,
				
				print '#',
				print

			for x in range (0,width + 2):
				print '#',
			print
			print
		


if __name__ == '__main__': 

	setup = ar.SU()

	matrixd = CPU(setup)
	
	i = Interface(setup)

	if setup.gui == True:
		while i.quit == 0:
			i.solve_png(matrixd)
	

	
	if setup.gui == False:
		matrixd.set_map(setup.maze, setup.width, setup.height)	
		#matrixd.load_kernel()
		#matrixd.set_buffers()
		starttime = time.clock()
		matrixd.execute()
		endtime = time.clock()
		
		matrixd.follow_path()
		
		a = matrixd.get_prev()
		b = matrixd.get_dist()
		i.show_maze(a, matrixd.get_width(), matrixd.get_height(), False)
		print 'prev'
		
		i.show_maze(b, matrixd.get_width(), matrixd.get_height(), False)
		print 'dist'
		print endtime - starttime, 'time on cpu'
	
	if matrixd.get_width() <= 30 :
		print 'last printout'
		i.show_maze(matrixd.get_maze() , matrixd.get_width(), matrixd.get_height())
	
	if setup.gui == True and setup.output == True :
		f = open('outifle.txt','w')
		f.close()
		f = open('outifle.txt','a')
		f.write('#written by program\n')
		f.write(str(matrixd.get_width()) )
		f.write(',')
		f.write(str(matrixd.get_height()))
		f.write( '\n')
		for i in setup.wallout :
			f.write(str(i)+",")
		f.close()
	

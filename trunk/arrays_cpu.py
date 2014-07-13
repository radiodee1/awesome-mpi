#!/usr/bin/env python

import time

def add(size=10):

    starttime = time.clock()
	
    a = tuple([float(i) for i in range(size)])
    b = tuple([float(j) for j in range(size)])
    c = [None for i in range(size)]
    for i in range(size):
        c[i] = a[i]+b[i]
 
    #print "a", a
    #print "b", b
    #print "c", c[:1000]
    endtime = time.clock()
    print size, endtime - starttime
 
#add(50)
#add(500)
#add(5000)

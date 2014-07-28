		#pragma OPENCL EXTENSION cl_khr_int64_base_atomics : enable
		
		#define LOCKME 999
		
		#define LOCK(a) atom_cmpxchg(a, 0, 999)
		#define UNLOCK(a) atom_xchg(a, 0)
		
		#define FREE  0
    	#define OPEN  1
    	#define WALL  2
    	#define START  3
    	#define END  4
    	#define PATH  5

		#define VISITED  1
		#define UNDEFINED  -1
		
		#define FALSE 0
		#define TRUE 1
		
		int get_x(int width,  int ii) {
 			return ii - (width * (ii / width));   
        }
        
        int get_y(int width, int ii) {
        	return (int)( ii / width);
        }
        int get_index(int width, int x, int y) {
        	return (y * width) + x;
        }
        
        int near_visited( 
        			int ii,  
        			__global int* maze, 
        			__global int* visited, 
        			int width, 
        			int height) {
        			

            int dim = width * height;
            
            if  (maze[ii] == START  ){
				//return TRUE;
			}
            
			if ( (ii + 1 < dim ) && get_y(width,ii) == get_y(width,ii + 1)   ) {
				//if (dist[ii+1] != UNDEFINED ) return TRUE;
				if  ( visited[ii+1] !=   FREE && maze[ii+1] != WALL ){
					return TRUE;
				}
			}
			if( (ii >= 1 ) && get_y(width, ii) == get_y(width, ii - 1)   )  {
				//if (dist[ii-1] != UNDEFINED ) return TRUE;
				if  ( visited[ii - 1] !=   FREE && maze[ii-1] != WALL){
					return TRUE;
				}
			}
			if  (ii +   width < dim) {
				//if (dist[ii+width] != UNDEFINED ) return TRUE;
				if   (visited[ii + width] !=   FREE && maze[ii+ width] != WALL  ) {
					return TRUE;
				}
			}
			if  (ii >= width ) {
				//if (dist[ii-width] != UNDEFINED ) return TRUE;
				if   (visited[ii - width] !=  FREE && maze[ii-width] != WALL  ) {
					return TRUE;
				}
			}
			
			return FALSE;
            
            
        	
        }
        void must_check(
        		int ii,
        		__global int* maze, 
         		__global int* visited, 
         		__global int* dist, 
         		__global int* prev,
         		__global int* mutex,
        		int  test) {
        		
            //ii = get_global_id(0);
        	int alt = 0;
        
        	if   ((visited[test] !=   VISITED ) && visited[ii] != VISITED
        			&& maze[test] != WALL && maze[ii] != WALL) {
        			
        		alt = dist[ii] + 1;
        		if (dist[ii] == UNDEFINED ) alt = 0;
        		
				if  (  dist[test] == UNDEFINED   ) {
					//if   (maze[test] !=   START || (maze[ii] == START && test != ii)) {
					
						while(LOCK(&mutex[test]) != LOCKME);// spin
				  		prev[test] = ii; 
				  		//atom_xchg(&prev[test], ii);
				  		
				  		dist[test] = alt;
				  		//atom_add(&dist[test], alt);
				  		UNLOCK(&mutex[test]);
				  	//}
				  	
				  	
				  	//dist[test] =  alt;// dist[ii] + 1;
				}
			}
	
            //barrier(CLK_LOCAL_MEM_FENCE);
        
        }
        
         __kernel void find(
         		__global int* maze, 
         		__global int* visited, 
         		__global int* dist, 
         		__global int* prev,
         		__global int* mutex,
         		__global int* dimension)
         		
        {
        	
			
            unsigned int ii = get_global_id(0);
            
 			unsigned int width = dimension[0];
 			unsigned int height = dimension[1];
 			unsigned int dim = width * height;
 			
 			unsigned int flag = 0;
 			unsigned int localflag = 0;
 			unsigned int i = 0;

			if (visited[ii] == VISITED && maze[ii] == END ){
           		flag = 1;
           		localflag = 1;
           		dimension[2] = 1;
           		//return;
           }
			else if (maze[ii] == START && visited[ii] != VISITED) {
           		while(LOCK(&mutex[ii]) != LOCKME);// spin
           		visited[ii] = VISITED;
           		dist[ii] = 0;
           		prev[ii] = UNDEFINED;
           		UNLOCK(&mutex[ii]);
           }
           else {
       		//while (flag == 0 && i < dim) {
       		//if (flag == 0) {
       		
       			i ++;
		   		if ((visited[ii] ==  FREE &&  maze[ii] !=  WALL) ) {

					//while(LOCK(&mutex[ii]) != LOCKME);// spin

					if ( (ii + 1 < dim) && get_y(width,ii) == get_y(width,ii + 1)  
						&& near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex,ii + 1);
					}

					if ( (ii >=1) && get_y(width,  ii) == get_y(width,  ii - 1)  
						&& near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex, ii - 1);
					}

					if ( ii +  width < dim  && near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex, ii +  width);
					}

					if (( ii >=  width)   && near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex, ii -  width);
					}

					if  ( maze[ii] ==  START) {
						//dist[ii] = 0;
						//atom_xchg(&visited[ii], VISITED);
						//must_check(ii,maze, visited, dist, prev, mutex, ii);						
					}

					if (near_visited(ii, maze, visited, width, height)) {
						// visited[ii] =  VISITED;
						atom_xchg(&visited[ii], VISITED);
					}
					
					//UNLOCK(&mutex[ii]);
				}
       		}
       		
           barrier(CLK_LOCAL_MEM_FENCE);
           
           
           
			//	
			
           
        }

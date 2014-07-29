		#pragma OPENCL EXTENSION cl_khr_int64_base_atomics : enable
		#pragma OPENCL EXTENSION cl_khr_global_int32_base_atomics : enable
		#pragma OPENCL EXTENSION cl_khr_local_int32_base_atomics : enable
		
		#define LOCKME 999
		
		
		//atom_cmpxchg(a, 0, 999)
		#define FREE  0
    	#define OPEN  1
    	#define WALL  2
    	#define START  3
    	#define END  4
    	#define PATH  5

		#define VISITED  1
		#define UNDEFINED  1600
		
		#define FALSE 0
		#define TRUE 1
		
		void GetSemaphor(__global int * semaphor) {
   			int occupied = atom_xchg(semaphor, LOCKME);
   			while(occupied > 0)
   			{
     			occupied = atom_xchg(semaphor, LOCKME);
   			}
		}

 

		void ReleaseSemaphor(__global int * semaphor)
		{
   			int prevVal = atom_xchg(semaphor, 0);
		}
		
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

				if  ( visited[ii+1] != FREE && (maze[ii+1] != WALL || maze[ii+1] == START) ){
					return TRUE;
				}
			}
			if( (ii >= 1 ) && get_y(width, ii) == get_y(width, ii - 1)   )  {

				if  ( visited[ii - 1] !=   FREE && (maze[ii-1] != WALL  || maze[ii-1] == START)){
					return TRUE;
				}
			}
			if  (ii +   width < dim) {

				if(visited[ii + width] !=  FREE && (maze[ii+ width] != WALL  || maze[ii+width] == START ) ) {
					return TRUE;
				}
			}
			if  (ii >= width ) {

				if (visited[ii - width] !=  FREE &&( maze[ii-width] != WALL || maze[ii-width] == START ) ) {
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
         		int dim,
        		int  test) {
        		
            //ii = get_global_id(0);
        	int alt = 0;
        	
        
        	if   ((visited[test] !=   VISITED )// && visited[ii] != VISITED
        			&& maze[test] != WALL && maze[ii] != WALL) {
        			
        		alt = dist[ii] + 1;
        		if (dist[ii] == UNDEFINED  ) alt = 0;
        		if (maze[ii] == START) {
        			//alt = 0;
        		}
        		
				if  (alt < dist[ii] || dist[test] == UNDEFINED ){//dim ){// || maze[test] == START ){
					//if   (maze[test] !=   START || (maze[ii] == START && test != ii)) {
						GetSemaphor(&mutex[test]);
						//while(LOCK(&mutex[test]) != LOCKME);// spin
				  		prev[test] = ii; 
				  		
				  		//prev[ii] = test;
				  		dist[test] = alt;
				  		//atom_add(&dist[test], alt);
				  		//UNLOCK(&mutex[test]);
				  		ReleaseSemaphor(&mutex[test]);
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
			
			int up, down, left, right;
			up = 0;
			down = 0;
			left = 0;
			right = 0;
			
			//while(LOCK(&mutex[ii]) != LOCKME);// spin
			if (visited[ii] == VISITED && maze[ii] == END ){
           		flag = 1;
           		localflag = 1;
           		dimension[2] = 1;
           		//return;
           }
           
           //else {
       		
       		if (flag == 0) {
       			//while(LOCK(&mutex[ii]) != LOCKME);// spin
       			//GetSemaphor(&mutex[ii]);
       			i ++;
		   		if ((visited[ii] ==  FREE &&  maze[ii] !=  WALL) ) {
       				//GetSemaphor(&mutex[ii]);
					//while(LOCK(&mutex[ii]) != LOCKME);// spin
					
					/////////////////////////////////////////////

					if ( (ii + 1 < dim) && get_y(width,ii) == get_y(width,ii + 1)  
						&& near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex,dim,ii + 1);
					}

					if ( (ii >=1) && get_y(width,  ii) == get_y(width,  ii - 1)  
						&& near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex,dim, ii - 1);
					}

					if ( ii +  width < dim  && near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex,dim, ii +  width);
					}

					if (( ii >=  width)   && near_visited(ii, maze, visited, width, height)) {
						must_check(ii,maze, visited, dist, prev, mutex,dim, ii -  width);
					}

					if  ( maze[ii] ==  START) {
						//dist[ii] = 0;
						//atom_xchg(&visited[ii], VISITED);
						//must_check(ii,maze, visited, dist, prev, mutex, ii);						
					}

					if (near_visited(ii, maze, visited, width, height) == TRUE) {
						// visited[ii] =  VISITED;
						//while(LOCK(&mutex[ii]) != LOCKME);// spin
						//GetSemaphor(&mutex[ii]);
						visited[ii]= VISITED;
						//UNLOCK(&mutex[ii]);
					}
					////////////////////////////////////
					
					//UNLOCK(&mutex[ii]);
					//ReleaseSemaphor(&mutex[ii]);
				}
				//UNLOCK(&mutex[ii]);
				//ReleaseSemaphor(&mutex[ii]);
       		}
       		
           barrier(CLK_LOCAL_MEM_FENCE);
           
           
           //UNLOCK(&mutex[ii]);
			//	
			
           
        }

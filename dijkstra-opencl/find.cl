		#define FREE  0
    	#define OPEN  1
    	#define WALL  2
    	#define START  3
    	#define END  4
    	#define PATH  5

		#define VISITED  1
		#define UNDEFINED  -1
		
		
		int get_x(int width,  int ii) {
 			return ii - (width * (ii / width));   
        }
        
        int get_y(int width, int ii) {
        	return (int)( ii / width);
        }
        int get_index(int width, int x, int y) {
        	return (y * width) + x;
        }
        
        int near_visited( __global int* maze, 
        			__global int* visited, 
        			int width, 
        			int height) {
        			
            unsigned int ii = get_global_id(0);
            int dim = width * height;
            
            
			if (get_y(width,ii) == get_y(width,ii + 1) &&  ii + 1 < dim ) {
				if  ( visited[ii+1] ==   VISITED){
					return 1;
				}
			}
			if( get_y(width, ii) == get_y(width, ii - 1) &&  ii >= 1 )  {
				if  ( visited[ii - 1] ==   VISITED){
					return 1;
				}
			}
			if  (ii +   width < dim) {
				if   (visited[ii + width] ==   VISITED) {
					return 1;
				}
			}
			if  (ii >= width ) {
				if   (visited[ii - width] ==   VISITED) {
					return 1;
				}
			}
			if  (maze[ii] == START ){
				return 1;
			}
			return 0;
            
            
        	//visited[ii] = 1;
        	//return 1;
        }
        void must_check(
        		__global int* maze, 
         		__global int* visited, 
         		__global int* dist, 
         		__global int* prev,
        		int  test) {
        		
            unsigned int ii = get_global_id(0);
        	
        
        	if   (visited[test] !=   VISITED &&   maze[ii] !=   WALL) {
				if  ( dist[ii] + 1 <=   dist[test] || dist[test] == UNDEFINED ) {
					if   (maze[test] !=   START  ) {
				  		prev[test] = ii; 
				  		dist[test] =   dist[ii] + 1;
				  	}
				}
			}
	
            //barrier(CLK_LOCAL_MEM_FENCE);
        
        }
        
         __kernel void find(
         		__global int* maze, 
         		__global int* visited, 
         		__global int* dist, 
         		__global int* prev,
         		__global int* dimension)
         		
        {
        	
			
            unsigned int ii = get_global_id(0);
            
 			unsigned int width = dimension[0];
 			unsigned int height = dimension[1];
 			unsigned int dim = width * height;
 			
 			unsigned int flag = 0;
 			unsigned int localflag = 0;
 			unsigned int i = 0;

       		//while (flag == 0 && i < dim) {
       		if (1) {
       		
       			i ++;
		   		if (visited[ii] ==  FREE &&  maze[ii] !=  WALL) {

					if (get_y(width,ii) == get_y(width,ii + 1)  
						&& ii + 1 < dim  && near_visited(maze, visited, width, height)) {
						must_check(maze, visited, dist, prev, ii + 1);
					}

					if (get_y(width,  ii) == get_y(width,  ii - 1)  
						&& ( ii >= 1)  && near_visited(maze, visited, width, height)) {
						must_check(maze, visited, dist, prev, ii - 1);
					}

					if ( ii +  width < dim  && near_visited(maze, visited, width, height)) {
						must_check(maze, visited, dist, prev, ii +  width);
					}

					if (( ii >=  width)   && near_visited(maze, visited, width, height)) {
						must_check(maze, visited, dist, prev, ii -  width);
					}

					if  ( maze[ii] ==  START) {
						must_check(maze, visited, dist, prev, ii);
					}

					if (near_visited(maze, visited, width, height)) {
						 visited[ii] =  VISITED;
					}
				}
       		}
       		
           barrier(CLK_LOCAL_MEM_FENCE);
           
           if (visited[ii] == VISITED && maze[ii] == END ){
           		flag = 1;
           		localflag = 1;
           		//dimension[2] = 1;
           		return;
           }
			//	
			
           
        }

		int get_x(int width,  int ii) {
 			return ii - (width * (ii / width));   
        }
        
        int get_y(int width, int ii) {
        	return ii / width;
        }
        int get_index(int width, int x, int y) {
        	return (y * width) + x;
        }
        
        int near_visited(__global float* visited, int width, int height) {
            unsigned int ii = get_global_id(0);
            int dim = width * height;
            int VISITED = 1;
            
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
			//if  ii == get_ ii(  startx,   starty)  :
			//	return 1
			return 0;
            
            
        	//visited[ii] = 1;
        	//return 1;
        }
        void must_check(int  ii) {
        
        }
        
         __kernel void find(
         		__global float* maze, 
         		__global float* visited, 
         		__global float* dist, 
         		__global float* prev,
         		__global float* dimension)
         		
        {
        	int FREE = 0;
        	int OPEN = 1;
        	int WALL = 2;
        	int START = 3;
        	int END = 4;
        	int PATH = 5;

			int VISITED = 1;
			int UNDEFINED = -1;
			
            unsigned int ii = get_global_id(0);
            
 			unsigned int width = dimension[0];
 			unsigned int height = dimension[1];
 			unsigned int dim = width * height;
 			
 			unsigned int flag = 0;
 			unsigned int localflag = 0;
 			unsigned int i = 0;

       		//while (flag == 0 && i < dim) {
       		if (1) {
		   		if (visited[ii] ==  FREE &&  maze[ii] !=  WALL) {

					if (get_y(width,ii) == get_y(width,ii + 1)  
						&& ii + 1 < dim  && near_visited(visited, width, height)) {
						must_check(ii + 1);
					}

					if (get_y(width,  ii) == get_y(width,  ii - 1)  
						&& ( ii >= 1)  && near_visited(visited, width, height)) {
						must_check(ii - 1);
					}

					if ( ii +  width < dim  && near_visited(visited, width, height)) {
						must_check(ii +  width);
					}

					if (( ii >=  width)   && near_visited(visited, width, height)) {
						must_check(ii -  width);
					}

					if  ( maze[ii] ==  START) {
						must_check(ii);
					}

					if (near_visited(visited, width, height)) {
						 visited[ii] =  VISITED;
					}
				}
       		}
           
           //prev[ii] =  maze[ii];
           
        }

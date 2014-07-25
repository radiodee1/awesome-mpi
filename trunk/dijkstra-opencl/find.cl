		int get_x(int width,  int ii) {
 			return ii - (width * (ii / width));   
        }
        
        int get_y(int width, int ii) {
        	return ii / width;
        }
        int get_index(int width, int x, int y) {
        	return (y * width) + x;
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
       		
       		while (flag == 0 && i < dim) {
       		
		   		if (visited[ii] ==  FREE && main[ii] !=  WALL) {
						
					if (get_y(width,ii) == get_y(width,ii + 1)  && ii + 1 < dim  && near_visited()) {
						must_check(ii + 1,  RIGHT);
					}
					if (get_y(width, ii) == get_y(width, ii - 1)  && ii - 1 >= 0  && near_visited()) {
						must_check(ii - 1,  LEFT);
					}
					if (ii +  width < dim  && near_visited()) {
						must_check(ii +  width,  DOWN);
					}
					if (ii -  width >= 0  && near_visited()) {
						must_check(ii -  width,  UP);
					}
					if  (main[ii] ==  START) {
						must_check(ii,  CENTER);
					}

					if (near_visited()) {
						 visited[ii] =  VISITED;
					}
				}
       		}
           
           prev[ii] =  maze[ii];
           
        }

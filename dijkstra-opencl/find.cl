float add(float a, float b)
        {
            
 			return 2*(a + b);
            
        }
         __kernel void find(
         		__global float* maze, 
         		__global float* visited, 
         		__global float* dist, 
         		__global float* prev,
         		__global float* dimension)
         		
        {
            unsigned int ii = get_global_id(0);
            
 			unsigned int width = dimension[0];
 			unsigned int height = dimension[1];
 			
           //c[i] = add (a[i] , b[i]);
           prev[ii] = maze[ii];
        }


#include "mpi.h" 

int main(int argc, char *argv[]) 
{ 

int myrank, numprocs, length_name; 
char nodename[128]; 

MPI_Init(&argc, &argv); 
MPI_Comm_rank(MPI_COMM_WORLD, &myrank); 
MPI_Comm_size(MPI_COMM_WORLD, &numprocs); 
MPI_Get_processor_name(nodename, &length_name); 
printf("Hellow, MPI! (%0d/%0d)-- %s\n", myrank, numprocs, nodename); 
MPI_Finalize(); 
return 0; 

}

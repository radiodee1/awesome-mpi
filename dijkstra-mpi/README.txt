README

the object here is to make dijkstra's algorithm work on a simple maze
with the dimensions of 10 x 10. Here we also want to use MPICH2.

then we want to make a version that runs on a picture thousands
of pixels in dimension. Here we want to use OpenCL.

for MPICH2 we will try to simply run mpiexec with 100 nodes, using
a machine file that identifies 3 computers with 4 cores each.

The 12 cores will be used by the MPICH2 system as if they were
100.

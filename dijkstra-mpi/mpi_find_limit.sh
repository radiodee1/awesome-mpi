echo 'if this file does not work edit the array_setup.py file '

mpiexec.hydra -np 300 -f /mirror/awesome-mpi/machinefiles/machinefile-3x4 /mirror/awesome-mpi/dijkstra-mpi/find_path.py /mirror/awesome-mpi/dijkstra-mpi/wallfile-limit.txt



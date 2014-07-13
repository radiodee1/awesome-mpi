the folder /mirror is owned by the 'dave' user, and is mirrored on all three vm's.

the 'dave' user has ssh set up to allow him/her to login to the three vm's
without password

the 'awesome-mpi' svn repository is set up in the '/mirror' folder, so all that
is needed to run mpich programs is to log in as 'dave' and cd to '/mirror'.
Then use 'mpiexec.hydra' to run code.

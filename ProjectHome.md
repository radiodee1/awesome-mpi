# NOTES: #

## Setup: ##

These programs and scripts were initially tested on a simple laptop with Fedora 20 on it. The laptop also had Intel GPU which could be used for OpenCL and also MPICH2 so that mpi could be tested. Almost all the programming was done in Python. For MPI the mpi4py package was used from the Fedora repository. For OpenCL Beignet was installed from the repository, and also pyopencl was installed from source. A link to pyopencl 2014.1 is included below.

Later, a group of three vm's were made available to me, that were configured as a MPICH2 cluster. They ran with four cores each and at about 2.0 GHz. They were configured for mpi with CentOS 6. When I was trying to implement Dijkstra's algorithm the cluster was used.

https://pypi.python.org/packages/source/p/pyopencl/pyopencl-2014.1.tar.gz

A list of python libraries that are used in these python projects would include: pyopencl, math, numpy, time, fileinput, pygame, and sys.

## Addition Programs: ##

The trunk of the svn repository has several python programs in it, all that test out the speed of some simple mathematical computations. Essentially they all add lists of integers together. There is a addition program that works on a cpu (what you might consider as the base case), an mpi installation (tested on a cluster of one computer and then three computers), and finally a gpu situation (where an intel gpu is used initially). I should note that there is a python script called 'bad\_arrays\_mpi.py' that takes a long time AND is highly inefficient. It is included as an example of time spent poorly. There are two other mpi based scripts. One adds the numbers together and exits, while the other adds the numbers together and then returns the numbers. This second script it much slower. Both are included because opencl and cpu programs don't typically have to return any values, they just add them together.

## Folders: ##

The list of folders in the trunk directory of the svn repository is below:

```
dijkstra-cpu
dijkstra-mpi
dijkstra-opencl
examples
machinefiles
src
system-scripts
```

Most of the folders have some relation to testing out MPI. This is not the case for the 'dijkstra-opencl' folder. Also, the 'dijkstra-mpi' folder is used with the 'machinefiles' folder. The 'system-scripts' folder has scripts that were used in setting up MPI on the CentOS 6 machines. The 'src' folder has a c program that can be used to test a MPI install, as does the 'examples' folder. The 'dijkstra-opencl' folder has python scripts that are used for OpenCL only. I will go over the contents of all the folders below.

## dijkstra-cpu ##

This folder has a version of the test program that runs on a single cpu on any computer. It was tested out on a fedora 20 64-bit laptop. The programs in this folder function much the way that the 'dijkstra-opencl' programs do, and they have much the same limitations. The major difference when running them is that they take longer (sometimes seconds longer) than the opencl version. This program is included mostly for speed comparisons.

## dijkstra-mpi ##

This folder has the python scripts that use dijkstra's algorithm for MPI. Originally they were all used to test out an MPI install on just one laptop. Later they were used on the three vm cluster mentioned above.

The scripts took a basic shape. There was an 'array\_setup.py' script which had the given maze in it, then there was the 'node.py' script that contained the essential algorithm, and the 'find\_path.py' script, which was the launching point and which called the two other python scripts. These essential scripts must all be in the same directory. Additionally there was a file called a 'wallfile' which could be specified on the command line which would help define mazes of different sizes.

There were also some bash scripts which had pre-defined conditions and maze sizes. They basically used the vm cluster, and therefore the machinefile that was associated with the cluster. They were helpful for testing out the vm's and that's about it.

There was also one file callet 'find\_printout\_start.py' that was used to print the maze to the screen without running the algorithm. It loads the 'array\_setup.py' file and prints the maze to the screen from that file. It's use is a little limited, but it came in handy on the laptop when running the full algorithm on the maze would take more than a minute and seeing the maze on the screen was all that was desired.

There is a file in the folder called 'trace\_my\_trace.py'. This came from a text on python programming and it helps to time each line of a program to see what portions take the most time. It was very helpful. The book is called 'Foundations of Python Network Programming'.

There is a folder in the 'dijkstra-mpi' folder called 'test-results'. It holds, as expected, test results that show how long mazes of certain sizes took to process on the laptop and the vm cluster. The output from several runs of the 'trace\_my\_trace.py' program are also here.

## dijkstra-opencl ##

This is the folder where the test for opencl is located. It's the only part of the svn repository that is not concerned with mpi. The ptyhon code here relies on OpenCl, using Beignet on the Fedora 20 installation. It also uses pyopencl installed from source. It also uses pygame and numpy. Pygame is used to allow for a gui for the program when testing that uses a 'png' for a map. Pygame, in this instance, is blitting the image to the screen, and therefore uses the cpu. Then opencl uses the GPU to figure out a solution for the maze that the user selects. The image is not using the 3d rendering of the GPU, so a gui and the opencl seem to work together.

Some of the scripts in this folder are actually based on scripts from the MPI project, so the names of some of the files are the same. The 'array\_setup.py' file is one of those. It contains the setup for a minimal maze and also the initialization for many arrays and some enumerations. Like that file with the same name in the mpi folder this file is not called from the command line but rather from another python script.

There is a file called 'dijkstra-opencl.py'. This is the file called from the command line. It calls the 'array\_setup.py' file and it runs the gui and the opencl program. It loads the 'find.cl' file and builds it and runs it as a 'kernel' on the GPU. It has a option '-nogui' which runs the program in text mode. It has a nother option '-output', which, when run in gui mode, spits out a 'wallfile' that represents the last map you tried to navigate on the screen. Finally it takes as an argument a 'wallfile'. If the program is not running in gui mode, a wallfile can be used to load wall definition information.

There is a file called 'find.cl'. This file contains the code that is built and turned into the GPU kernel. This is essentially a c file. The programming language is essentially something called 'C99'. At this writing this file contains three kernel modules, which all essentially use a subroutine called 'sub'.

There is a file called 'map.png'. This is an image in high contrast that represents Manhattan. Any image could be used. Pygame displays this image in a window. Then you use the arrow keys to select the part of the image you are interested in. Then the program blows up that segment of the png to the size of the window and you can use the controls on the screen to test the program. You put a green marker where you want the program to start, you put a red marker where you want the program to stop, and when you're done you press the blue square to tell the program to find a solution. It usually does, marking the path from the start to the finish with blue dots. When you are finished you may press the return button or click the mouse button to signify that you are done. At that point the screen goes back to the stage where you can select an area from the larger map.

There is also a set of files named 'wallfile.txt' or something similar. These files have the definition of mazes in them that allows you to test a maze out without the gui interface, from the command line. The format of the files is simple. Comment lines begin with a '#' in the first space. (No space is allowed in a comment line before the '#' mark.) The first non comment line has the width and height of the maze separated by a comma. The second non-comment line contains a comma separated list of wall cells. The entries are in the format `(y * width) + x` so that a single number can represent a wall cell anywhere in the maze.

## examples ##

This folder contains c files for computing pi on an MPI installation. There are three files, 'cpi', 'cpi.c', and 'cpi.o' . 'cpi' is an executable but 'cpi.c' is probably most important, as you can use it to compile the test program for your system. The command to start the test executing on the mpi installation is as follows:

```
mpiexec.hydra -n 12 -f ../machinefiles/machinefile-3x4 ./cpi
```

After that output on the screen should show the value of pi and how long it took the program to calculate it. The 'machinefiles' directory was specific to the tests from this project.

## machinefiles ##

Below is the contents of a typical machinefile:

```
vm-node0:4
vm-node1:4
vm-node2:4
```

Each line is the hostname for one of the machines from the cluster, followed by a colon, followed by a number representing how many nodes should be run on that machine. This arrangement is standard for mpi and is well documented. I set up a separate folder to hold my machinefiles and stored it in the svn repository.

## src ##

This folder contians source for another c program for testing mpi. This one is called 'mpi\_helloworld.c'.

## system-scripts ##

This folder holds scripts that I used for installing software on the vm cluster. After installing the OS, I would install svn right away and then run svn update to get the scripts from this folder onto the machine. Then I would use the scripts to install software identically on all three machines. I am not going to describe the contents of each file. Some, usually with the '.sh' file extension, can be executed, and most have notes in them that describe some of their purpose. They are disorganized for the most part.


---

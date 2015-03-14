# dijkstra-opencl.py #

This is a description of the 'dijkstra-opencl.py' program. It also includes some info on command-line options. The program itself uses dijkstra's algorithm to navigate a simple maze. The navigation itself is done by OpenCL on a GPU. There is a graphical user interface that allows the user to specify a graph for the algorithm to search. This graph is chosen at runtime and can be almost completely different from run to run. The program can also be used in a non-graphical setting, where graphs can be loaded from text files and then tested. The program can also measure the time that a given computation took to complete.

## INSTALLATION: ##

This program uses python. It was installed on a laptop with Fedora 20 on it. It also uses OpenCL and Beigenet. Standard packages for both OpenCL and Beignet exist in the Fedora repository. 'opencl-devel' and 'beignet-devel' were also installed, along with 'ocl-icd', which allowed pyopencl to be compiled and installed on the computer.

## RUNNING: ##

These are examples of program execution:
```
./dijkstra-opencl.py 
./dijkstra-opencl.py -nogui
./dijkstra-opencl.py -nogui wallfile.txt
./dijkstra-opencl.py -output
./dijkstra-opencl.py -single-kernel
./dijkstra-opencl.py -size 100
```
This is an explanation of the examples:
```
./dijkstra-opencl.py
```
This starts the program in full gui mode. In this mode the map window pops up and you select a portion of the map that you select a small area from. Then this area is magnified. You select start and end positions on the map and the gui shows in blue a path or solution.
```
./dijkstra-opencl.py -nogui
```
The program starts in text-only mode. Then it finds it's way through a simple pre-defined maze. There is no interaction and the maze is diminutive.
```
./dijkstra-opencl.py -nogui wallfile.txt
```
The program starts in text-only mode. Then it loads the information from the 'wallfile' which describes certian parts of the maze. Then it finds it's way through the maze. There is no interaction, but the maze can be any size. There can only be one 'wallfile' specified on the command line.
```
./dijkstra-opencl.py -output
```
This starts the program in full gui mode. When the session is completed the program saves information on the last selected maze as a 'wallfile' which can be used in later testing without the gui. This makes testing on a reasonably complex maze possible at the command line for later execution. This option does not work with the '-nogui' option.
```
./dijkstra-opencl.py -single-kernel
```
When the program starts with this option it attempts to use a 'single kernel' execution scheme. This can be used with other options. If the GPU doesn't support out-of-order execution the program reverts to a 'two kernel' execution scheme automatically.
```
./dijkstra-opencl.py -size 100
```
Here it is possible to specify the width and height of the area of the map that will be considered by the program. In this example '100' is used but other values can be specified. The invocation above would set the square to 100 width times 100 height. Values as small as 6 or 8 are possible, as are values as high as 100 or 150. At some point it is difficult to see the solution that the program finds for a given map because the pixels are so small. The window that the program uses is 480 by 480. This option can be used with others.

## NOTES ON THE GUI: ##

A typical session with the gui might go as follows.

  1. Start the gui from the command line. A simple map will open in a window on the screen.
  1. Use the arrow keys to select a part of the map.
  1. Press the return key to designate your selection.
  1. The screen changes to show the selected part of the map close up.
  1. Click on the green box once with the mouse pointer to indicate you want to place the 'start' location on the map.
  1. Move the mouse to the part of the map where you want the 'start' location to be. Click once to place the green box.
  1. Do the same as 5 and 6 for the red box to indicate where the 'end' location should be.
  1. Click on the blue box to indicate that you are done placing markers and that you would like the path to be shown.
  1. Blue boxes appear on the screen showing the path that the program has found.
  1. Click with the mouse on the map, or press 'return' on the keyboard to return to the larger map.
  1. Use the program again by returning to step 2.


---

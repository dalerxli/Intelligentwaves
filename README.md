# IntellegenceWave
Scientific computing programs for light behavior prediction using convalutional neural network

## Description
This programs is mainly to approximate solver in traditional electromagnetism numerical algorithms. Main idea is to grasp the relation of scatterer geometry and its produced wave solution. Currently in progressing...

__Finished__:
1. Create the mesh object to generate mesh files for data generation by traditional solver. The mesh object contains full information of patch, edge, nodes and thier relationship.

__To do__:
1. Wrap the solver from Fortran to Python to generate enough input-output dataset. This may be done by glue Fortran to python or use Fortran itself.

2. Create proper CNN architecure using Tensorflow. The key point is the input file may not be samesized (cannot shrink or enlarge).

3. Train the CNN and find the optimal hyperparameters and architecures.

4. Finish statistical comparison and other utils.

## Requirement
Python 3.5 or above, Fortran

## Running
To create a mesh we need the input file representing the square mesh by 2D list or numpy array. The 1's in array represent the pad with metal and 0's represent the void. For example:
```
pad = [[0, 1, 1], [1, 0, 1], [1, 1, 1]]
```
This list represents a square pad with left upper corner and middle one to be void. To create the mesh object with pad lenght _l_ and width _w_, change the directory and type:
```
mesh = Mesh(pad, l, w)
```
Access all the node, patch, edge information and relationship from the mesh object. And to visualize the mesh, just type:
```
mesh.printMesh()
```
The meshed structure will be shown in terminal where + stands for metal dn - stands for void.

# 3D Curved Grape Stem Generator

This program generates the set of points of a 3d curved cylinder and produces a digital phantom (set of PGM files) of the model. 

The input data needed:
 - 2 points in 3D (positive values only)
 - Curvature angle of the cylinder (between 0 and 360 - _if choose to create a model with an angle bigger than 270 the model will become quite big to accommodate the angle_)
 - Radius of the cylinder (positive integer)
 - Size for the PGM file in px (no smaller than 50px)

### Prerequisites

The following imports are needed to run the project:

 - Python 3: https://www.python.org/downloads/
 - Matplotlib: https://matplotlib.org/3.2.0/users/installing.html
 - NumPy: 
```
pip3 install numpy
```
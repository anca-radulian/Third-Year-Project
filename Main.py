import matplotlib.pyplot as plt
import grapeStemGenerator
from DigitalPhantomGenerator import DigitalPhantomGenerator
import numpy as np


# Main program (first will be GUI stuff)
A = [20.0, 6.0, 10.0]
B = [50.0, 60.0, 100]
curve_angle = 35
radius_cylinder = 10

x_arc, y_arc, z_arc, C = grapeStemGenerator.generate_arc_coordinates(A, B, curve_angle)
X, Y, Z = grapeStemGenerator.generate_cylinder_coordinates(x_arc, y_arc, z_arc, radius_cylinder, C)

#grapeStemGenerator.plot_points(X, Y, Z, 250, A, B, C)

DigitalPhantomGenerator().create_digital_phantom_of_models('x', X, Y, Z)
# DigitalPhantomGenerator().create_digital_phantom_of_models('y', X, Y, Z)
# DigitalPhantomGenerator().create_digital_phantom_of_models('z', X, Y, Z)


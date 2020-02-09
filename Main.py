import grapeStemGenerator
from DigitalPhantomGenerator import DigitalPhantomGenerator
import tkinter as tk
from tkinter import messagebox, W, E, N, S


def generate_stem_phantom():
    A = [coord1_x.get(), coord1_y.get(), coord1_z.get()]
    B = [coord2_x.get(), coord2_y.get(), coord2_z.get()]
    x_arc, y_arc, z_arc, C = grapeStemGenerator.generate_arc_coordinates(A, B, curve_angle.get())
    X, Y, Z = grapeStemGenerator.generate_cylinder_coordinates(x_arc, y_arc, z_arc, radius_cylinder.get(), C)
    # grapeStemGenerator.plot_points(X, Y, Z, 250, A, B, C)

    # DigitalPhantomGenerator().create_digital_phantom_of_models('x', X, Y, Z)
    # DigitalPhantomGenerator().create_digital_phantom_of_models('y', X, Y, Z)
    # DigitalPhantomGenerator().create_digital_phantom_of_models('z', X, Y, Z)

    print("Generation successful")

window = tk.Tk()
# to rename the title of the window
window.title("Grape Stem Generator")
# pack is used to show the object in the window
# label = tk.Label(window, text="This application generates PGM files from a 3D model of a curved grape stem").pack()

coord1 = tk.Label(window, text="Enter coordinates for the first point").grid(row=0, columnspan=5, sticky=W)

coord1_x = tk.DoubleVar()
coord1_y = tk.DoubleVar()
coord1_z = tk.DoubleVar()

coord1_entry_x = tk.Entry(window, textvariable=coord1_x).grid(row=1, column=1)
coord1_entry_y = tk.Entry(window, textvariable=coord1_y).grid(row=1, column=3)
coord1_entry_z = tk.Entry(window, textvariable=coord1_z).grid(row=1, column=5)

coord1_label_x = tk.Label(window, text="X").grid(row=1)
coord1_label_y = tk.Label(window, text="Y").grid(row=1, column=2)
coord1_label_z = tk.Label(window, text="Z").grid(row=1, column=4)

coord2 = tk.Label(window, text="Enter coordinates for the second point").grid(row=4, columnspan=5, sticky=W)

coord2_x = tk.DoubleVar()
coord2_y = tk.DoubleVar()
coord2_z = tk.DoubleVar()

coord2_entry_x = tk.Entry(window, textvariable=coord2_x).grid(row=5, column=1)
coord2_entry_y = tk.Entry(window, textvariable=coord2_y).grid(row=5, column=3)
coord2_entry_z = tk.Entry(window, textvariable=coord2_z).grid(row=5, column=5)

coord2_label_x = tk.Label(window, text="X").grid(row=5)
coord2_label_y = tk.Label(window, text="Y").grid(row=5, column=2)
coord2_label_z = tk.Label(window, text="Z").grid(row=5, column=4)

curve_angle = tk.IntVar()
radius_cylinder = tk.IntVar()

curve_angle_label = tk.Label(window, text="Insert the curvature of the cylinder",fg="purple").grid(row=6, columnspan=2, sticky=W)
radius_cylinder_label = tk.Label(window, text="Insert the radius of the cylinder", fg="purple").grid(row=7, columnspan=2, sticky=W)

curve_angle_entry = tk.Entry(window, textvariable=curve_angle).grid(row=6, column=3)
radius_cylinder_entry = tk.Entry(window, textvariable=radius_cylinder).grid(row=7, column=3)

button = tk.Button(window, text="Generate", fg="green", command= generate_stem_phantom).grid(row=8, column=3)
window.mainloop()

# Main program (first will be GUI stuff)
# A = [110.1, 6.0, 79.1]
# B = [110.0, 240.0, 79.0]
# curve_angle = 60
# radius_cylinder = 10

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import grapeStemGenerator
from DigitalPhantomGenerator import DigitalPhantomGenerator
import tkinter as tk
from tkinter import messagebox, W, E, N, S


def validate_inputs():
    try:
        if coord1_x.get() < 0 or coord1_y.get() < 0 or coord1_z.get() < 0 \
                or coord2_x.get() < 0 or coord2_y.get() < 0 or coord2_z.get() < 0:
            messagebox.showerror(title="Wrong coordinates values", message="Please enter positive values for "
                                                                           "coordinates")
            return False
    except tk.TclError:
        messagebox.showerror(title="Wrong coordinate value", message="Please enter float values for coordinates")
        return False

    try:
        if curve_angle.get() < 0 or curve_angle.get() > 180:
            messagebox.showerror(title="Wrong curve angle value", message="Please enter an angle value between 0 and "
                                                                          "180")
            return False
    except tk.TclError:
        messagebox.showerror(title="Wrong curve angle value", message="Please enter float values for the curve angle")
        return False

    try:
        if radius_cylinder.get() < 1:
            messagebox.showerror(title="Wrong radius cylinder value", message="Please enter a positive value for the "
                                                                              "cylinder radius")
            return False
    except tk.TclError:
        messagebox.showerror(title="Wrong radius cylinder value", message="Please enter integer values for the "
                                                                          "cylinder radius")
        return False

    try:
        if pgm_size.get() < 10 or pgm_size.get() > 300:
            messagebox.showerror(title="Wrong PGM file size", message="Please enter a file size between 10 and 300")
            return False
    except tk.TclError:
        messagebox.showerror(title="Wrong PGM file size", message="Please enter integer values for the PGM file size")

    return True


def on_closing():
    button["state"] = tk.NORMAL


def generate_stem_phantom():
    if not validate_inputs():
        return

    A = [coord1_x.get(), coord1_y.get(), coord1_z.get()]
    B = [coord2_x.get(), coord2_y.get(), coord2_z.get()]
    x_arc, y_arc, z_arc, C = grapeStemGenerator.generate_arc_coordinates(A, B, curve_angle.get())
    X, Y, Z = grapeStemGenerator.generate_cylinder_coordinates(x_arc, y_arc, z_arc, radius_cylinder.get(), C)

    if create_plot.get() == 1:
        button["state"] = tk.DISABLED
        window2 = tk.Toplevel(window)
        window2.protocol("WM_DELETE_WINDOW", on_closing)

        figure = grapeStemGenerator.plot_points(X, Y, Z, pgm_size.get(), A, B, C)

        canvas = FigureCanvasTkAgg(figure, master=window2)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack()

    # DigitalPhantomGenerator().create_digital_phantom_of_models('x', X, Y, Z)
    # DigitalPhantomGenerator().create_digital_phantom_of_models('y', X, Y, Z)
    # DigitalPhantomGenerator().create_digital_phantom_of_models('z', X, Y, Z)
    messagebox.showinfo(title="Successful generation", message="The PGM files have been generated successfully!")


def message_plot():
    if create_plot.get() == 1:
        ans = messagebox.askquestion(title="Generate Plot", message="The generation of the plot will take some time."
                                                                    "Do you still want to proceed?")

        if ans == 'no':
            create_plot.set(0)


window = tk.Tk()

# to rename the title of the window
window.title("Grape Stem Generator")

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

curve_angle = tk.DoubleVar()
radius_cylinder = tk.IntVar()

curve_angle_label = tk.Label(window, text="Insert the curvature of the cylinder").grid(row=6, columnspan=3,
                                                                                       sticky=W)
radius_cylinder_label = tk.Label(window, text="Insert the radius of the cylinder").grid(row=7, columnspan=3,
                                                                                        sticky=W)
curve_angle_entry = tk.Entry(window, textvariable=curve_angle).grid(row=6, column=3)
radius_cylinder_entry = tk.Entry(window, textvariable=radius_cylinder).grid(row=7, column=3)

pgm_size = tk.IntVar()

pgm_size_label = tk.Label(window, text="Specify the PGM file size").grid(row=8, columnspan=3, sticky=W)
pgm_size_entry = tk.Entry(window, textvariable=pgm_size).grid(row=8, column=3)

create_plot = tk.IntVar()

c = tk.Checkbutton(window, text="Create plot of model", variable=create_plot,
                   command=message_plot).grid(row=9, columnspan=2, sticky=W)

button = tk.Button(window, text="Generate", command=generate_stem_phantom)
button.grid(row=10, column=3)
window.mainloop()

# Main program (first will be GUI stuff)
# A = [110.1, 6.0, 79.1]
# B = [110.0, 240.0, 79.0]
# curve_angle = 60
# radius_cylinder = 10
# pgm file size = 250

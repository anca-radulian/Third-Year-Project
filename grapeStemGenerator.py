import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# --------------------------------------- METHODS -----------------------------------

# Let V be the normal vector on the plane defined by middle point of AB and the centre O. Then find a random point P
# using the equation of the plane xv(x−xm)+yv(y−ym)+zv(z−zm)=0.
def generate_arc_coordinates(A, B, curve_angle):
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    phi = np.deg2rad(curve_angle)
    P = np.array([5.0, 30.0, 0.0])  # random point
    if A[2] == B[2]:
        B[2] = B[2] + 0.01  # so the M point won't have the z coord 0
    M = (A + B) / 2
    AB = np.linalg.norm(A - B)
    V = A - B

    # Using plane equation calculate P
    P[2] = (-V[0] * (P[0] - M[0]) - V[1] * (P[1] - M[1])) / V[2] + M[2]

    # Height of the arc segment
    H = AB / (2 * np.tan(phi / 2))
    Pp = P - M

    Cp = H / np.linalg.norm(P - M) * Pp
    C = Cp + M

    # The slerp formula is coordinate-free and gives you a constant-speed parametrization of the arc.
    # P = C + (sin(𝛼−𝜃)𝑢+sin(𝜃)𝑣) /sin(𝛼)
    # You should use values of θ between zero and ϕ, where ϕ is the angle between OA and OB.
    X_arc = (A - C)
    Y_arc = (B - C)

    # The central angle is divided in N number of sections
    th = np.linspace(0, phi, int(AB * 3))
    x_curve, y_curve, z_curve \
        = [C[i] + ((np.sin(phi) * np.cos(th) - np.cos(phi) * np.sin(th)) * X_arc[i] + np.sin(th) * Y_arc[i]) / np.sin(
        phi) for i in [0, 1, 2]]

    return x_curve, y_curve, z_curve, C


# ================================= Cylinder plotting =================================================================
# Equation of the circle
#    (x,y,z) = (x0, y0, z0) + R cos(theta)u + R sin(theta)v
# where theta varies over the interval 0 to 2pi and t ranges over the
# the set of real numbers and
# u and v are unit vectors that are mutually perpendicular
def generate_cylinder_coordinates(x_curve, y_curve, z_curve, R, C):
    # Determine how many points will be used to draw the circle
    theta = np.linspace(0, 2 * np.pi, int(2 * np.pi * R * 3))

    X_all, Y_all, Z_all = [], [], []
    for y in range(0, x_curve.size):
        P = np.array([x_curve[y], y_curve[y], z_curve[y]])

        # vector in the plane of the circle
        w = C - P
        w /= np.linalg.norm(w)

        if y == x_curve.size - 1:
            Pp = np.array([x_curve[0], y_curve[0], z_curve[0]])
        else:
            Pp = np.array([x_curve[x_curve.size - 1], y_curve[x_curve.size - 1], z_curve[x_curve.size - 1]])

        u = C - Pp
        # normalize u
        u /= np.linalg.norm(u)

        # another vector in the circle plane orthogonal on w
        v = np.cross(u, w)
        # normalize u
        v /= np.linalg.norm(v)

        X, Y, Z = [P[i] + R * np.sin(theta) * w[i] + R * np.cos(theta) * v[i] for i in [0, 1, 2]]

        X_all = np.append(X_all, X)
        Y_all = np.append(Y_all, Y)
        Z_all = np.append(Z_all, Z)

        for j in range(R - 1, 0, -1):
            th = np.linspace(0, 2 * np.pi, int(2 * np.pi * R * 3))
            X, Y, Z = [P[i] + j * np.sin(th) * w[i] + j * np.cos(th) * v[i] for i in [0, 1, 2]]
            X_all = np.append(X_all, X)
            Y_all = np.append(Y_all, Y)
            Z_all = np.append(Z_all, Z)

    return X_all, Y_all, Z_all


def plot_for_offset(X, Y, Z, x_arc, y_arc, z_arc):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X, Y, Z, color='blue', marker='.')
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 50)
    ax.set_zlim(0, 50)

    # Used to return the plot as an image rray
    fig.canvas.draw()  # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


def plot_points(X, Y, Z, limit, A, B, C, fig, x_arc, y_arc, z_arc):
    ax = fig.add_subplot(111, projection='3d')
    ax.mouse_init()
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.set_zlim(0, limit)
    ax.scatter(C[0], C[1], C[2], color='blue')
    ax.plot(*zip(C, A), color='red', linestyle='dashed')
    ax.plot(*zip(C, B), color='red', linestyle='dashed')
    # ax.plot(*zip(B, A), color='blue')
    ax.scatter(X, Y, Z, color='blue', marker='.')
    # ax.scatter(x_arc, y_arc, z_arc, color='blue', marker='.')
    ax.scatter(A[0], A[1], A[2], color='red')
    ax.scatter(B[0], B[1], B[2], color='red')
    ax.text2D(0.05, 0.95, "Number of points generated: " + str(X.size), transform=ax.transAxes)


def create_figure():
    return plt.figure()


#  ==== Plotting the perpendicular plane =====
# formula to calculate the plane equation
# a(x−x0)+b(y−y0)+c(z−z0)=0
# x y are np.linespaces
def plot_plane(P, x, y):
    X, Y = np.meshgrid(x, y)
    Z = (-P[0] * (X - [P[0]]) - P[1] * (Y - P[1])) / P[2] + P[2]
    return Z

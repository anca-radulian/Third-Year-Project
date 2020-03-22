import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# --------------------------------------- METHODS -----------------------------------

#  Generate the centre of the circle and a set of points that describe the axis of the cylinder based on its curvature.
def generate_arc_coordinates(A, B, curve_angle):
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)

    # Avoid having angles multiple of pi, since sin(angle) will be 0 and division result will tent towards infinity
    if curve_angle % 180 == 0:
        curve_angle += 0.01

    phi = np.deg2rad(curve_angle)
    sin_phi = np.sin(phi)

    # Take random x and y coordinates for point P and use plane equation [xv(x−xm)+yv(y−ym)+zv(z−zm)=0] to calculate
    # a z coordinate which translates point P in the plane perpendicular to segment AB in M (middle point of AB)
    P = np.array([5.0, 30.0, 0.0])  # random point

    # As x and y were chosen and z will be calculated, there will be division by z value of V (perpendicular vector).
    # To avoid division by 0 which should return infinity, B's z value is incremented by a negligible value.
    if A[2] == B[2]:
        B[2] = B[2] + 0.01
    M = (A + B) / 2
    V = A - B

    # Using plane equation calculate P's z coordinate
    P[2] = (-V[0] * (P[0] - M[0]) - V[1] * (P[1] - M[1])) / V[2] + M[2]

    # Height of the triangle determined by A, B and Centre of the circle
    AB = np.linalg.norm(A - B)
    H = AB / (2 * np.tan(phi / 2))
    Pm = P - M

    # Determine centre of the circle (C) placed at distance H from point M on line MP
    Cm = H / np.linalg.norm(P - M) * Pm
    C = Cm + M

    # The slerp formula is coordinate-free and gives you a constant-speed parametrization of the arc.
    # P = C + (sin(𝛼−𝜃)𝑢+sin(𝜃)𝑣) /sin(𝛼)
    # You should use values of θ between zero and ϕ, where ϕ is the angle between CA and CB.
    X_arc = (A - C)
    Y_arc = (B - C)

    # The arc is constructed using 3 x arc_length points
    radius = np.linalg.norm(A - C)
    points_on_arc = 3 * int((curve_angle / 180) * np.pi * radius)

    # put a cap limit for the number of points generated for the arc
    if points_on_arc > 1000:
        points_on_arc = 1000

    th = np.linspace(0, phi, points_on_arc)

    # Generate points on the arc
    x_curve, y_curve, z_curve \
        = [C[i] + ((sin_phi * np.cos(th) - np.cos(phi) * np.sin(th)) * X_arc[i] + np.sin(th) * Y_arc[i]) /sin_phi for i in [0, 1, 2]]

    return x_curve, y_curve, z_curve, C


# ================================= Cylinder plotting =================================================================
# Equation of a circle in 3D
#    (x,y,z) = (x0, y0, z0) + R cos(theta)u + R sin(theta)v
# where theta varies over the interval 0 to 2pi and t ranges over the
# the set of real numbers and
# u and v are unit vectors that are mutually perpendicular
# Each disc will be made out of concentric circles
def generate_cylinder_coordinates(x_curve, y_curve, z_curve, R, C):

    # first vector in the plane of the circle
    # Determined by points A and B (end points of the arc)
    u = np.array([x_curve[0], y_curve[0], z_curve[0]]) - np.array(
        [x_curve[x_curve.size - 1], y_curve[y_curve.size - 1], z_curve[z_curve.size - 1]])
    # normalize u
    u /= np.linalg.norm(u)

    X_all, Y_all, Z_all = [], [], []
    for y in range(0, x_curve.size):
        #  current point on the arc
        P = np.array([x_curve[y], y_curve[y], z_curve[y]])

        # the second vector in the plane of the circle
        # Determined by the current point on the arc and the centre of the circle
        w = C - P
        w /= np.linalg.norm(w)

        # another vector in the concentric circles' plane, orthogonal on w
        v = np.cross(u, w)
        v /= np.linalg.norm(v)

        # Generate inner circles to create a disc
        for j in np.arange(R, -0.5, -0.5):
            th = np.linspace(0, 2 * np.pi, int(2 * np.pi * j * 3))
            X, Y, Z = [P[i] + j * np.sin(th) * w[i] + j * np.cos(th) * v[i] for i in [0, 1, 2]]
            X_all = np.append(X_all, X)
            Y_all = np.append(Y_all, Y)
            Z_all = np.append(Z_all, Z)

    return X_all, Y_all, Z_all


def plot_points(X, Y, Z,  A, B, C, fig):
    ax = fig.add_subplot(111, projection='3d')
    ax.mouse_init()
    ax.scatter(C[0], C[1], C[2], color='blue')
    ax.plot(*zip(C, A), color='red', linestyle='dashed')
    ax.plot(*zip(C, B), color='red', linestyle='dashed')
    ax.scatter(X, Y, Z, color='blue', marker='.')
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

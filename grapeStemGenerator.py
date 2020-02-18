import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# --------------------------------------- METHODS -----------------------------------

# Let V be the normal vector on the plane defined by A, B and the centre O. Then we calculate the equation of the plane
# using xv(x−xm)+yv(y−ym)+zv(z−zm)=0. Let P another point in the plane. Xp and yp be random values.
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

    P[2] = (-V[0] * (P[0] - M[0]) - V[1] * (P[1] - M[1])) / V[2] + M[2]

    Rad = AB / (2 * np.tan(phi / 2))
    Pp = P - M

    Cp = Rad / np.linalg.norm(P - M) * Pp
    C = Cp + M

    # Let X and W be unit vectors in the directions of A−O, and B−O respectively.
    # Then let Z be the unit vector in the direction of X×W, and let Y=W×X.
    # We now have an orthonormal set of vectors X,Y,Z.
    # If r is the radius of the circle, then the curve can be parameterized
    # P(θ)=O+(rcosθ)X+(rsinθ)Y
    # You should use values of θ between zero and ϕ, where ϕ is the angle between OA and OB.
    X_arc = (A - C)
    Y_arc = (B - C)

    th = np.linspace(0, phi, 500)
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
    # Angle to determine the circle
    theta = np.linspace(0, 2 * np.pi, 300)

    X_all, Y_all, Z_all = [], [], []
    for y in range(0, x_curve.size):
        P = np.array([x_curve[y], y_curve[y], z_curve[y]])

        # vector in the plane of the circle
        w = C - P
        mag = np.linalg.norm(w)
        w = w / mag

        # make some vector not in the same direction as w
        if w[1] == 0 and w[2] == 0:
            u = np.cross(w, [0, 1, 0])
        else:
            u = np.cross(w, [1, 0, 0])

        # normalize u
        u /= np.linalg.norm(u)

        # another vector in the circle plane orthogonal on w
        v = np.cross(u, w)

        X, Y, Z = [P[i] + R * np.sin(theta) * w[i] + R * np.cos(theta) * v[i] for i in [0, 1, 2]]
        # ax.scatter(X, Y, Z, color='blue', marker=",")

        X_all = np.append(X_all, X)
        Y_all = np.append(Y_all, Y)
        Z_all = np.append(Z_all, Z)

        for j in range(R - 1, 0, -1):
            X, Y, Z = [P[i] + j * np.sin(theta) * w[i] + j * np.cos(theta) * v[i] for i in [0, 1, 2]]
            X_all = np.append(X_all, X)
            Y_all = np.append(Y_all, Y)
            Z_all = np.append(Z_all, Z)

    return X_all, Y_all, Z_all


def plot_points(X, Y, Z, limit, A, B, C):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, limit)
    ax.set_ylim(0, limit)
    ax.scatter(C[0], C[1], C[2], color='green')
    ax.plot(*zip(C, A), color='red', linestyle='dashed')
    ax.plot(*zip(C, B), color='red', linestyle='dashed')
    # ax.plot(*zip(B, A), color='blue')
    ax.scatter(X, Y, Z, color='blue')

    return fig

#  ==== Plotting the perpendicular plane =====
# formula to calculate the plane equation
# a(x−x0)+b(y−y0)+c(z−z0)=0
# x y are np.linespaces
def plot_plane(P, x, y):
    X, Y = np.meshgrid(x, y)
    Z = (-P[0] * (X - [P[0]]) - P[1] * (Y - P[1])) / P[2] + P[2]
    return Z

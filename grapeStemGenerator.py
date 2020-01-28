import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)
ax.set_zlim(0, 50)

# Coordinates chosen
user_x = 20.0
user_y = 10.0
user_z = 30.0

B = np.array([user_x, user_y, user_z])  # end
A = np.array([10.0, 15.0, 10.0])  # start

# plot the axis of the
ax.plot(*zip(B, A), color='blue')

ax.scatter(B[0], B[1], B[2], color='purple')
ax.scatter(A[0], A[1], A[2], color='pink')



#  ==== Plotting the perpendicular plane =====
# formula to calculate the plane equation
# a(x−x0)+b(y−y0)+c(z−z0)=0
x = np.linspace(0, 40, 10)
y = np.linspace(0, 40, 10)
X, Y = np.meshgrid(x, y)
Z = (-user_x * (X - user_x) - user_y * (Y - user_y)) / user_z + user_z

# ax.plot_surface(X, Y, Z)

# =========================


# ----------------------------- Arc plotting  ---------------------------------------------------------------------
# Let V be the normal vector on the plane defined by A, B and the centre O. Then we calculate the equation of the plane
# using xv(x−xm)+yv(y−ym)+zv(z−zm)=0. Let P another point in the plane. Xp and yp be random values.
phi = np.deg2rad(160)  # 60 degrees in radians
P = np.array([5.0, 30.0, 0.0])
M = (A + B) / 2
AB = np.linalg.norm(A - B)
V = A - B

P[2] = (-V[0] * (P[0] - M[0]) - V[1] * (P[1] - M[1])) / V[2] + M[2]

Rad = AB / (2 * np.tan(phi / 2))
Pp = P - M

Cp = Rad / np.linalg.norm(P - M) * Pp

C = Cp + M

ax.scatter(C[0], C[1], C[2], color='green')

ax.plot(*zip(C, A), color='red', linestyle='dashed')
ax.plot(*zip(C, B), color='red', linestyle='dashed')

# Let X and W be unit vectors in the directions of A−O, and B−O respectively.
# Then let Z be the unit vector in the direction of X×W, and let Y=W×X.
# We now have an orthonormal set of vectors X,Y,Z.
# If r is the radius of the circle, then the curve can be parameterized
# P(θ)=O+(rcosθ)X+(rsinθ)Y
# You should use values of θ between zero and ϕ, where ϕ is the angle between OA and OB.

X_arc = (A - C)
Y_arc = (B - C)

alpha = phi

th = np.linspace(0, alpha, 100)

x_curve, y_curve, z_curve \
    = [C[i] + ((np.sin(alpha) * np.cos(th) - np.cos(alpha) * np.sin(th)) * X_arc[i] + np.sin(th) * Y_arc[i]) / np.sin(
    alpha)
       for i in [0, 1, 2]]

ax.scatter(x_curve, y_curve, z_curve, color='purple')

# ================================= Cylinder plotting =================================================================

# Equation of the circle
#    (x,y,z) = (x0, y0, z0) + R cos(theta)u + R sin(theta)v
# where theta varies over the interval 0 to 2pi and t ranges over the
# the set of real numbers and
# u and v are unit vectors that are mutually perpendicular

# Angle to determine the circle
theta = np.linspace(0, 2 * np.pi, 100)
# radius of the circle
R = 3

for y in range(0, 100):
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
    ax.scatter(X, Y, Z, color='blue', marker="," )

    for j in range(0, 0, -1):
        X, Y, Z = [P[i] + j * np.sin(theta) * w[i] + j * np.cos(theta) * v[i] for i in [0, 1, 2]]
        ax.scatter(X, Y, Z, color='red', marker=",")
plt.show()

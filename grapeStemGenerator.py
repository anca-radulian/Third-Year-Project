import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 30)
ax.set_ylim(0, 30)
ax.set_zlim(0, 30)

# Coordinates chosen
user_x = 20
user_y = 10
user_z = 30

c = np.array([user_x, user_y, user_z])
o = np.array([10, 15, 10])

# plot the axis of the
ax.plot(*zip(c, o), color = 'red')

# radius of the circle
R = 3

#  ==== Plotting the perpendicular plane =====
# formula to calculate the plane equation
# a(x−x0)+b(y−y0)+c(z−z0)=0
x = np.linspace(0, 40, 10)
y = np.linspace(0, 40, 10)
X,Y = np.meshgrid(x, y)
Z = (-user_x *( X - user_x) - user_y * (Y - user_y)) / user_z + user_z

# ax.plot_surface(X, Y, Z)

# =========================

# Equation of the circle
#    (x,y,z) = (x0, y0, z0) + cos(theta)u + sin(theta)v + t*w
# where theta varies over the interval 0 to 2pi and t ranges over the
# the set of real numbers and
# u and v are unit vectors that are (1) mutually perpendicular and (2) are perpendicular
# to the axis , w = unit vector of the chosen axis

# vector between the two points
w = c - o
# mag of vector
mag = np.linalg.norm(w)

# unit vector
w = w / mag

# make some vector not in the same direction as v
not_w = np.array([1, 0, 0])
if (w == not_w).all():
    not_w = np.array([0, 1, 0])

# make vector perpendicular to v
u = np.cross(w, not_w)
# normalize n1
u /= np.linalg.norm(u)
# make unit vector perpendicular to v and n1
v = np.cross(w, u)

# surface ranges over t from 0 to length of axis and 0 to 2*pi
t = np.linspace(0, mag, 100)
theta = np.linspace(0, 2 * np.pi, 100)
# use meshgrid to make 2d arrays
t, theta = np.meshgrid(t, theta)
# generate coordinates for surface
X, Y, Z = [o[i] + w[i] * t + R * np.sin(theta) * v[i] + R * np.cos(theta) * u[i] for i in [0, 1, 2]]
ax.plot_surface(X, Y, Z, color = 'purple')

plt.show()
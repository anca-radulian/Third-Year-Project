import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, 50)
ax.set_ylim(0, 50)
ax.set_zlim(0, 50)

# Coordinates chosen
user_x = 20
user_y = 10
user_z = 30

c = np.array([user_x, user_y, user_z])  # end
o = np.array([10, 15, 10])  # start

mid = (user_x + o[0]) /2 , (user_y + o[1]) /2, (user_z + o[2]) /2
O = np.array([0, 0, 0])
center = np.array([30, 42.5, 20])

# plot the axis of the
#ax.plot(*zip(c, O), color = 'red')
ax.plot(*zip(mid, center), color = 'red')
ax.plot(*zip(c, o), color = 'blue')

ax.scatter(mid[0], mid[1], mid[2], color = 'yellow')
ax.scatter(center[0], center[1], center[2], color = 'yellow')


ax.scatter(c[0], c[1], c[2], color = 'purple')
ax.scatter(o[0], o[1], o[2], color = 'pink')



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
#    (x,y,z) = (x0, y0, z0) + R cos(theta)u + R sin(theta)v + t*w
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
# ax.plot_surface(X, Y, Z, color = 'purple')

# ----------------------------- Arc plotting ---------------------------------------------------------------------

# Let X and W be unit vectors in the directions of A−O, and B−O respectively.
# Then let Z be the unit vector in the direction of X×W, and let Y=W×X.
# We now have an orthonormal set of vectors X,Y,Z.
# If r is the radius of the circle, then the curve can be parameterized
# P(θ)=O+(rcosθ)X+(rsinθ)Y
# You should use values of θ between zero and ϕ, where ϕ is the angle between OA and OB.
R = np.linalg.norm(c - center)

X_arc = (o - center)
Y_arc = (c - center)


alpha = np.arccos(np.clip((np.dot(X_arc, Y_arc) / (np.linalg.norm(X_arc) * np.linalg.norm(X_arc)) ), -1, 1))
cos_alpha = np.cos(alpha)
sin_alpha = np.sin(alpha)

th = np.linspace(0, alpha, 50)

x_curve, y_curve, z_curve =[center[i] + ((sin_alpha * np.cos(th) - cos_alpha * np.sin(th)) * X_arc[i] + np.sin(th) * Y_arc[i])/ sin_alpha for i in [0,1,2]]

ax.scatter(x_curve, y_curve, z_curve, color ='purple')


plt.show()
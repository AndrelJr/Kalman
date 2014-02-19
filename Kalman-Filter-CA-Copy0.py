# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# <headingcell level=1>

# Kalman Filter Implementation in Python

# <markdowncell>

# Situation covered: You have an acceleration sensor (in 2D: $\ddot x$ and $\ddot y$) and try to calculate velocity ($\dot x$ and $\dot y$) as well as position ($x$ and $y$)

# <headingcell level=2>

# State Vector - Constant Acceleration

# <markdowncell>

# Constant Acceleration Model for Ego Motion in Plane
# 
# $$x= \left[ \matrix{ x \\ y \\ \dot x \\ \dot y \\ \ddot x \\ \ddot y} \right]$$
# 

# <markdowncell>

# Formal Definition:
# 
# $$x_{k+1} = F \cdot x_{k} + B \cdot u$$
# 
# $$x_{k+1} = \begin{bmatrix}1 & 0 & \Delta t & 0 & \frac{1}{2}\Delta t^2 & 0 \\ 0 & 1 & 0 & \Delta t & 0 & \frac{1}{2}\Delta t^2 \\ 0 & 0 & 1 & 0 & \Delta t & 0 \\ 0 & 0 & 0 & 1 & 0 & \Delta t \\ 0 & 0 & 0 & 0 & 1 & 0  \\ 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix} \cdot \begin{bmatrix} x \\ y \\ \dot x \\ \dot y \\ \ddot x \\ \ddot y\end{bmatrix}_{k}$$
# 
# $$y = H \cdot x$$
# 
# $$y = \begin{bmatrix}0 & 0 & 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 & 0 & 1\end{bmatrix} \cdot x$$

# <headingcell level=4>

# Initial State

# <codecell>

x = np.matrix([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]).T
print(x, x.shape)
plt.scatter(x[0],x[1], s=100)
plt.title('Initial Location')

# <headingcell level=4>

# Initial Uncertainty

# <codecell>

P = np.matrix([[10.0, 0.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 10.0, 0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 10.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 10.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 10.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0, 10.0]])
print(P, P.shape)


# Plot between -10 and 10 with .001 steps.
xpdf = np.arange(-10, 10, 0.001)

fig = plt.figure(figsize=(8,5))
plt.subplot(231)
plt.plot(xpdf, norm.pdf(xpdf,0,P[0,0]))
plt.title('$x$')

plt.subplot(232)
plt.plot(xpdf, norm.pdf(xpdf,0,P[2,2]))
plt.title('$\dot x$')

plt.subplot(233)
plt.plot(xpdf, norm.pdf(xpdf,0,P[4,4]))
plt.title('$\ddot x$')

plt.subplot(234)
plt.plot(xpdf, norm.pdf(xpdf,0,P[1,1]))
plt.title('$y$')

plt.subplot(235)
plt.plot(xpdf, norm.pdf(xpdf,0,P[3,3]))
plt.title('$\dot y$')

plt.subplot(236)
plt.plot(xpdf, norm.pdf(xpdf,0,P[5,5]))
plt.title('$\ddot y$')



plt.tight_layout()

# <headingcell level=4>

# Dynamic Matrix

# <markdowncell>

# It is calculated from the dynamics of the Egomotion.
# 
# $$x_{k+1} = x_{k} + \dot x_{k} \cdot \Delta t +  \ddot x_k \cdot \frac{1}{2}\Delta t^2$$
# $$y_{k+1} = y_{k} + \dot y_{k} \cdot \Delta t +  \ddot y_k \cdot \frac{1}{2}\Delta t^2$$
# $$\dot x_{k+1} = \dot x_{k} + \ddot x \cdot \Delta t$$
# $$\dot y_{k+1} = \dot y_{k} + \ddot y \cdot \Delta t$$
# $$\ddot x_{k+1} = \ddot x_{k}$$
# $$\ddot y_{k+1} = \ddot y_{k}$$

# <codecell>

dt = 0.5 # Time Step between Filter Steps

F = np.matrix([[1.0, 0.0, dt, 0.0, 1/2.0*dt**2, 0.0],
              [0.0, 1.0, 0.0, dt, 0.0, 1/2.0*dt**2],
              [0.0, 0.0, 1.0, 0.0, dt, 0.0],
              [0.0, 0.0, 0.0, 1.0, 0.0, dt],
              [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
print(F, F.shape)

# <headingcell level=4>

# Measurement Matrix

# <markdowncell>

# Here you can determine, which of the states is covered by a measurement. In this example, the position ($x$ and $y$) as well as the acceleration is measured ($\ddot x$ and $\ddot y$).

# <codecell>

H = np.matrix([[0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
              [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]])
print(H, H.shape)

# <headingcell level=4>

# Measurement Noise Covariance

# <codecell>

ra = 10.0
R = np.matrix([[ra, 0.0],
               [0.0, ra]])
print(R, R.shape)

plt.subplot(121)
plt.plot(xpdf, norm.pdf(xpdf,0,R[0,0]))
plt.title('$x$')

plt.subplot(122)
plt.plot(xpdf, norm.pdf(xpdf,0,R[1,1]))
plt.title('$y$')


plt.tight_layout()

# <headingcell level=4>

# Process Noise Covariance

# <markdowncell>

# The Position of the car can be influenced by a force (e.g. wind), which leads to an acceleration disturbance (noise). This process noise has to be modeled with the process noise covariance matrix Q.
# 
# $$Q = \begin{bmatrix}\sigma_{x}^2 & \sigma_{xy} & \sigma_{x \dot x} & \sigma_{x \dot y} & \sigma_{x \ddot x} & \sigma_{x \ddot y} \\ \sigma_{yx} & \sigma_{y}^2 & \sigma_{y \dot x} & \sigma_{y \dot y} & \sigma_{y \ddot x} & \sigma_{y \ddot y} \\ \sigma_{\dot x x} & \sigma_{\dot x y} & \sigma_{\dot x}^2 & \sigma_{\dot x \dot y} & \sigma_{\dot x \ddot x} & \sigma_{\dot x \ddot y} \\ \sigma_{\dot y x} & \sigma_{\dot y y} & \sigma_{\dot y \dot x} & \sigma_{\dot y}^2 & \sigma_{\dot y \ddot x} & \sigma_{\dot y \ddot y} \\ \sigma_{\ddot x x} & \sigma_{\ddot x y} & \sigma_{\ddot x \dot x} & \sigma_{\ddot x \dot y} & \sigma_{\ddot x}^2 & \sigma_{\ddot x \ddot y} \\ \sigma_{\ddot y x} & \sigma_{\ddot y y} & \sigma_{\ddot y \dot x} & \sigma_{\ddot y \dot y} & \sigma_{\ddot y \ddot x} & \sigma_{\ddot y}^2\end{bmatrix}$$
# 
# Referring to [Schubert, R., Adam, C., Obst, M., Mattern, N., Leonhardt, V., & Wanielik, G. (2011). Empirical evaluation of vehicular models for ego motion estimation. 2011 IEEE Intelligent Vehicles Symposium (IV), 534–539. doi:10.1109/IVS.2011.5940526], the standard deviation for acceleration process noise can be assumed with $8.8 \frac{m}{s^2}$.
# 
# To easily calcualte Q, one can ask the question: How the noise effects my state vector? For example, how the acceleration change the position over one timestep dt.
# 
# This leads to the equation $dx = \frac{1}{2}dt^2 \cdot a_n$ with $a_n$ as the noisy acceleration. The velocity is influenced with $d\dot x = dt \cdot a_n$ and the acceleration is influenced by the acceleration with factor $1.0$.

# <codecell>

sa = 0.5
G = np.matrix([[1/2.0*dt**2],
               [1/2.0*dt**2],
               [dt],
               [dt],
               [1.0],
               [1.0]])
Q = G*G.T*sa**2

print(Q, Q.shape)


fig = plt.figure(figsize=(8,5))

plt.subplot(231)
plt.plot(xpdf, norm.pdf(xpdf,0,Q[0,0]))
plt.title('$x$')

plt.subplot(232)
plt.plot(xpdf, norm.pdf(xpdf,0,Q[2,2]))
plt.title('$\dot x$')

plt.subplot(233)
plt.plot(xpdf, norm.pdf(xpdf,0,Q[4,4]))
plt.title('$\ddot x$')

plt.subplot(234)
plt.plot(xpdf, norm.pdf(xpdf,0,Q[1,1]))
plt.title('$y$')

plt.subplot(235)
plt.plot(xpdf, norm.pdf(xpdf,0,Q[3,3]))
plt.title('$\dot y$')

plt.subplot(236)
plt.plot(xpdf, norm.pdf(xpdf,0,Q[5,5]))
plt.title('$\ddot y$')

plt.tight_layout()

# <headingcell level=4>

# Identity Matrix

# <codecell>

I = np.eye(6)
print(I, I.shape)

# <headingcell level=2>

# Measurement

# <codecell>

m = 500 # Measurements

# Acceleration
sa= 0.1 # Sigma for acceleration
ax= 0.0 # in X
ay= 0.0 # in Y

mx = np.array(ax+sa*np.random.randn(m))
my = np.array(ay+sa*np.random.randn(m))

measurements = np.vstack((mx,my))

print(measurements.shape)

# <codecell>

fig = plt.figure(figsize=(16,9))
plt.step(range(m),mx, label='$a_x$')
plt.step(range(m),my, label='$a_y$')
plt.ylabel('Acceleration')
plt.title('Measurements')
plt.legend(loc='best',prop={'size':18})

# <codecell>

# Preallocation for Plotting
xt = []
yt = []
dxt= []
dyt= []
ddxt=[]
ddyt=[]
Zx = []
Zy = []
Px = []
Py = []
Pdx= []
Pdy= []
Pddx=[]
Pddy=[]
Kx = []
Ky = []
Kdx= []
Kdy= []
Kddx=[]
Kddy=[]

# <headingcell level=2>

# Kalman Filter

# <markdowncell>

# ![Kalman Filter](http://bilgin.esme.org/portals/0/images/kalman/iteration_steps.gif)

# <codecell>

for n in range(len(measurements[0])):
    
    # Measurement Update (Correction)
    # ===============================
    # Compute the Kalman Gain
    S = H*P*H.T + R
    K = (P*H.T) * np.linalg.pinv(S)

    
    # Update the estimate via z
    Z = measurements[:,n].reshape(2,1)
    y = Z - (H*x)                            # Innovation or Residual
    x = x + (K*y)
    
    # Update the error covariance
    P = (I - (K*H))*P

    # Time Update (Prediction)
    # ========================
    # Project the state ahead
    x = F*x
    
    # Project the error covariance ahead
    P = F*P*F.T + Q
    
    
    # Save states for Plotting
    xt.append(float(x[0]))
    yt.append(float(x[1]))
    dxt.append(float(x[2]))
    dyt.append(float(x[3]))
    ddxt.append(float(x[4]))
    ddyt.append(float(x[5]))
    Zx.append(float(Z[0]))
    Zy.append(float(Z[1]))
    Px.append(float(P[0,0]))
    Py.append(float(P[1,1]))
    Pdx.append(float(P[2,2]))
    Pdy.append(float(P[3,3]))
    Pddx.append(float(P[4,4]))
    Pddy.append(float(P[5,5]))
    Kx.append(float(K[0,0]))
    Ky.append(float(K[1,0]))
    Kdx.append(float(K[2,0]))
    Kdy.append(float(K[3,0]))
    Kddx.append(float(K[4,0]))
    Kddy.append(float(K[5,0]))

# <codecell>


# <headingcell level=2>

# Plots

# <headingcell level=3>

# Unsicherheiten

# <codecell>

fig = plt.figure(figsize=(16,4))
#plt.plot(range(len(measurements[0])),Px, label='$x$')
#plt.plot(range(len(measurements[0])),Py, label='$y$')
plt.plot(range(len(measurements[0])),Pddx, label='$\ddot x$')
plt.plot(range(len(measurements[0])),Pddy, label='$\ddot y$')

plt.xlabel('Filter Step')
plt.ylabel('')
plt.title('Uncertainty (Elements from Matrix $P$)')
plt.legend(loc='best',prop={'size':22})

# <headingcell level=3>

# Kalman Gains

# <codecell>

fig = plt.figure(figsize=(16,4))
plt.plot(range(len(measurements[0])),Kx, label='Kalman Gain for $x$')
plt.plot(range(len(measurements[0])),Ky, label='Kalman Gain for $y$')
plt.plot(range(len(measurements[0])),Kdx, label='Kalman Gain for $\dot x$')
plt.plot(range(len(measurements[0])),Kdy, label='Kalman Gain for $\dot y$')
plt.plot(range(len(measurements[0])),Kddx, label='Kalman Gain for $\ddot x$')
plt.plot(range(len(measurements[0])),Kddy, label='Kalman Gain for $\ddot y$')

plt.xlabel('Filter Step')
plt.ylabel('')
plt.title('Kalman Gain (the lower, the more the measurement fullfill the prediction)')
plt.legend(loc='best',prop={'size':18})

# <headingcell level=3>

# Covariance Matrix

# <codecell>

fig = plt.figure(figsize=(5, 5))
im = plt.imshow(P, interpolation="none")
plt.title('Covariance Matrix $P$')
ylocs, ylabels = yticks()
# set the locations of the yticks
yticks(arange(7))
# set the locations and labels of the yticks
yticks(arange(6),('$x$', '$y$', '$\dot x$', '$\dot y$', '$\ddot x$', '$\ddot y$'), fontsize=22)

xlocs, xlabels = xticks()
# set the locations of the yticks
xticks(arange(7))
# set the locations and labels of the yticks
xticks(arange(6),('$x$', '$y$', '$\dot x$', '$\dot y$', '$\ddot x$', '$\ddot y$'), fontsize=22)

plt.xlim([-0.5,5.5])
plt.ylim([5.5, -0.5])

from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", "5%", pad="3%")
plt.colorbar(im, cax=cax)


plt.tight_layout()

# <codecell>

fig = plt.figure(figsize=(16,9))

plt.subplot(311)
plt.step(range(len(measurements[0])),ddxt, label='$\ddot x$')
plt.step(range(len(measurements[0])),ddyt, label='$\ddot y$')

plt.title('Estimate (Elements from State Vector $x$)')
plt.legend(loc='best',prop={'size':22})
plt.ylabel('Acceleration')
plt.ylim([-1,1])

plt.subplot(312)
plt.step(range(len(measurements[0])),dxt, label='$\dot x$')
plt.step(range(len(measurements[0])),dyt, label='$\dot y$')

plt.ylabel('')
plt.legend(loc='best',prop={'size':22})
plt.ylabel('Velocity')
           
plt.subplot(313)
plt.step(range(len(measurements[0])),xt, label='$x$')
plt.step(range(len(measurements[0])),yt, label='$y$')

plt.xlabel('Filter Step')
plt.ylabel('')
plt.legend(loc='best',prop={'size':22})
plt.ylabel('Position')

# <codecell>

fig = plt.figure(figsize=(16,16))
plt.scatter(xt,yt, s=20, label='State', c='k')
plt.scatter(xt[0],yt[0], s=100, label='Start', c='g')
plt.scatter(xt[-1],yt[-1], s=100, label='Goal', c='r')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Position')
plt.legend(loc='best')
axis('equal')

# <headingcell level=1>

# Conclusion

# <markdowncell>


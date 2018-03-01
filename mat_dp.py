"""
A Python script defining a class that represents a double pendulum object and
calculates its trajectory over a given time with a given time delta, and then
animates this using matplotlib.
"""

# note from Izaak van Dongen: This was originally found at
# https://matplotlib.org/examples/animation/double_pendulum_animated.html and
# was then adapted to be able to draw multiple pendulums, and the paths each
# pendulum takes.

# Double pendulum formula translated from the C code at
# http://www.physics.usyd.edu.au/~wheat/dpend_html/solve_dpend.c

import argparse
import datetime

from numpy import sin, cos
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation

from itertools import chain

DT = 0.03
TRAIL_WIDTH = 1
PEND_WIDTH = 2

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--formats", nargs="*", type=str, default=[],
                        help="file formats to write to. None if not included.")
    return parser.parse_args()

def join_mat_funcs(*funcs):
    return lambda *args: tuple(chain.from_iterable(f(*args) for f in funcs))

class Pendulum:
    def __init__(self, G, L1, L2, M1, M2, dt, th1, w1, th2, w2, ax):
        self.G = G        # acceleration due to gravity, in m/s^2
        self.L1 = L1      # length of pendulum 1 in m
        self.L2 = L2      # length of pendulum 2 in m
        self.M1 = M1      # mass of pendulum 1 in kg
        self.M2 = M2      # mass of pendulum 2 in kg
        self.dt = dt      # time delta
        self.th1 = th1    # initial angle 1 in degrees
        self.w1 = w1      # initial angular velocity 1 in degrees
        self.th2 = th2    # initial angle 2 in degrees
        self.w2 = w2      # initial angular velocity 2 in degrees

        # initial state
        self.state = np.radians([th1, w1, th2, w2])
        # create the time array
        self.t = np.arange(0.0, 20, dt)
        # integrate your ODE using scipy.integrate.
        self.y = integrate.odeint(self.derivs, self.state, self.t)

        self.x1 =  L1*sin(self.y[:, 0])
        self.y1 = -L1*cos(self.y[:, 0])
        self.x2 =  L2*sin(self.y[:, 2]) + self.x1
        self.y2 = -L2*cos(self.y[:, 2]) + self.y1

        self.ax = ax
        self.ax.grid()

        self.line, = self.ax.plot([], [], 'o-', c="#0000FF", lw=PEND_WIDTH)
        self.inner_trail, = self.ax.plot([], [], c="#B80000", lw=TRAIL_WIDTH)
        self.outer_trail, = self.ax.plot([], [], c="#6600FF", lw=TRAIL_WIDTH)
        self.time_template = 'time = %.1fs'
        self.time_text = self.ax.text(0.05, 0.9, '', transform=self.ax.transAxes)

    def animate(self, i):
        self.line.set_data([0, self.x1[i], self.x2[i]],
                           [0, self.y1[i], self.y2[i]])
        self.inner_trail.set_data(self.x1[:i + 1], self.y1[:i + 1])
        self.outer_trail.set_data(self.x2[:i + 1], self.y2[:i + 1])
        self.time_text.set_text(self.time_template % (i*self.dt))

        return self.line, self.time_text, self.inner_trail, self.outer_trail

    def init(self):
        self.line.set_data([], [])
        self.time_text.set_text('')
        self.inner_trail.set_data([], [])
        self.outer_trail.set_data([], [])
        return self.line, self.time_text, self.inner_trail, self.outer_trail

    def serialise_parameters(self):
        return "_".join(map("{:.1e}".format,
                        (self.G, self.L1, self.L2, self.M1, self.M2, self.dt,
                         self.th1, self.w1, self.th2, self.w2)))

    def derivs(self, state, t):
        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        del_ = state[2] - state[0]
        den1 = (self.M1 + self.M2)*self.L1 - self.M2*self.L1*cos(del_)*cos(del_)
        dydx[1] = (self.M2*self.L1*state[1]*state[1]*sin(del_)*cos(del_) +
                   self.M2*self.G*sin(state[2])*cos(del_) +
                   self.M2*self.L2*state[3]*state[3]*sin(del_) -
                   (self.M1 + self.M2)*self.G*sin(state[0]))/den1

        dydx[2] = state[3]

        den2 = (self.L2/self.L1)*den1
        dydx[3] = (-self.M2*self.L2*state[3]*state[3]*sin(del_)*cos(del_) +
                   (self.M1 + self.M2)*self.G*sin(state[0])*cos(del_) -
                   (self.M1 + self.M2)*self.L1*state[1]*state[1]*sin(del_) -
                   (self.M1 + self.M2)*self.G*sin(state[2]))/den2

        return dydx

if __name__ == "__main__":
    args = get_args()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 6))

    for ax in (ax1, ax2):
        ax.set_xlim((-2, 2))
        ax.set_ylim((-2, 2))
        ax.set_aspect("equal")

    pend1 = Pendulum(G=9.8, L1=1.0, L2=1.0, M1=1.0, M2=1.0, dt=DT,
                     th1=120.0, w1=0.01, th2=-10.0, w2=0.0, ax=ax1)
    pend2 = Pendulum(G=9.8, L1=1.0, L2=1.0, M1=1.0, M2=1.0, dt=DT,
                     th1=130.0, w1=0.01, th2=-10.0, w2=0.0, ax=ax2)

    ani = animation.FuncAnimation(fig,
                                  join_mat_funcs(pend1.animate, pend2.animate),
                                  np.arange(1, len(pend1.y)),
                                  interval=25, blit=True,
                                  init_func=join_mat_funcs(pend1.init, pend2.init))

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()

    file_base = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    print("file base is {!r}".format(file_base))

    for file_format in args.formats:
        file_name = "{}.{}".format(file_base, file_format)
        print("saving animation to file {!r}.. this may take a while".format(file_name))
        ani.save(file_name, fps=1 / DT)
        print("saved, displaying animation")

    plt.show()

#!/usr/bin/env python2
#^ shebang fixes syntax highlighting in vim

# Maths taken from Daniel Shiffman's project/video:
# https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_93_DoublePendulum/CC_93_DoublePendulum.pde
# https://www.youtube.com/watch?v=uWzPe_S-RVE

"""
A now *iterative* model of a double pendulum in Processing.
"""

from pde_pendulum import DoublePendulum

FPS = 60
DT = 1.0 / FPS

FRICTION = 1

def setup():
    global pend1, pend2
    size(720, 480)
    frameRate(FPS)
    imageMode(CORNER)
    pend1 = DoublePendulum(G=9.8, L1=2, L2=1.5, M1=1, M2=1, dt=DT,
                           th1=120.0, w1=-50, th2=-10.0, w2=-50,
                           cx=width / 4, cy=height / 2, friction=FRICTION,
                           p_col=color(0, 0, 255), t_col=color(0x66, 0, 255))
    pend2 = DoublePendulum(G=9.8, L1=2, L2=1.5, M1=1, M2=1, dt=DT,
                           th1=130.0, w1=-50, th2=-10.0, w2=-50,
                           cx=3 * width / 4, cy=height / 2, friction=FRICTION,
                           p_col=color(220, 220, 0), t_col=color(255, 70, 0))
def draw():
    background(230)
    pend1.update()
    pend2.update()
    pend1.draw()
    pend2.draw()
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

FRICTION = 0.995

def setup():
    global pend1
    size(800, 800)
    frameRate(FPS)
    imageMode(CORNER)
    pend1 = DoublePendulum(G=9.8, L1=150, L2=150, M1=10, M2=10, dt=DT,
                           th1=120.0, w1=0.01, th2=-10.0, w2=0.0,
                           cx=width / 2, cy=height / 2, friction=FRICTION)

def draw():
    background(0)
    pend1.update()
    pend1.draw()
    print(frameRate)
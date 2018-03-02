L_SCALE = 50
M_SCALE = 20

class DoublePendulum(object):
    __slots__ = "G L1 L2 M1 M2 dt th1 w1 th2 w2 canvas x1 y1 x2 y2 px1 py1 px2 py2 cx cy friction p_col t_col".split()

    def __init__(self, G, L1, L2, M1, M2, dt, th1, w1, th2, w2, cx, cy, friction, p_col, t_col):
        self.G   = G       # acceleration due to gravity, in m/s^2
        self.L1  = L1      # length of pendulum 1 in m
        self.L2  = L2      # length of pendulum 2 in m
        self.M1  = M1      # mass of pendulum 1 in kg
        self.M2  = M2      # mass of pendulum 2 in kg
        self.dt  = dt      # time delta in s
        self.th1 = radians(th1)     # initial angle 1 in degrees
        self.w1  = radians(w1 )     # initial angular velocity 1 in degrees
        self.th2 = radians(th2)     # initial angle 2 in degrees
        self.w2  = radians(w2 )     # initial angular velocity 2 in degrees
        self.cx = cx       # centre x
        self.cy = cy       # centre y
        self.friction = friction ** dt # friction scalar
        self.p_col = p_col
        self.t_col = t_col

        # canvas to draw the trail on
        self.canvas = createGraphics(width, height)
        # calculate bob coordinates
        self.calculate_coords()
        # previous co-ordinates, used to draw the trail
        self.px1, self.py1, self.px2, self.py2 = self.x1, self.y1, self.x2, self.y2

    def calculate_coords(self):
        self.x1 = self.cx + self.L1 * sin(self.th1) * L_SCALE
        self.y1 = self.cy + self.L1 * cos(self.th1) * L_SCALE
        self.x2 = self.x1 + self.L2 * sin(self.th2) * L_SCALE
        self.y2 = self.y1 + self.L2 * cos(self.th2) * L_SCALE

    def draw(self):
        image(self.canvas, 0, 0, width, height)
        stroke(self.p_col)
        strokeWeight(2)
        fill(self.p_col)
        line(self.cx, self.cy, self.x1, self.y1)
        ellipse(self.x1, self.y1, self.M1 * M_SCALE, self.M1 * M_SCALE)
        line(self.x1, self.y1, self.x2, self.y2)
        ellipse(self.x2, self.y2, self.M2 * M_SCALE, self.M2 * M_SCALE)

    def update(self):
        w1p = ((-self.G * (2 * self.M1 + self.M2) * sin(self.th1) +
                     -self.M2 * self.G * sin(self.th1-2*self.th2) +
                    (-2*sin(self.th1-self.th2)*self.M2 * 
                     (self.w2*self.w2*self.L2+self.w1*self.w1*self.L1*cos(self.th1-self.th2)))) /
                     (self.L1 * (2*self.M1+self.M2-self.M2*cos(2*self.th1-2*self.th2))))

        w2p = (2 * sin(self.th1-self.th2) *
                  ((self.w1*self.w1*self.L1*(self.M1+self.M2)) +
                    self.G * (self.M1 + self.M2) * cos(self.th1) +
                    self.w2*self.w2*self.L2*self.M2*cos(self.th1-self.th2)) /
                   (self.L2 * (2*self.M1+self.M2-self.M2*cos(2*self.th1-2*self.th2))))

        self.w1 += w1p * self.dt
        self.w2 += w2p * self.dt
        self.th1 += self.w1 * self.dt
        self.th2 += self.w2 * self.dt

        self.w1 *= self.friction
        self.w2 *= self.friction

        self.calculate_coords()

        self.canvas.beginDraw()
        self.canvas.stroke(self.t_col)
        self.canvas.line(self.px2, self.py2, self.x2, self.y2)
        self.canvas.endDraw()

        self.px1 = self.x1
        self.py1 = self.y1
        self.px2 = self.x2
        self.py2 = self.y2
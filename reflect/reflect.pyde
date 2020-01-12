from random import randint

# http://paulbourke.net/geometry/pointlineplane/
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
# https://math.stackexchange.com/questions/12745/how-do-you-calculate-the-unit-vector-between-two-points
# http://www.jeffreythompson.org/collision-detection/line-point.php

w = 1000
h = 1000

def dist_point_to_line(p1, p2, p3): 
    # The numerator is twice the area of the triangle with its vertices at the three points, (x0,y0), P1 and P2.
    # The denominator of this expression is the distance between P1 and P2.
    d = abs((p2.y - p1.y) * p3.x - (p2.x - p1.x) * p3.y + p2.x * p1.y - p2.y * p1.x) / p2.dist(p1)
    u = ((p3.x - p1.x) * (p2.x - p1.x) + (p3.y - p1.y) * (p2.y - p1.y)) / (p1.dist(p2) ** 2)
    x = p1.x + u * (p2.x - p1.x)
    y = p1.y + u * (p2.y - p1.y)
    return u, d, PVector(x, y) 

class Ball(object):
    def __init__(self, pos, vel, acc, ext):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.ext = ext
    
    def move(self):
        self.vel.add(self.acc);
        self.pos.add(self.vel);
    
    def draw(self):
        r = self.ext / 2
        f1 = self.pos
        f2 = f1 + self.vel * self.ext
        line(f1.x, f1.y, f2.x, f2.y)
        circle(self.pos.x, self.pos.y, self.ext)

class Mirror(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def draw(self):
        line(self.p1.x, self.p1.y, self.p2.x, self.p2.y)


ball = Ball(PVector(w/4, h/2), PVector(4, -0.75), PVector(0, 0), 10)
mirrors = []

click1 = 0
def mousePressed():
    global click1, mirrors
    if mouseButton == LEFT:
        click1 = PVector(mouseX, mouseY)
    elif mouseButton == RIGHT:
        click2 = PVector(mouseX, mouseY)
        click1, click2 = (click1, click2) if click1.x < click2.x else (click2, click1)
        mirrors.append(Mirror(click1, click2))

def setup():
    frameRate(60)
    size(w, h)
    colorMode(RGB)
    background(0, 0, 0)
    noFill()
    stroke(255, 255, 255)

def draw():
    # clear()

    ball.draw()
    for mirr in mirrors:
        mirr.draw()
    
    if keyPressed:
        if key == CODED:
            if keyCode == LEFT:
                ball.vel.rotate(-radians(5))
            elif keyCode == RIGHT:
                ball.vel.rotate(radians(5))
        elif key == " ":
            ball.pos = PVector(w / 2, h / 2)
            
    ball.move()
    
        if ball.pos.x < 0:
        ball.pos.x = w
    elif ball.pos.x > w:
        ball.pos.x = 0
    
    for mirr in mirrors:
        u, d, p = dist_point_to_line(mirr.p1, mirr.p2, ball.pos)
        if d <= ball.ext / 2 and mirr.p1.x < ball.pos.x < mirr.p2.x:
            a, b = ball.vel, mirr.p2 - mirr.p1
            print(u, d, p)
            circle(p.x, p.y, 10)
            line(p.x, p.y, ball.pos.x, ball.pos.y)
            n = (ball.pos - p).normalize()
            d = ball.vel
            ball.pos.add(n * (ball.ext / 2))
            ball.vel = d - 2 * (d.dot(n)) * n

    
    
    
    

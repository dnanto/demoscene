from random import randint

# http://paulbourke.net/geometry/pointlineplane/
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
# https://math.stackexchange.com/questions/12745/how-do-you-calculate-the-unit-vector-between-two-points
# http://www.jeffreythompson.org/collision-detection/line-point.php
# https://en.wikipedia.org/wiki/Specular_reflection#Vector_formulation
# https://math.stackexchange.com/a/13263

w = 1000
h = 1000

def point_line_dist(p1, p2, p3): 
    # The numerator is twice the area of the triangle with its vertices at the three points, (x0,y0), P1 and P2.
    # The denominator of this expression is the distance between P1 and P2.
    return abs((p2.y - p1.y) * p3.x - (p2.x - p1.x) * p3.y + p2.x * p1.y - p2.y * p1.x) / p2.dist(p1)

def point_line_intr(p1, p2, p3):
    u = ((p3.x - p1.x) * (p2.x - p1.x) + (p3.y - p1.y) * (p2.y - p1.y)) / (p1.dist(p2) ** 2)
    return PVector(p1.x + u * (p2.x - p1.x), p1.y + u * (p2.y - p1.y)) 

def specular_reflection(d, n):
    return d - 2 * (d.dot(n)) * n

def circle_segment_collision(circ, segm):
    dst = point_line_dist(segm.p1, segm.p2, circ.pos)
    pnt = point_line_intr(segm.p1, segm.p2, circ.pos)
    if dst <= circ.ext / 2 and (segm.p1.x < circ.pos.x < segm.p2.x or segm.p1.y < circ.pos.y < segm.p2.y):
        circle(pnt.x, pnt.y, 10)
        line(pnt.x, pnt.y, circ.pos.x, circ.pos.y)
        # collision normal
        n = (circ.pos - pnt).normalize()
        # move circle back to minimum collision distance
        circ.pos.add(n * (circ.ext / 2))
        # specular reflection
        circ.vel = specular_reflection(Circle.vel, n)

class Circle(object):
    def __init__(self, pos, vel, acc, ext):
        self.pos = pos
        self.vel = vel
        self.acc = acc
        self.ext = ext
    
    def move(self):
        self.vel.add(self.acc);
        self.pos.add(self.vel);
    
    def collide(self, other):
        if isinstance(other, Segment):
            pass
    
    def draw(self):
        r = self.ext / 2
        f1 = self.pos
        f2 = f1 + self.vel * self.ext / 2
        line(f1.x, f1.y, f2.x, f2.y)
        circle(self.pos.x, self.pos.y, self.ext)

class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self):
        line(self.p1.x, self.p1.y, self.p2.x, self.p2.y)


ball = Circle(PVector(w/2, h/2), PVector(2, 0), PVector(0, 0), 10)
segments = []

click1 = 0
def mousePressed():
    global click1, Segments
    if mouseButton == LEFT:
        click1 = PVector(mouseX, mouseY)
    elif mouseButton == RIGHT:
        click2 = PVector(mouseX, mouseY)
        click1, click2 = (click1, click2) if click1.x < click2.x else (click2, click1)
        segments.append(Segment(click1, click2))

def setup():
    frameRate(60)
    size(w, h)
    colorMode(RGB)
    background(0, 0, 0)
    noFill()
    stroke(255, 255, 255)

def draw():
    clear()

    # draw
    ball.draw()
    for segm in Segments:
        segm.draw()
    
    # ui
    if keyPressed:
        if key == CODED:
            if keyCode == LEFT:
                ball.vel.rotate(-radians(5))
            elif keyCode == RIGHT:
                ball.vel.rotate(radians(5))
        elif key == " ":
            ball.pos = PVector(w / 2, h / 2)
    
    # move
    ball.move()
    
    # collision detection
    for segm in segments:
        pass

    # toroidal world
    if ball.pos.x < 0:
        ball.pos.x = w
    elif ball.pos.x > w:
        ball.pos.x = 0
    elif ball.pos.y < 0:
        ball.pos.y = h
    elif ball.pos.y > h:
        ball.pos.y = 0
    
    

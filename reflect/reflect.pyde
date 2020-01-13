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

def circle_segment_collision(crc, seg):
    dst = point_line_dist(seg.p1, seg.p2, crc.pos)
    pnt = point_line_intr(seg.p1, seg.p2, crc.pos)
    if dst <= crc.ext / 2 and (seg.p1.x < crc.pos.x < seg.p2.x or seg.p1.y < crc.pos.y < seg.p2.y):
        circle(pnt.x, pnt.y, 10)
        line(pnt.x, pnt.y, crc.pos.x, crc.pos.y)
        # collision normal
        n = (crc.pos - pnt).normalize()
        # move circle back to minimum collision distance
        crc.pos.add(n * (crc.ext / 2))
        # specular reflection
        crc.vel = specular_reflection(crc.vel, n)

def circle_square_collision(crc, sqr):
    for seg in sqr.sides:
        circle_segment_collision(crc, seg)

class Circle(object):
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
        f2 = f1 + self.vel * self.ext / 2
        line(f1.x, f1.y, f2.x, f2.y)
        circle(self.pos.x, self.pos.y, self.ext)

class Square(object):
    def __init__(self, pos, ext):
        x, y = pos.x, pos.y
        self.pos = pos
        self.ext = ext
        self.col = (0, 0, 0)
        self.sides = [
            Segment(PVector(x, y), PVector(x + ext, y)),
            Segment(PVector(x + ext, y), PVector(x + ext, y + ext)),
            Segment(PVector(x, y), PVector(x, y + ext)),
            Segment(PVector(x, y + ext), PVector(x + ext, y + ext))
        ]
    
    def draw(self):
        fill(*self.col)
        square(self.pos.x, self.pos.x, self.ext)
        noFill()

class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self):
        line(self.p1.x, self.p1.y, self.p2.x, self.p2.y)

crc = Circle(PVector(w/2, h/2), PVector(2, 0), PVector(0, 0), 10)
sqr = Square(PVector(w/3, h/3), 500)
segs = []

click1 = 0
def mousePressed():
    global click1, Segments
    if mouseButton == LEFT:
        click1 = PVector(mouseX, mouseY)
    elif mouseButton == RIGHT:
        click2 = PVector(mouseX, mouseY)
        click1, click2 = (click1, click2) if click1.x < click2.x else (click2, click1)
        segs.append(Segment(click1, click2))

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
    sqr.draw()
    for seg in segs:
        seg.draw()
    crc.draw()
    
    # ui
    if keyPressed:
        if key == CODED:
            if keyCode == LEFT:
                crc.vel.rotate(-radians(5))
            elif keyCode == RIGHT:
                crc.vel.rotate(radians(5))
        elif key == " ":
            crc.pos = PVector(w / 2, h / 2)
    
    # move
    crc.move()
    
    # collision detection
    circle_square_collision(crc, sqr)
    for seg in segs:
        circle_segment_collision(crc, seg)

    # toroidal world
    if crc.pos.x < 0:
        crc.pos.x = w
    elif crc.pos.x > w:
        crc.pos.x = 0
    elif crc.pos.y < 0:
        crc.pos.y = h
    elif crc.pos.y > h:
        crc.pos.y = 0
    
    

from random import randint

class Circle(object):

    def __init__(self, x, y, r, col=(255, 255, 255)):
        self.x, self.y, self.r = x, y, r
        self.col = col

    def __repr__(self):
        return str((self.x, self.y))

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def draw(self):
        r, g, b = self.col
        fill(r, g, b)
        circle(self.x, self.y, self.r)
        noFill()

class Bounds(object):

    def __init__(self, x, y, w, h):
        self.x1, self.y1, self.w, self.h = x, y, w, h
        self.x2, self.y2 = x + w, y + h

    def __repr__(self):
        return str(self.points())

    def __contains__(self, ele):
        return self.x1 <= ele.x <= self.x2 and self.y1 <= ele.y <= self.y2

    def points(self):
        return self.x1, self.y1, self.x2, self.y2

    def intersects(self, bounds):
        return not (self.x2 < bounds.x1 or bounds.x2 < self.x1 or self.y2 < bounds.y1 or bounds.y2 < self.y1)

    def draw(self, color=(255, 255, 255)):
        noFill()
        stroke(*color)
        rect(self.x1, self.y1, self.w, self.h)

class QuadTree(object):

    def __init__(self, bounds, n, lvl=0, lab="root"):
        self.bounds = bounds

        self.n = n

        self.lvl = lvl
        self.lab = lab

        self.elements = []
        self.nw, self.ne, self.se, self.sw = None, None, None, None
        self.subdivided = False

    def subtrees(self):
        return self.nw, self.ne, self.se, self.sw

    def subdivide(self):
        x, y, w, h = self.bounds.x1, self.bounds.y1, self.bounds.w / 2.0, self.bounds.h / 2.0
        self.nw = QuadTree(Bounds(x, y, w, h), self.n, self.lvl + 1, "nw")
        self.ne = QuadTree(Bounds(x + w, y, w, h), self.n, self.lvl + 1, "ne")
        self.se = QuadTree(Bounds(x + w, y + h, w, h), self.n, self.lvl + 1, "se")
        self.sw = QuadTree(Bounds(x, y + h, w, h), self.n, self.lvl + 1, "sw")

        self.subdivided = True
        
        self.elements, elements = [], self.elements
        for ele in elements:
            tree.insert(ele)

    def insert(self, ele):
        if not ele in self.bounds:
            return False

        if not self.subdivided and len(self.elements) < self.n:
            ele.col = col[self.lab]
            self.elements.append(ele)
            return True

        if not self.subdivided:
            self.subdivide()

        for tree in self.subtrees():
            if tree.insert(ele):
                return True

    def query(self, bounds):
        if self.bounds.intersects(bounds):
            for ele in self.elements:
                if ele in bounds:
                    yield ele

            for tree in filter(None, self.subtrees()):
                for ele in tree.query(bounds):
                    yield ele

    def all(self):
        for ele in self.elements:
            yield ele
        for tree in filter(None, self.subtrees()):
            for ele in tree.all():
                yield ele

    def draw(self):
        self.bounds.draw()
        for tree in filter(None, self.subtrees()):
            tree.draw()

    def pprint(self):
        print(self.lvl * '\t' + self.lab)
        for ele in self.elements:
            print(self.lvl * '\t' + len(self.lab) * " " + "\t" + str(ele.x) + ", " + str(ele.y))
        for tree in filter(None, self.subtrees()):
            tree.pprint()

col = {
    "root": (255, 255, 255),
    "nw": (255, 0, 0),
    "ne": (0, 255, 0),
    "se": (0, 0, 255),
    "sw": (200, 200, 200)
}

w = 1000
h = 1000
n = 1
r = 2

drag = None
release = None

b = Bounds(0, 0, w, h)
tree = QuadTree(b, n)
circles = {Circle(randint(0, w), randint(0, h), r) for _ in range(10000)}
for ele in circles:
    tree.insert(ele)

n1, n2, n3 = len(circles), sum(1 for _ in tree.query(b)), sum(1 for _ in tree.all())
print(n1, n2, n3)
assert n1 == n2 == n3

def setup():
    frameRate(60)
    size(w, h)
    colorMode(RGB)
    background(0, 0, 0)

def draw():
    clear()

    noFill()
    stroke(255, 255, 255)
    tree.draw()
    noStroke()

    for ele in circles:
        ele.draw()

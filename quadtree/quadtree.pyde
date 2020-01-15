from random import randint

# https://en.wikipedia.org/wiki/Quadtree

col = {
    "root": (255, 255, 255),
    "nw": (255, 0, 0),
    "ne": (0, 255, 0),
    "se": (0, 0, 255),
    "sw": (200, 200, 200) 
}

class Circle(object):
    def __init__(self, x, y, r, col=(255, 255, 255)):
        self.x, self.y, self.r = x, y, r
        self.col = col
    def draw(self):
        r, g, b = self.col
        fill(r, g, b)
        circle(self.x, self.y, self.r)
        noFill()

class QuadTree(object):
    def __init__(self, x, y, w, h, n, lvl=0, lab="root"):
        self.lvl, self.lab = lvl, lab
        self.n = n
        self.x, self.y, self.w, self.h = x, y, w, h
        self.x1, self.y1, self.x2, self.y2 = x, y, x + w, y + h
        self.points = []
        self.nw, self.ne, self.se, self. sw = None, None, None, None
    
    def __repr__(self):
        return str((self.lvl, self.lab, len(self.points), self.x, self.y, self.x + self.w, self.y + self.h))
    
    def subdivide(self):
        lvl = self.lvl + 1
        w, h = self.w / 2, self.h / 2
        self.nw = QuadTree(self.x, self.y, w, h, self.n, lvl, "nw")
        self.ne = QuadTree(self.x + w, self.y, w, h, self.n, lvl, "ne")
        self.se = QuadTree(self.x + w, self.y + h, w, h, self.n, lvl, "se")
        self.sw = QuadTree(self.x, self.y + h, w, h, self.n, lvl, "sw")
        
        for obj in self.points:
            for tree in (self.nw, self.ne, self.se, self.sw):
                tree.insert(obj)
        
        self.points = []
    
    def insert(self, obj):
        x, y = obj if isinstance(obj, tuple) else (obj.x, obj.y)
        
        if self.x1 < x < self.x2 and self.y1 < y < self.y2:
            if not self.nw:
                if len(self.points) < self.n:
                    obj.col = col[self.lab]
                    self.points.append(obj)
                    return True
                
                self.subdivide()
            
            for tree in (self.nw, self.ne, self.se, self.sw):
                if tree.insert(obj):
                    return True
        
        return False
    
    def draw(self, node="root", lvl=0):
        print(self)
        rect(self.x, self.y, self.w, self.h)
        lvl += 1
        if self.nw:
            self.nw.draw("nw", lvl)
        if self.ne:
            self.ne.draw("ne", lvl)
        if self.se:
            self.se.draw("se", lvl)
        if self.sw:
            self.sw.draw("sw", lvl)

w = 1000
h = 1000
n = 100
r = 10

def setup():
    frameRate(60)
    size(w, h)
    colorMode(RGB)
    background(0, 0, 0)
    
def draw():
    if (frameCount - 1) % (60 * 2) == 0:
        clear()
        
        circles = [Circle(randint(0, w), randint(0, h), r, (0, 255, 0)) for _ in range(n)]
        tree = QuadTree(0, 0, w, h, 4)

        for ele in circles:
            tree.insert(ele)
        
        noFill()
        stroke(255, 255, 255)
        tree.draw()
        noStroke()
        
        for ele in circles:
            ele.draw()
        

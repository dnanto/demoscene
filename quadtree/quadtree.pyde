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
        self.x, self.y, self.w, self.h = x, y, w, h
        self.n = n
        self.lvl, self.lab = lvl, lab
        
        self.points = []
        self.nw, self.ne, self.se, self. sw = None, None, None, None
    
    def contains(self, obj):
        x, y = obj if isinstance(obj, tuple) else (obj.x, obj.y)
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h
    
    def subtrees(self):
        return (self.nw, self.ne, self.se, self.sw)
    
    def subdivide(self):
        lvl = self.lvl + 1
        w, h = self.w / 2, self.h / 2
        self.nw = QuadTree(self.x, self.y, w, h, self.n, lvl, "nw")
        self.ne = QuadTree(self.x + w, self.y, w, h, self.n, lvl, "ne")
        self.se = QuadTree(self.x + w, self.y + h, w, h, self.n, lvl, "se")
        self.sw = QuadTree(self.x, self.y + h, w, h, self.n, lvl, "sw")
        
        for obj in self.points:
            for tree in self.subtrees():
                tree.insert(obj)
        
        self.points = []
    
    def insert(self, obj):
        if not self.contains(obj):
            return False
        
        if not self.nw and len(self.points) < self.n:
            obj.col = col[self.lab]
            self.points.append(obj)
            return True
        
        if not self.nw:
            self.subdivide()
        
        for tree in self.subtrees():
            if tree.insert(obj):
                return True
    
    def query(self, x, y, w, h):
        if not self.x > x + w or self.x + self.w > x or self.y < y + h or self.y + h < y:
            for obj in self.points:
                if x < obj.x < x + w and y < obj.y < y + h:
                    yield obj
        
            if self.nw:
                for tree in self.subtrees():
                    for obj in tree.query(x, y, w, h):
                        yield obj
    
    def draw(self):
        rect(self.x, self.y, self.w, self.h)
        for tree in filter(None, self.subtrees()):
            tree.draw()

w = 1000
h = 1000
n = 1
r = 5

drag = None
release = None

tree = QuadTree(0, 0, w, h, n)
circles = []

def keyPressed():
    global tree, circles
    if key == ' ':
        ele = Circle(mouseX, mouseY, r)
        circles.append(ele)
        tree.insert(ele)

def mousePressed():
    global drag
    drag = (mouseX, mouseY) 

def mouseReleased():
    release = (mouseX, mouseY)
    stroke(150, 0, 150)
    x, y, w, h, = drag[0], drag[1], abs(drag[0] - release[0]), abs(drag[1] - release[1])
    rect(drag[0], drag[1], abs(drag[0] - release[0]), abs(drag[1] - release[1]))
    print()
    for obj in tree.query(x, y, w, h):
        obj.col = (255, 255, 0)
        print(obj)
    print()
    
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

        

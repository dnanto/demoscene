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
    
    def __contains__(self, obj):
        return self.x1 < obj.x < self.x2 and self.y1 < obj.y < self.y2
    
    def points(self):
        return self.x1, self.y1, self.x2, self.y2
    
    def intersects(self, bounds):
        return not ((self.x2 < bounds.x1 or bounds.x2 < self.x1) and (self.y2 < bounds.y1 or bounds.y2 < self.y1))
        
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
        
        self.objects = []
        self.nw, self.ne, self.se, self.sw = None, None, None, None
        self.subdivided = False
    
    def subtrees(self):
        return (self.nw, self.ne, self.se, self.sw) if self.subdivided else ()
    
    def subdivide(self):
        x, y, w, h = self.bounds.x1, self.bounds.y1, self.bounds.w / 2, self.bounds.h /2
        self.nw = QuadTree(Bounds(x, y, w, h), self.n, self.lvl + 1, "nw")
        self.ne = QuadTree(Bounds(x + w, y, w, h), self.n, self.lvl + 1, "ne")
        self.se = QuadTree(Bounds(x + w, y + h, w, h), self.n, self.lvl + 1, "se")
        self.sw = QuadTree(Bounds(x, y + h, w, h), self.n, self.lvl + 1, "sw")
        
        for obj in self.objects:
            for tree in self.subtrees():
                tree.insert(obj)
        
        self.objects = []
    
    def insert(self, obj):
        if not obj in self.bounds:
            return False
        
        if not self.subdivided and len(self.objects) < self.n:
            obj.col = col[self.lab]
            self.objects.append(obj)
            return True
        
        if not self.subdivided:
            self.subdivided = True
            self.subdivide()
        
        for tree in self.subtrees():
            if tree.insert(obj):
                return True
    
    def query(self, bounds):
        if self.bounds.intersects(bounds):
            for obj in self.objects:
                if obj in bounds:
                    yield obj

        for tree in self.subtrees():
            for obj in tree.query(bounds):
                yield obj

    def all(self):
        for obj in self.objects:
            yield obj
        for tree in self.subtrees():
            for obj in tree.all():
                yield obj

    def draw(self):
        self.bounds.draw()
        for tree in filter(None, self.subtrees()):
            tree.draw()
    
    def pprint(self):
        print(self.lvl * '\t' + self.lab)
        for obj in self.objects:
            print(self.lvl * '\t' + len(self.lab) * " " + "\t" + str(obj.x) + ", " + str(obj.y))
        for tree in self.subtrees():
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
r = 10

drag = None
release = None

tree = QuadTree(Bounds(0, 0, w, h), n)
circles = []

def keyPressed():
    global tree, circles
    if key in (ENTER, RETURN):
        inserted = set(tree.query(Bounds(0, 0, w, h)))
        print(">", len(inserted), sum(1 for _ in tree.all()))
    if key == ' ':
        ele = Circle(mouseX, mouseY, r)
        circles.append(ele)
        tree.insert(ele)
    if key == 't':
        print()
        tree.pprint()
        print()
        
def mousePressed():
    global drag
    drag = (mouseX, mouseY) 

def mouseReleased():
    release = (mouseX, mouseY)
    stroke(150, 0, 150)
    bounds = Bounds(drag[0], drag[1], abs(drag[0] - release[0]), abs(drag[1] - release[1]))
    bounds.draw((255, 0, 0))
    for obj in tree.query(bounds):
        print(">>", obj)
        obj.col = (255, 255, 0)
    
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

    
        

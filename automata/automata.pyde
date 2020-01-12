from random import randint
from itertools import product

w = 1000
h = 1000
e = 50

class Cell(object):
    def __init__(self, x, y, e):
        self.x, self.y, self.e = x, y, e
    def draw(self):
        fill(200, 200, 200)
        square(self.x, self.y, self.e)
        noFill()
    def __hash__(self):
        return hash((self.x, self.y))
    def __eq__(self, other):
        x, y = (other.x, other.y) if isinstance(other, Cell) else other
        return (self.x, self.y) == other

coors = list(product(range(0, w, e), range(0, h, e)))
grid = {Cell(x, y, e) for x, y in coors if randint(0, 1)}

def moore(x, y, e):
    return (
        (x, y - e),
        (x + e, y - e),
        (x + e, y),
        (x + e, y + e),
        (x, y + e),
        (x - e, y + e),
        (x - e, y),
        (x - e, y - e)
    )

def setup():
    frameRate(60)
    size(w, h)
    colorMode(RGB)
    background(0, 0, 0)
    noFill()
    stroke(255, 255, 255)

def draw():
    global grid
    clear()
    sums = { coor: sum(ele in grid for ele in moore(coor[0], coor[1], e)) for coor in coors }
    grid = {Cell(coor[0], coor[1], e) for coor in coors if (coor not in grid and sums[coor] == 3) or (coor in grid and sums[coor] in (2, 3))}
    for cell in grid:
        cell.draw()

from random import randint

n = 10
s = 3

w = 1000
h = 1000

r = { "0": "1[0]0", "1": "11" }

def setup():
    frameRate(30)
    size(w, h)
    colorMode(RGB)
    background(0, 0, 0)

def draw():
    clear()
    stroke(randint(0, 255))
    strokeWeight(2)

    a = "0"
    for i in range(frameCount % n):
        a = "".join(r.get(e, e) for e in a)

    pos = []
    x, y, deg = 4 + (w - 4) / 2, h - 4, 0
    for e in a:
        stroke(randint(0, 255), randint(0, 255), randint(0, 255))
        # 0: draw a line segment ending in a leaf
        # 1: draw a line segment
        # [: push position and angle, turn
        # ]: pop position and angle, turn 
        if e == "[":
            pos.append((x, y, deg))
            deg -= randint(0, 360)
        elif e == "]":
            x, y, deg = pos.pop()
            deg += randint(0, 360) 
        elif e == "0":
            line(x, y, x + s * sin(radians(deg)), y - s * cos(radians(deg)))
        elif e == "1":
            to = (x + s * sin(radians(deg)), y - s * cos(radians(deg)))
            line(x, y, *to)
            x, y = to

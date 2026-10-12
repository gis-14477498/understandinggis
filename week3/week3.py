from math import sqrt
def distance(x1, y1, x2, y2):
    return sqrt ((x2-x1)**2 + (y2-y1)**2)
d = distance(345678, 456789, 445678, 556789)
print(d)
def distance(x1, y1, x2, y2):
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    return distance
d = distance(345678, 456789, 445678, 556789)
print(d)

import math
import rhinoscriptsyntax as rs


class Color:
    def __init__(self, R, G, B):
        self.R = R
        self.G = G
        self.B = B

    def __add__(self, other):
        return Color(self.R + other.R, self.G + other.G, self.B + other.B)

    def __sub__(self, other):
        return Color(self.R - other.R, self.G - other.G, self.B - other.B)

    def __mul__(self, other):
        # Color must be first item in equation.  So that's Color * number, not number * Color
        return Color(self.R * other, self.G * other, self.B * other)

    def read(self):
        return (self.R, self.G, self.B)


class Domain:
    def __init__(self, _min, _max):
        self.min = _min
        self.max = _max

    def read(self):
        return (self.min, self.max)


def remap(value, source, target):
    # source and target are Domain objects
    # value must be a single number
    # new value is clipped to target domain bounds
    new_value = ((((value - source.min) / (source.max - source.min))
                  * (target.max - target.min)) + target.min)
    if new_value > target.max:
        return target.max
    if new_value < target.min:
        return target.min
    else:
        return new_value

def chunks(list, n):
    # Yield successive n-sized chunks from list
    for i in range(0, len(list), n):
        yield tuple(list[i:i + n])


# declare variables
# gh component requires input of colors, numbers, and _range
# colors must be input as flat list of integers, which then get "chunked" into RGB tuples
colors = list(chunks(colors, 3))
colors = [Color(*x) for x in colors]
domains = zip(_range[0:-1], _range[1:])
domains = [Domain(*x) for x in domains]

# sort numbers into buckets, clip numbers outside of range
buckets = []
for number in numbers:
    for domain in domains:
        if domain.min <= number <= domain.max:
            buckets.append(domains.index(domain))
            break
        if number < domains[0].min:
            buckets.append(0)
            break
        if number > domains[-1].max:
            buckets.append(len(domains) - 1)
            break


# create list of domains that corresponds to list of numbers
source = []
for bucket in buckets:
    source.append(domains[bucket])

# remap each number to the target domain of (0, 1) from its respective source domain
target = Domain(0, 1)
source_increment = 0
positions = []
for number in numbers:
    positions.append(remap(number, source[source_increment], target))
    source_increment += 1

# create list of colors representing the difference between colors2 and colors1
colors1 = colors[0:-1]
colors2 = colors[1:]
differences = []
color1_increment = 0
for color in colors2:
    differences.append(color - colors1[color1_increment])
    color1_increment += 1

# interpolate colors
interpcolors = []
bucket_increment = 0
for position in positions:
    bucket = buckets[bucket_increment]
    interpcolors.append((differences[bucket] * position) + colors1[bucket])
    bucket_increment += 1

# "read" colors and turn them into rhino color objects
colors_out = [rs.coercecolor(color.read()) for color in interpcolors]
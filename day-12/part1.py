import itertools

# requires PyPI module parse
import parse

with open("input.txt") as f:
    input_ = [line.rstrip() for line in f.readlines()]

class Position():
    def __init__(self, line=None, value=None):
        if line:
            x, y, z = parse.parse('<x={:3d}, y={:3d}, z={:3d}>', line)
        elif value:
            x, y, z = value
        else:
            x, y, z = (0, 0, 0)
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return '\'<x={:3d}, y={:3d}, z={:3d}>\''.format(self.x, self.y, self.z)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Position(value=(x, y, z))

    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

class Moon():
    def __init__(self, line):
        self.position = Position(line=line)
        self.velocity = Position()

    def __repr__(self):
        return 'Moon(pos={}, vel={})'.format(repr(self.position),
                                             repr(self.velocity))

    def energy(self):
        return self.position.energy() * self.velocity.energy()

moons = list(map(Moon, input_))

def apply_gravity():
    global moons

    for pair in itertools.combinations(moons, 2):
        first, second = pair

        if first.position.x < second.position.x:
            first.velocity.x += 1
            second.velocity.x -= 1
        elif first.position.x > second.position.x:
            first.velocity.x -= 1
            second.velocity.x += 1

        if first.position.y < second.position.y:
            first.velocity.y += 1
            second.velocity.y -= 1
        elif first.position.y > second.position.y:
            first.velocity.y -= 1
            second.velocity.y += 1
        
        if first.position.z < second.position.z:
            first.velocity.z += 1
            second.velocity.z -= 1
        elif first.position.z > second.position.z:
            first.velocity.z -= 1
            second.velocity.z += 1
        
def apply_velocity():
    global moons

    for moon in moons:
        moon.position += moon.velocity

def time_step():
    global moons

    apply_gravity()
    apply_velocity()


for _ in range(1000):
    time_step()

print(sum(m.energy() for m in moons))

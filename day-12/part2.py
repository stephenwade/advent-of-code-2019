import functools
import itertools
import math

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

initial_moons = list(map(Moon, input_))
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

current_step = 0
def time_step():
    global current_step, moons

    apply_gravity()
    apply_velocity()
    current_step += 1


x_repeat_step = None
y_repeat_step = None
z_repeat_step = None
current_step = 0

while True:
    time_step()

    if not x_repeat_step:
        x_positions_match = lambda: (
            list(map(lambda m: m.position.x, moons))
            == list(map(lambda m: m.position.x, initial_moons))
            )
        x_velocities_match = lambda: (
            list(map(lambda m: m.velocity.x, moons))
            == list(map(lambda m: m.velocity.x, initial_moons))
            )

        if x_positions_match() and x_velocities_match():
            x_repeat_step = current_step

    if not y_repeat_step:
        y_positions_match = lambda: (
            list(map(lambda m: m.position.y, moons))
            == list(map(lambda m: m.position.y, initial_moons))
            )
        y_velocities_match = lambda: (
            list(map(lambda m: m.velocity.y, moons))
            == list(map(lambda m: m.velocity.y, initial_moons))
            )

        if y_positions_match() and y_velocities_match():
            y_repeat_step = current_step

    if not z_repeat_step:
        z_positions_match = lambda: (
            list(map(lambda m: m.position.z, moons))
            == list(map(lambda m: m.position.z, initial_moons))
            )
        z_velocities_match = lambda: (
            list(map(lambda m: m.velocity.z, moons))
            == list(map(lambda m: m.velocity.z, initial_moons))
            )

        if z_positions_match() and z_velocities_match():
            z_repeat_step = current_step

    if x_repeat_step and y_repeat_step and z_repeat_step:
        break

def lcm2(a, b):
    return abs(a*b) // math.gcd(a, b)

def lcm(*items):
    return functools.reduce(lcm2, items)

print(lcm(x_repeat_step, y_repeat_step, z_repeat_step))

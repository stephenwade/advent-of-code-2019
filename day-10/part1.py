import math

with open("input.txt") as f:
    input_ = [line.rstrip() for line in f.readlines()]

map_ = [[x == '#' for x in line] for line in input_]

def is_asteroid_visible(asteroid, from_):
    f_x, f_y = from_
    a_x, a_y = asteroid

    # find the coordinates of the asteroid relative to the initial location
    r_x = a_x - f_x
    r_y = a_y - f_y

    # find the closest point to the intial location that is in line
    gcd = math.gcd(r_x, r_y)
    c_x = int(r_x / gcd)
    c_y = int(r_y / gcd)

    # work from that point outward, checking every point in the line
    x = c_x
    y = c_y

    while x != r_x or y != r_y:
        if map_[f_x + x][f_y + y]:
            return False
        x += c_x
        y += c_y
    return True

def count_asteroids_visible(from_):
    asteroid_count = 0

    for x, row in enumerate(map_):
        for y, has_asteroid in enumerate(row):
            if has_asteroid and (x != from_[0] or y != from_[1]):
                if is_asteroid_visible((x, y), from_):
                    asteroid_count += 1

    return asteroid_count

best_asteroid = (-1, -1)
best_asteroid_count = -1

for x, row in enumerate(map_):
    for y, has_asteroid in enumerate(row):
        if has_asteroid:
            current_asteroid_count = count_asteroids_visible((x, y))
            if current_asteroid_count > best_asteroid_count:
                best_asteroid_count = current_asteroid_count
                best_asteroid = (x, y)

if best_asteroid_count == -1:
    raise ValueError('no asteroids')

print(best_asteroid_count)

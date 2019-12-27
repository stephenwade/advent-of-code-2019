import math

with open("input.txt") as f:
    input_ = [line.rstrip() for line in f.readlines()]


### part 1: find the best asteroid for a monitoring station

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

# the best asteroid for the monitoring station is at best_asteroid


### part 2: which is the 200th asteroid to be vaporized?

def get_asteroids_in_vaporize_order(station):
    m_x, m_y = station
    asteroids = []
    for x, row in enumerate(map_):
        for y, has_asteroid in enumerate(row):
            if has_asteroid and (x != m_x or y != m_y):
                asteroids.append({
                    'point': (x, y),
                    'angle': math.degrees(math.atan2(y - m_y, x - m_x))
                })

    def distance(p1, p2):
        return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

    asteroids = sorted(asteroids, key=lambda x: x['angle'] * 100 - distance(x['point'], station), reverse=True)

    # find first point
    current_i = len(asteroids) - 1
    current_angle = asteroids[current_i]['angle']

    asteroids_vaporized = 0
    while True:
        yield asteroids[current_i]
        asteroids[current_i] = None
        asteroids_vaporized += 1
        if asteroids_vaporized >= len(asteroids):
            break

        # find next point
        next_point_found = False
        for i in range(current_i + 1, len(asteroids)):
            if asteroids[i] and asteroids[i]['angle'] < current_angle:
                current_i = i
                next_point_found = True
                break
        if not next_point_found:
            current_i = 0
            while not asteroids[current_i]:
                current_i += 1
        current_angle = asteroids[current_i]['angle']

# debugging output

# for i, x in enumerate(get_asteroids_in_vaporize_order(best_asteroid)):
#     x_, y = x['point']
#     map_[x_][y] = i
# print('<table>')
# for row in map_:
#     print('<tr>',end='')
#     for cell in row:
#         print('<td>',end='')
#         if cell:
#             print(cell,end='')
#         print('</td>',end='')
#     print('</tr>')
# print('</table>')

x, y = list(get_asteroids_in_vaporize_order(best_asteroid))[200]['point']
print(y*100+x)

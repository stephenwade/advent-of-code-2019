with open("input.txt") as f:
    input = [line.rstrip() for line in f.readlines()]

lines = [line.split(",") for line in input]
lines = [[(instruction[0], int(instruction[1:])) for instruction in line] for line in lines]

if len(lines) != 2:
    raise ValueError('expected two lines')

all_points = []
for line in lines:
    points = []
    current_point = (0, 0)
    for instruction in line:
        (direction, distance) = instruction
        for _ in range(distance):
            (x, y) = current_point
            if direction == 'U':
                y += 1
            elif direction == 'D':
                y -= 1
            elif direction == 'L':
                x -= 1
            elif direction == 'R':
                x += 1
            else:
                raise ValueError('invalid direction in ' + str(instruction))
            current_point = (x, y)
            points.append(current_point)
    all_points.append(points)

common_points = set(all_points[0]) & set(all_points[1])
if not common_points:
    raise ValueError('no line crossings')

# the closest crossing is the intersection with the smallest abs(x) + abs(y)
def distance(point):
    (x, y) = point
    return abs(x) + abs(y)
closest_point = min(common_points, key=distance)

print(distance(closest_point))

with open("input.txt") as f:
    input_ = [line.rstrip() for line in f.readlines()]

lines = [line.split(",") for line in input_]
lines = [[(instruction[0], int(instruction[1:])) for instruction in line] for line in lines]

if len(lines) != 2:
    raise ValueError('expected two lines')

lines_details = []
for line in lines:
    points = []
    current_point = (0, 0)
    current_signal_length = 0
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
            current_signal_length += 1
            points.append({'point': current_point, 'signal_length': current_signal_length})
    lines_details.append(points)

all_points = [[p['point'] for p in line] for line in lines_details]
common_points = set(all_points[0]) & set(all_points[1])
if not common_points:
    raise ValueError('no line crossings')

# look up the signal length for each point
def distance_per_line(point, line):
    for p in line:
        if point == p['point']:
            return p['signal_length']
    raise ValueError('point not found in line')

def distance(point):
    return sum([distance_per_line(point, line) for line in lines_details])

closest_point = min(common_points, key=distance)

print(distance(closest_point))

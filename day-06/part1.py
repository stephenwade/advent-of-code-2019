with open("input.txt") as f:
    input = [line.rstrip() for line in f.readlines()]

lines = [line.split(")") for line in input]
orbits = [(line[0], line[1]) for line in lines]

def count_orbits_r(orbit, orbits, n):
    matching_next_orbits = [x for x in orbits if x[1] == orbit[0]]
    if len(matching_next_orbits) > 1:
        raise ValueError('invalid map data')
    if len(matching_next_orbits) == 1:
        return count_orbits_r(matching_next_orbits[0], orbits, n + 1)
    return n

def count_orbits(orbit, orbits):
    return count_orbits_r(orbit, orbits, 1)

total_orbits = sum(count_orbits(orbit, orbits) for orbit in orbits)

print(total_orbits)

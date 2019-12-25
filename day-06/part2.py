from itertools import zip_longest

with open("input.txt") as f:
    input_ = [line.rstrip() for line in f.readlines()]

lines = [line.split(")") for line in input]
orbits = [(line[0], line[1]) for line in lines]

def find_chain_r(orbits, current_chain):
    #current_chain = current_chain[:]

    parents = [x[0] for x in orbits if x[1] == current_chain[-1]]
    if not parents:
        return current_chain
    else:
        return find_chain_r(orbits, current_chain + [parents[0]])

def find_chain(from_, orbits):
    return find_chain_r(orbits, [from_])

your_chain  = find_chain('YOU', orbits)
santa_chain = find_chain('SAN', orbits)

common_object = None
total_orbits = 0
for (you, san) in zip_longest(reversed(your_chain), reversed(santa_chain)):
    if you == san:
        common_object = you
    else:
        if you: total_orbits += 1
        if san: total_orbits += 1

total_orbital_transfers = total_orbits - 2  # remove YOU and SAN
print(total_orbital_transfers)

from intcode import intcode

with open("input.txt") as f:
    input_ = f.read().rstrip()

program = [x for x in map(int, input_.split(","))]

result = intcode(program, [1])

print(result)

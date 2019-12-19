with open("input.txt") as f:
    input_ = f.read().rstrip()

program = [x for x in map(int, input_.split(","))]

def parse_instruction(x):
    opcode = x % 100

    parameter_modes = []
    x //= 100
    while x > 0:
        parameter_modes.append(x % 10)
        x //= 10
    while len(parameter_modes) < 3:
        parameter_modes.append(0)

    return (opcode, parameter_modes)

def get_value(parameter, mode):
    if mode == 0:
        return program[parameter]
    elif mode == 1:
        return parameter
    else:
        raise ValueError('invalid mode')

# execute Intcode program
pc = 0
while True:
    (opcode, modes) = parse_instruction(program[pc])
    # print((opcode, modes))
    if opcode == 1:
        # print('   ', program[pc+1:pc+4])
        a = get_value(program[pc + 1], modes[0])
        b = get_value(program[pc + 2], modes[1])
        c = program[pc + 3]
        program[c] = a + b
        pc += 4
    elif opcode == 2:
        # print('   ', program[pc+1:pc+4])
        a = get_value(program[pc + 1], modes[0])
        b = get_value(program[pc + 2], modes[1])
        c = program[pc + 3]
        program[c] = a * b
        pc += 4
    elif opcode == 3:
        # print('   ', program[pc+1:pc+2])
        in_ = int(input('> '))
        a = program[pc + 1]
        program[a] = in_
        pc += 2
    elif opcode == 4:
        # print('   ', program[pc+1:pc+2])
        a = get_value(program[pc + 1], modes[0])
        print(a)
        pc += 2
    elif opcode == 99:
        break
    else:
        raise Exception('something went wrong')

with open("input.txt") as f:
    input = f.read().rstrip()
    program = map(int, input.split(","))

    # 1202 program alarm
    program[1] = 12
    program[2] = 2

    # execute Intcode program
    pc = 0
    while True:
        instruction = program[pc]
        if instruction == 1:
            a = program[pc + 1]
            b = program[pc + 2]
            c = program[pc + 3]
            program[c] = program[a] + program[b]
        elif instruction == 2:
            a = program[pc + 1]
            b = program[pc + 2]
            c = program[pc + 3]
            program[c] = program[a] * program[b]
        elif instruction == 99:
            break
        else:
            raise Exception('something went wrong')
        pc += 4

    print(program[0])

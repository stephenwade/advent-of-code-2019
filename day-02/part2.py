with open("input.txt") as f:
    input = f.read().rstrip()

target = 19690720

for noun in range(99):
    for verb in range(99):
        program = map(int, input.split(","))
        
        program[1] = noun
        program[2] = verb
        
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
        
        if program[0] == target:
            print(100 * noun + verb)
            break

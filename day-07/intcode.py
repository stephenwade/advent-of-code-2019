import queue
import threading

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

def get_value(parameter, mode, program):
    if mode == 0:
        return program[parameter]
    elif mode == 1:
        return parameter
    else:
        raise ValueError('invalid mode')

def run(program, input_queue, output_queue):
    pc = 0
    while True:
        (opcode, modes) = parse_instruction(program[pc])
        # print((opcode, modes))
        # add
        if opcode == 1:
            # print('   ', program[pc+1:pc+4])
            a = get_value(program[pc + 1], modes[0], program)
            b = get_value(program[pc + 2], modes[1], program)
            s = program[pc + 3]
            program[s] = a + b
            pc += 4
        # multiply
        elif opcode == 2:
            # print('   ', program[pc+1:pc+4])
            a = get_value(program[pc + 1], modes[0], program)
            b = get_value(program[pc + 2], modes[1], program)
            s = program[pc + 3]
            program[s] = a * b
            pc += 4
        # input
        elif opcode == 3:
            # print('   ', program[pc+1:pc+2])
            in_ = input_queue.get()
            s = program[pc + 1]
            program[s] = in_
            pc += 2
        # output
        elif opcode == 4:
            # print('   ', program[pc+1:pc+2])
            a = get_value(program[pc + 1], modes[0], program)
            output_queue.put(a)
            pc += 2
        # jump-if-true
        elif opcode == 5:
            # print('   ', program[pc+1:pc+3])
            a = get_value(program[pc + 1], modes[0], program)
            b = get_value(program[pc + 2], modes[1], program)
            if a:
                pc = b
            else:
                pc += 3
        # jump-if-false
        elif opcode == 6:
            # print('   ', program[pc+1:pc+3])
            a = get_value(program[pc + 1], modes[0], program)
            b = get_value(program[pc + 2], modes[1], program)
            if not a:
                pc = b
            else:
                pc += 3
        # less than
        elif opcode == 7:
            # print('   ', program[pc+1:pc+4])
            a = get_value(program[pc + 1], modes[0], program)
            b = get_value(program[pc + 2], modes[1], program)
            s = program[pc + 3]
            if a < b:
                program[s] = 1
            else:
                program[s] = 0
            pc += 4
        # equals
        elif opcode == 8:
            # print('   ', program[pc+1:pc+4])
            a = get_value(program[pc + 1], modes[0], program)
            b = get_value(program[pc + 2], modes[1], program)
            s = program[pc + 3]
            if a == b:
                program[s] = 1
            else:
                program[s] = 0
            pc += 4
        elif opcode == 99:
            break
        else:
            raise Exception('something went wrong')

def intcode(program, input_=None, input_queue=None, output_queue=None):
    if not input_queue:
        input_queue = queue.SimpleQueue()
    if not output_queue:
        output_queue = queue.SimpleQueue()
    if input_:
        for item in input_:
            input_queue.put(item)

    thread_ = threading.Thread(target=run, args=(program, input_queue, output_queue))
    thread_.start()

    return (thread_, input_queue, output_queue)

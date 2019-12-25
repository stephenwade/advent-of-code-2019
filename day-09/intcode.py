import collections
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

def get_value(parameter, mode, memory, rbo):
    if mode == 0:
        return memory[parameter]
    if mode == 1:
        return parameter
    if mode == 2:
        return memory[rbo + parameter]
    raise ValueError('invalid mode')

def get_location(parameter, mode, memory, rbo):
    if mode == 0:
        return parameter
    if mode == 1:
        raise ValueError('storage locations cannot be in intermediate mode')
    if mode == 2:
        return rbo + parameter
    raise ValueError('invalid mode')

def run(program, input_queue, output_queue, block):
    memory = collections.defaultdict(lambda: 0)
    for i, x in enumerate(program):
        memory[i] = x

    # program counter
    pc = 0

    # relative base offset
    rbo = 0

    while True:
        (opcode, modes) = parse_instruction(memory[pc])

        # if (memory[pc] == 203): breakpoint()

        # add
        if opcode == 1:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            b = get_value(memory[pc + 2], modes[1], memory, rbo)
            s = get_location(memory[pc + 3], modes[2], memory, rbo)
            memory[s] = a + b
            pc += 4
        # multiply
        elif opcode == 2:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            b = get_value(memory[pc + 2], modes[1], memory, rbo)
            s = get_location(memory[pc + 3], modes[2], memory, rbo)
            memory[s] = a * b
            pc += 4
        # input
        elif opcode == 3:
            in_ = input_queue.get(block)
            s = get_location(memory[pc + 1], modes[0], memory, rbo)
            memory[s] = in_
            pc += 2
        # output
        elif opcode == 4:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            output_queue.put(a, block)
            pc += 2
        # jump-if-true
        elif opcode == 5:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            b = get_value(memory[pc + 2], modes[1], memory, rbo)
            if a:
                pc = b
            else:
                pc += 3
        # jump-if-false
        elif opcode == 6:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            b = get_value(memory[pc + 2], modes[1], memory, rbo)
            if not a:
                pc = b
            else:
                pc += 3
        # less than
        elif opcode == 7:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            b = get_value(memory[pc + 2], modes[1], memory, rbo)
            s = get_location(memory[pc + 3], modes[2], memory, rbo)
            if a < b:
                memory[s] = 1
            else:
                memory[s] = 0
            pc += 4
        # equals
        elif opcode == 8:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            b = get_value(memory[pc + 2], modes[1], memory, rbo)
            s = get_location(memory[pc + 3], modes[2], memory, rbo)
            if a == b:
                memory[s] = 1
            else:
                memory[s] = 0
            pc += 4
        # relative base offset
        elif opcode == 9:
            a = get_value(memory[pc + 1], modes[0], memory, rbo)
            rbo += a
            pc += 2
        elif opcode == 99:
            break
        else:
            raise Exception('something went wrong')

def intcode_thread(program, input_queue=None, output_queue=None, single_thread=True):
    if not input_queue:
        input_queue = queue.SimpleQueue()
    if not output_queue:
        output_queue = queue.SimpleQueue()

    block = not single_thread

    thread_ = threading.Thread(target=run, args=(program, input_queue, output_queue, block))
    thread_.start()

    return (thread_, input_queue, output_queue)

def intcode(program, input_=None):
    input_queue = None

    if input_:
        input_queue = queue.SimpleQueue()
        for item in input_:
            input_queue.put(item)

    (thread_, _, output_queue) = intcode_thread(program, input_queue=input_queue, single_thread=True)
    thread_.join()

    result = []
    while True:
        try:
            item = output_queue.get_nowait()
            result.append(item)
        except queue.Empty:
            return result

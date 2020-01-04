import collections
import enum
import queue
import threading

def read_program(filename):
    with open(filename) as f:
        line = f.read().rstrip()
        return list(map(int, line.split(",")))

class Message(enum.Enum):
    INPUT  = 3
    OUTPUT = 4
    HALT   = 99

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

def run(program, input_queue, output_queue, communication_queue, block):
    memory = collections.defaultdict(lambda: 0)
    for i, x in enumerate(program):
        memory[i] = x

    # program counter
    pc = 0

    # relative base offset
    rbo = 0

    def get_value(parameter, mode):
        if mode == 0:
            return memory[parameter]
        if mode == 1:
            return parameter
        if mode == 2:
            return memory[rbo + parameter]
        raise ValueError('invalid mode')

    def get_location(parameter, mode):
        if mode == 0:
            return parameter
        if mode == 1:
            pass
        if mode == 2:
            return rbo + parameter
        raise ValueError('invalid mode')

    while True:
        (opcode, modes) = parse_instruction(memory[pc])

        # if (memory[pc] == 203): breakpoint()

        # add
        if opcode == 1:
            a = get_value(memory[pc + 1], modes[0])
            b = get_value(memory[pc + 2], modes[1])
            s = get_location(memory[pc + 3], modes[2])
            memory[s] = a + b
            pc += 4
        # multiply
        elif opcode == 2:
            a = get_value(memory[pc + 1], modes[0])
            b = get_value(memory[pc + 2], modes[1])
            s = get_location(memory[pc + 3], modes[2])
            memory[s] = a * b
            pc += 4
        # input
        elif opcode == 3:
            communication_queue.put_nowait(Message.INPUT)
            in_ = input_queue.get(block)
            s = get_location(memory[pc + 1], modes[0])
            memory[s] = in_
            pc += 2
        # output
        elif opcode == 4:
            communication_queue.put_nowait(Message.OUTPUT)
            a = get_value(memory[pc + 1], modes[0])
            output_queue.put(a, block)
            pc += 2
        # jump-if-true
        elif opcode == 5:
            a = get_value(memory[pc + 1], modes[0])
            b = get_value(memory[pc + 2], modes[1])
            if a:
                pc = b
            else:
                pc += 3
        # jump-if-false
        elif opcode == 6:
            a = get_value(memory[pc + 1], modes[0])
            b = get_value(memory[pc + 2], modes[1])
            if not a:
                pc = b
            else:
                pc += 3
        # less than
        elif opcode == 7:
            a = get_value(memory[pc + 1], modes[0])
            b = get_value(memory[pc + 2], modes[1])
            s = get_location(memory[pc + 3], modes[2])
            if a < b:
                memory[s] = 1
            else:
                memory[s] = 0
            pc += 4
        # equals
        elif opcode == 8:
            a = get_value(memory[pc + 1], modes[0])
            b = get_value(memory[pc + 2], modes[1])
            s = get_location(memory[pc + 3], modes[2])
            if a == b:
                memory[s] = 1
            else:
                memory[s] = 0
            pc += 4
        # relative base offset
        elif opcode == 9:
            a = get_value(memory[pc + 1], modes[0])
            rbo += a
            pc += 2
        # halt
        elif opcode == 99:
            communication_queue.put_nowait(Message.HALT)
            break
        else:
            raise Exception('something went wrong')

def intcode(program,
            input_queue=None, output_queue=None, communication_queue=None,
            single_thread=False):
    if not input_queue:
        input_queue = queue.SimpleQueue()
    if not output_queue:
        output_queue = queue.SimpleQueue()
    if not communication_queue:
        communication_queue = queue.SimpleQueue()

    block = not single_thread

    thread = threading.Thread(target=run,
                              args=(program,
                                    input_queue, output_queue,
                                    communication_queue,
                                    block),
                              daemon=True)
    thread.start()

    return (thread, input_queue, output_queue, communication_queue)

def intcode_simple(program, input_=None):
    input_queue = None

    if input_:
        input_queue = queue.SimpleQueue()
        for item in input_:
            input_queue.put(item)

    (thread, _, output_queue, _) = intcode(program,
                                           input_queue=input_queue,
                                           single_thread=True)
    thread.join()

    result = []
    while True:
        try:
            item = output_queue.get_nowait()
            result.append(item)
        except queue.Empty:
            return result

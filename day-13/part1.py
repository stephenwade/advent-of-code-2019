import intcode

with open("input.txt") as f:
    input_ = f.read().rstrip()

program = list(map(int, input_.split(",")))

thread, input_queue, output_queue, communication_queue = intcode.intcode(program)

screen = {}

while True:
    next_message = communication_queue.get()

    if next_message == intcode.Message.INPUT:
        raise ValueError('unexpected message')

    elif next_message == intcode.Message.OUTPUT:
        x = output_queue.get()
        next_message = communication_queue.get()
        if next_message != intcode.Message.OUTPUT:
            raise ValueError('expected 3 outputs in a row')
        y = output_queue.get()
        next_message = communication_queue.get()
        if next_message != intcode.Message.OUTPUT:
            raise ValueError('expected 3 outputs in a row')
        tile = output_queue.get()

        screen[(x, y)] = tile

    elif next_message == intcode.Message.HALT:
        break

print(sum(1 for loc in screen if screen[loc] == 2))

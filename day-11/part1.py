import enum

import intcode

with open("input.txt") as f:
    input_ = f.read().rstrip()

program = list(map(int, input_.split(",")))

thread, input_queue, output_queue, communication_queue = intcode.intcode(program)

class Direction(enum.Enum):
    LEFT  = enum.auto()
    UP    = enum.auto()
    RIGHT = enum.auto()
    DOWN  = enum.auto()

hull = {}
current_location = (0, 0)
current_direction = Direction.UP

def turn_robot(turn):
    global current_location, current_direction

    # Turn left
    if turn == 0:
        if current_direction == Direction.LEFT:
            current_direction = Direction.DOWN
        elif current_direction == Direction.UP:
            current_direction = Direction.LEFT
        elif current_direction == Direction.RIGHT:
            current_direction = Direction.UP
        elif current_direction == Direction.DOWN:
            current_direction = Direction.RIGHT
        else:
            raise ValueError('invalid current_direction')
    # Turn right
    elif turn == 1:
        if current_direction == Direction.LEFT:
            current_direction = Direction.UP
        elif current_direction == Direction.UP:
            current_direction = Direction.RIGHT
        elif current_direction == Direction.RIGHT:
            current_direction = Direction.DOWN
        elif current_direction == Direction.DOWN:
            current_direction = Direction.LEFT
        else:
            raise ValueError('invalid current_direction')
    else:
        raise ValueError('invalid turn instruction')

    # Move forward one space
    x, y = current_location
    if current_direction == Direction.LEFT:
        x -= 1
    elif current_direction == Direction.UP:
        y += 1
    elif current_direction == Direction.RIGHT:
        x += 1
    elif current_direction == Direction.DOWN:
        y -= 1
    else:
        raise ValueError('invalid current_direction')
    current_location = (x, y)

while True:
    next_message = communication_queue.get()

    if next_message == intcode.Message.INPUT:
        if current_location in hull:
            input_queue.put_nowait(hull[current_location])
        else:
            input_queue.put_nowait(0)

    elif next_message == intcode.Message.OUTPUT:
        paint = output_queue.get()
        next_message = communication_queue.get()
        if next_message != intcode.Message.OUTPUT:
            raise ValueError('expected two outputs in a row')
        turn = output_queue.get()

        hull[current_location] = paint
        turn_robot(turn)

    elif next_message == intcode.Message.HALT:
        break

print(len(hull))

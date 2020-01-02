import collections
import curses
import enum
import time

import intcode

class Tile(enum.IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

with open("input.txt") as f:
    input_ = f.read().rstrip()

program = list(map(int, input_.split(",")))

# Insert 2 quarters to play for free
program[0] = 2

score = 0

def main(window):
    global program, score

    thread, input_queue, output_queue, communication_queue = intcode.intcode(program)

    window.clear()

    height, _ = window.getmaxyx()

    def draw_score(score):
        window.addstr(height-1, 0, 'Score: {} '.format(score))
        window.refresh()

    ball_x = None
    paddle_x = None

    def draw_tile(x, y, tile):
        nonlocal ball_x, paddle_x

        if tile == Tile.EMPTY:
            tile_str = '  '
        elif tile == Tile.WALL:
            tile_str = '++'
        elif tile == Tile.BLOCK:
            tile_str = '##'
        elif tile == Tile.PADDLE:
            tile_str = '––'
            paddle_x = x
        elif tile == Tile.BALL:
            tile_str = '()'
            ball_x = x
        window.addstr(y, x*2, tile_str)
        window.refresh()

    delay = 0
    while True:
        next_message = communication_queue.get()

        if next_message == intcode.Message.INPUT:
            delay = 0.001
            if ball_x < paddle_x:
                response = -1
            elif ball_x > paddle_x:
                response = 1
            else:
                response = 0
            input_queue.put(response)

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

            if x == -1 and y == 0:
                score = tile
                draw_score(score)
            else:
                draw_tile(x, y, tile)

            time.sleep(delay)

        elif next_message == intcode.Message.HALT:
            window.getkey()
            break

curses.wrapper(main)

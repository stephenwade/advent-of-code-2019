import collections
import enum
import itertools
import queue

import intcode

class Robot:
    class MoveCommand(enum.IntEnum):
        NORTH = 1
        SOUTH = 2
        WEST = 3
        EAST = 4

        def opposite(self):
            if self == self.NORTH:
                return self.SOUTH
            elif self == self.SOUTH:
                return self.NORTH
            elif self == self.WEST:
                return self.EAST
            elif self == self.EAST:
                return self.WEST

    class Status(enum.IntEnum):
        WALL = 0
        MOVED = 1
        MOVED_OXYGEN = 2

    program = intcode.read_program('input.txt')

    def __init__(self):
        self.thread, self.input_queue, self.output_queue, _ = \
            intcode.intcode(self.program)

    def move(self, direction: MoveCommand) -> Status:
        self.input_queue.put(direction.value)
        return self.Status(self.output_queue.get())

class Cell(enum.Enum):
    UNKNOWN = enum.auto()
    EMPTY = enum.auto()
    WALL = enum.auto()
    OXYGEN = enum.auto()

# adapted from
# https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
def explore():
    grid = collections.defaultdict(
        lambda: collections.defaultdict(
            lambda: Cell.UNKNOWN))

    robot = Robot()

    oxygen_location = None

    def search(x, y, move_command=None):
        nonlocal oxygen_location

        cell = grid[y][x]
        if cell != Cell.UNKNOWN:
            return

        # Try to move into the cell
        if move_command:
            robot_status = robot.move(move_command)

            if robot_status == Robot.Status.WALL:
                grid[y][x] = Cell.WALL
                return

            if robot_status == Robot.Status.MOVED:
                grid[y][x] = Cell.EMPTY
            elif robot_status == Robot.Status.MOVED_OXYGEN:
                grid[y][x] = Cell.OXYGEN
                oxygen_location = (x, y)

        # explore neighbors
        search(x, y+1, Robot.MoveCommand.NORTH)
        search(x, y-1, Robot.MoveCommand.SOUTH)
        search(x-1, y, Robot.MoveCommand.WEST)
        search(x+1, y, Robot.MoveCommand.EAST)

        # Leave the cell
        if move_command:
            robot_status = robot.move(move_command.opposite())
            assert(robot_status == Robot.Status.MOVED)

    search(0, 0)
    return grid, oxygen_location

# explore the entire maze
board, oxygen_location = explore()


# adapted from
# https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar
def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

def neighbors(board, location):
    x, y = location
    for x_, y_ in ((x, y+1), (x, y-1), (x-1, y), (x+1, y)):
        cell = board[y_][x_]
        if cell == Cell.EMPTY or cell == Cell.OXYGEN:
            yield (x_, y_)

def a_star_search(board, start, goal):
    frontier = queue.PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return cost_so_far[goal]

        for next_ in neighbors(board, current):
            new_cost = cost_so_far[current] + 1
            if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                cost_so_far[next_] = new_cost
                priority = new_cost + heuristic(goal, next_)
                frontier.put(next_, priority)
                came_from[next_] = current

# use A* to determine the shortest path from (0, 0) to the oxygen system
print(a_star_search(board, (0, 0), oxygen_location))

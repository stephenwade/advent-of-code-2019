import itertools
import queue

from intcode import intcode

with open("input.txt") as f:
    input_ = f.read().rstrip()

program = [x for x in map(int, input_.split(","))]

def find_output_signal(phase_settings):
    a_input_queue = queue.SimpleQueue()
    a_input_queue.put(phase_settings[0])
    a_output_queue = queue.SimpleQueue()

    b_input_queue = a_output_queue
    b_input_queue.put(phase_settings[1])
    b_output_queue = queue.SimpleQueue()

    c_input_queue = b_output_queue
    c_input_queue.put(phase_settings[2])
    c_output_queue = queue.SimpleQueue()

    d_input_queue = c_output_queue
    d_input_queue.put(phase_settings[3])
    d_output_queue = queue.SimpleQueue()

    e_input_queue = d_output_queue
    e_input_queue.put(phase_settings[4])
    e_output_queue = queue.SimpleQueue()

    (a_thread, _, _) = intcode(program[:], input_queue=a_input_queue, output_queue=a_output_queue)
    (b_thread, _, _) = intcode(program[:], input_queue=b_input_queue, output_queue=b_output_queue)
    (c_thread, _, _) = intcode(program[:], input_queue=c_input_queue, output_queue=c_output_queue)
    (d_thread, _, _) = intcode(program[:], input_queue=d_input_queue, output_queue=d_output_queue)
    (e_thread, _, _) = intcode(program[:], input_queue=e_input_queue, output_queue=e_output_queue)

    a_input_queue.put(0)

    a_thread.join()
    b_thread.join()
    c_thread.join()
    d_thread.join()
    e_thread.join()

    result = e_output_queue.get()
    return result

max_output_signal = max(find_output_signal(x) for x in itertools.permutations(range(5)))
print(max_output_signal)

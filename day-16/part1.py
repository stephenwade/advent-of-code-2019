import functools
import itertools
import operator

with open('input.txt') as f:
    input_ = f.read().rstrip()

signal = list(map(int, input_))

def fft_pattern(element_number):
    base_pattern = [0, 1, 0, -1]
    it = itertools.cycle(
        itertools.chain.from_iterable(
            itertools.repeat(n, element_number) for n in base_pattern
            ))
    next(it)
    return it

def fft(signal, phases):
    output = []
    for _ in range(phases):
        for i in range(len(signal)):
            element_number = i + 1

            result = functools.reduce(
                operator.add,
                itertools.starmap(
                    operator.mul,
                    zip(fft_pattern(element_number), signal)
                    ))
            # print(functools.reduce(operator.add, itertools.starmap(operator.mul, zip(fft_pattern(element_number), signal)))); import sys; sys.exit()
            output.append(abs(result) % 10)

        signal = output
        output = []

    return signal

print(''.join(map(str, fft(signal, 100)[:8])))

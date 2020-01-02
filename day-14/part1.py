import collections
import math

# requires PyPI module parse
import parse

with open('input.txt') as f:
    input_ = [line.rstrip() for line in f.readlines()]

class Chemical():
    def __init__(self, *args):
        if len(args) == 1:
            amount, name = parse.parse('{:d} {}', args[0])
        elif len(args) == 2:
            amount, name = args
        else:
            raise ValueError()
        self.amount = amount
        self.name = name

    def __repr__(self):
        return 'Chemical({} {})'.format(str(self.amount), self.name)

    def __mul__(self, other):
        return Chemical(self.amount * other, self.name)

    def is_ore(self):
        return self.name == 'ORE'

    # def is_fuel(self):
    #     return self.name == 'FUEL'

class Reaction():
    def __init__(self, *args):
        if len(args) == 1:
            input_line, output_line = parse.parse('{} => {}', args[0])
            self.inputs = list(map(Chemical, input_line.split(', ')))
            self.output = Chemical(output_line)
        elif len(args) == 2:
            inputs, output = args
            self.inputs = inputs
            self.output = output

    def __repr__(self):
        return 'Reaction({} => {})'.format(
            ', '.join(repr(c) for c in self.inputs),
            repr(self.output)
            )

    def __mul__(self, other):
        return Reaction(list(map(lambda r: r * other, self.inputs)),
                        self.output * other)

    # def is_ore_reaction(self):
    #     return len(self.inputs) == 1 and self.inputs[0].is_ore()

    # def is_fuel_reaction(self):
    #     return self.output.is_fuel()

reactions = list(map(Reaction, input_))

def make_chemical(request: Chemical,
                 ore_used=0, stock=collections.defaultdict(lambda: 0)):
    if request.amount <= 0:
        raise ValueError('must request positive amount')

    # stock = stock.copy()

    if request.is_ore():
        ore_used += request.amount
        stock[request.name] += request.amount
        return ore_used, stock

    reaction = next(r for r in reactions if r.output.name == request.name)

    # adjust reaction to make at least the requested amount of the chemical
    reaction *= int(math.ceil(request.amount / reaction.output.amount))

    for input_chemical in reaction.inputs:
        amount_needed = input_chemical.amount
        amount_available = stock[input_chemical.name]

        # ensure that enough stock is available
        if amount_available < amount_needed:
            ore_used, stock = make_chemical(
                Chemical(amount_needed - amount_available,
                         input_chemical.name),
                ore_used, stock)

        # consume the chemical
        stock[input_chemical.name] -= amount_needed

    stock[reaction.output.name] += reaction.output.amount

    return ore_used, stock

ore_used, _ = make_chemical(Chemical(1, 'FUEL'))
print(ore_used)

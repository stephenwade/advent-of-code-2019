total = 0
with open("input.txt") as f:
    for line in f:
        num = int(line)
        fuel = num // 3 - 2
        total += fuel
print(total)

total = 0
with open("input.txt") as f:
    for line in f:
        num = int(line)
        my_total = 0
        fuel = num
        while True:
            fuel = fuel // 3 - 2
            if fuel <= 0:
                break
            my_total += fuel
        total += my_total
print(total)

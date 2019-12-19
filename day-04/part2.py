with open("input.txt") as f:
    input = f.read().rstrip()

numbers = [int(x) for x in input.split('-')]
if len(numbers) != 2:
    raise ValueError('expected two numbers')

low = numbers[0]
high = numbers[1]

def is_valid_password(password):
    import itertools
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)

    password_str = str(password)

    any_groups_of_2 = any(sum(1 for _ in group) == 2 for _, group in itertools.groupby(password_str))
    if not any_groups_of_2:
        return False

    any_digits_decrease = any(x[0] > x[1] for x in pairwise(password_str))
    if any_digits_decrease:
        return False

    return True

total_valid_passwords = sum(1 for x in range(low, high+1) if is_valid_password(x))
print(total_valid_passwords)

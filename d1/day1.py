import itertools


def read_changes():
    with open('test.txt') as fp:
        return list(map(lambda x: int(x), fp.readlines()))


def solve_part_1(changes):
    return sum(changes)


def solve_part_2(changes):
    freqs = {0}
    data_iter = itertools.cycle(changes)
    curr_freq = 0
    done = False
    while not done:
        curr_freq += next(data_iter)
        if curr_freq in freqs:
            done = True
        else:
            freqs.add(curr_freq)
    return curr_freq


input_changes = read_changes()
print('Part 1 answer: ', solve_part_1(input_changes))
print('Part 2 answer: ', solve_part_2(input_changes))

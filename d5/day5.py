import string


def read_input():
    with open('secret.txt') as fp:
        return fp.readlines()[0]


def can_react(a, b):
    return (a.islower() ^ b.islower()) and a.lower() == b.lower()


def reduce_reccu(polymer):
    """more elegant way than iter but crashes for large polymers (reccu depth)"""
    for i in range(0, len(polymer) - 1):
        if can_react(polymer[i], polymer[i + 1]):
            return reduce_reccu(polymer[0: i] + polymer[i + 2: len(polymer)])
    return polymer


def reduce_iter(polymer):
    last_slice_start = 0
    while True:
        not_reacted = True
        for i in range(last_slice_start, len(polymer) - 1):
            if can_react(polymer[i], polymer[i + 1]):
                polymer = polymer[0: i] + polymer[i + 2: len(polymer)]
                last_slice_start = 0 if i < 1 else (i - 1)
                not_reacted = False
                break
        if not_reacted:
            return len(polymer)


def solve_part_1(polymer):
    return reduce_iter(polymer)


def remove_unit(polymer, unit):
    return polymer.replace(unit, "").replace(unit.upper(), "")


def solve_part_2(polymer):
    best_min = len(polymer)
    best_reduce = ''
    for unit in string.ascii_lowercase:
        experimental_polymer = remove_unit(polymer, unit)
        poly_len = reduce_iter(experimental_polymer)
        if poly_len < best_min:
            best_min = poly_len
            best_reduce = unit
    return best_min, best_reduce


polymer_input = read_input()
print(polymer_input)
print('Part 1 answer: ', solve_part_1(polymer_input))
print('Part 2 answer: ', solve_part_2(polymer_input))

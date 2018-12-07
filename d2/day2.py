twos = 0
threes = 0


def read_input():
    with open('test.txt') as fp:
        return list(map(lambda x: x.replace('\n', ''), fp.readlines()))


def check_freq(str):
    freq = {}
    for char in str:
        freq[char] = str.count(char)
    return freq


def count_items(item):
    global twos
    global threes
    freq = check_freq(item)
    curr_twos = len([k for k in freq if freq[k] == 2])
    if curr_twos > 0:
        twos += 1
    curr_threes = len([k for k in freq if freq[k] == 3])
    if curr_threes > 0:
        threes += 1


def solve_part_1(t_input):
    for item in t_input:
        count_items(item)
    return twos * threes


def differ_by_one(str1, str2):
    if str1 == str2:
        return False
    if len(str1) != len(str2):
        return False
    diffs = 0
    for i in range(len(str1)):
        if str1[i] != str2[i]:
            diffs += 1
    return diffs == 1


def trim_differ(str1, str2):
    res = ''
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            res += str1[i]
    return res


def solve_part_2(t_input):
    for item in t_input:
        for item2 in t_input:
            if differ_by_one(item, item2):
                return trim_differ(item, item2)


t_input = read_input()
print('Part 1 answer: ', solve_part_1(t_input))
print('Part 2 answer: ', solve_part_2(t_input))


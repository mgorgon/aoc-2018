import re
import datetime
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

EVENT_SHIFT = "SHIFT"
EVENT_FALLS = "FALLS"
EVENT_WAKES = "WAKES"


def to_event(token):
    if "begins shift" in token:
        return EVENT_SHIFT
    if "falls" in token:
        return EVENT_FALLS
    if "wakes" in token:
        return EVENT_WAKES


def read_input():
    with open('test.txt') as fp:
        return sorted(list(map(lambda x: x.replace('\n', ''), fp.readlines())))


def parse_record(record, prev_guard_id):
    tokens = record.split(']')
    tokens[0] = tokens[0].replace('[', '')
    event = to_event(tokens[1])
    minute = datetime.strptime(tokens[0], '%Y-%m-%d %H:%M').time().minute
    guard_desc = [x for x in map(int, re.findall(r'\d+', tokens[1]))]
    guard_id = guard_desc[0] if len(guard_desc) > 0 else prev_guard_id
    return event, minute, guard_id


def parse_records(records):
    guard_views = {}
    guard_id, prev_ix = 0, 0
    prev_stat = EVENT_SHIFT
    for line in records:
        this_stat, this_ix, guard_id = parse_record(line, guard_id)
        if this_stat == EVENT_SHIFT:
            if guard_id not in guard_views:
                guard_views[guard_id] = [0 for x in range(0, 60)]

        if prev_stat == EVENT_FALLS:
            for time in range(prev_ix, this_ix if this_stat == EVENT_WAKES else 60):
                guard_views[guard_id][time] += 1

        prev_stat = this_stat
        prev_ix = this_ix
    return guard_views


def plot_guards_stats(guards):
    flat = [[0 for x in range(60)] for y in range(len(guards))]
    for it, (key, value) in enumerate(guards.items()):
        flat[it] = value
    sns.heatmap(flat, yticklabels=guards.keys(), xticklabels=range(0, 60), cmap="cubehelix")
    plt.show()


def get_favourite_sleep_minute(guard_sleeps):
    return pd.Series(guard_sleeps).idxmax()


def solve_part_1(guards):
    max_sleep, curr_guard = 0, 0
    for key, value in guards.items():
        sleep_sum = sum(value)
        if sleep_sum > max_sleep:
            max_sleep = sleep_sum
            curr_guard = key
    fav_min = get_favourite_sleep_minute(guards[curr_guard])
    return fav_min * curr_guard


def solve_part_2(guards):
    max_sleep, curr_guard = 0, 0
    for key, hours in guards.items():
        curr_max_sleep = max(hours)
        if curr_max_sleep > max_sleep:
            max_sleep = curr_max_sleep
            curr_guard = key
    max_sleep_hour = get_favourite_sleep_minute(guards[curr_guard])
    return max_sleep_hour * curr_guard


sorted_input = sorted(read_input())
guards_stats = parse_records(sorted_input)
plot_guards_stats(guards_stats)

print('Part 1 answer: ', solve_part_1(guards_stats))
print('Part 2 answer: ', solve_part_2(guards_stats))




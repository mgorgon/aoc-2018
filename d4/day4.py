import re
import datetime
from datetime import datetime, timedelta
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
    with open('secret.txt') as fp:
        return sorted(list(map(lambda x: x.replace('\n', ''), fp.readlines())))


def parse_record(raw_record):
    tokens = raw_record.split(']')
    tokens[0] = tokens[0].replace('[', '')
    timestamp = datetime.strptime(tokens[0], '%Y-%m-%d %H:%M')
    date = timestamp.date()
    hour = timestamp.time().hour
    record = {
        "event": to_event(tokens[1]),
        "minute": timestamp.time().minute
    }
    if record["event"] == EVENT_SHIFT:
        record["guard_id"] = [x for x in map(int, re.findall(r'\d+', tokens[1]))][0]
        if hour > 0:
            date = timestamp.date() + timedelta(days=1)
    return record, date


def parse_records(input):
    diary = {}
    for line in input:
        record, date_key = parse_record(line)
        if date_key not in diary:
            diary[date_key] = {}
            diary[date_key]["records"] = []
        if record["event"] == EVENT_SHIFT:
            diary[date_key]["guard_id"] = record["guard_id"]
        else:
            diary[date_key]["records"].append(record)
    return dict(sorted(diary.items()))


def flat_diary(diary):
    for key, value in diary.items():
        diary[key]["guard_status"] = [0] * 60
        prev_stat = EVENT_WAKES
        prev_ix = 0
        for record in value["records"]:
            this_stat = record["event"]
            this_ix = record["minute"]
            if prev_stat == EVENT_FALLS and this_stat == EVENT_WAKES:
                for time in range(prev_ix, this_ix):
                    diary[key]["guard_status"][time] = 1
            prev_stat = this_stat
            prev_ix = this_ix
        if prev_stat == EVENT_FALLS:
            for time in range(prev_ix, 60):
                diary[key]["guard_status"][time] = 1


def plot_diary(diary):
    flat = [[0 for x in range(60)] for y in range(len(diary))]
    for it, (key, value) in enumerate(diary.items()):
        flat[it] = value["guard_status"]
    sns.heatmap(flat, yticklabels=diary.keys(), xticklabels=range(0, 60))
    plt.show()


def reduce_to_guards(diary):
    flat_diary(diary)
    guard_views = {}
    for k in diary.values():
        guard_views.setdefault(k['guard_id'], []).append(k['guard_status'])
    guards = {}
    for k, v in guard_views.items():
        guards[k] = [0 for x in range(0, 60)]
        for val in v:
            for i in range(0, 60):
                guards[k][i] += val[i]
    return guards


def plot_reduced_guards(guards):
    flat = [[0 for x in range(60)] for y in range(len(guards))]
    for it, (key, value) in enumerate(guards.items()):
        flat[it] = value
    sns.heatmap(flat, yticklabels=guards.keys(), xticklabels=range(0, 60), cmap="cubehelix")
    plt.show()


def get_favourite_sleep_minute(guard_sleeps):
    return pd.Series(guard_sleeps).idxmax()


def get_by_sum_of_sleep(guards):
    max_sleep = 0
    curr_guard = 0
    for key, value in guards.items():
        sleep_sum = sum(value)
        if sleep_sum > max_sleep:
            max_sleep = sleep_sum
            curr_guard = key
    return curr_guard


def solve_part_1(guards):
    guard = get_by_sum_of_sleep(guards)
    fav_min = get_favourite_sleep_minute(guards[guard])
    return fav_min * guard


def solve_part_2(guards):
    max_sleep = 0
    curr_guard = 0
    for key, hours in guards.items():
        curr_max_sleep = max(hours)
        if curr_max_sleep > max_sleep:
            max_sleep = curr_max_sleep
            curr_guard = key
    max_sleep_hour = get_favourite_sleep_minute(guards[curr_guard])
    return max_sleep_hour * curr_guard


diary = parse_records(read_input())
plot_diary(diary)

reduced_guards = reduce_to_guards(diary)
plot_reduced_guards(reduced_guards)

print('Part 1 answer: ', solve_part_1(reduced_guards))
print('Part 2 answer: ', solve_part_2(reduced_guards))




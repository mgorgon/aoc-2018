import re
from itertools import chain
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

size = 1000


def read_input():
    with open('secret.txt') as fp:
        return list(map(lambda x: x.replace('\n', ''), fp.readlines()))


def parse_claim(claim_str):
    raw_claim_details = [x for x in map(int, re.findall(r'\d+', claim_str))]
    claim = {
        "id": raw_claim_details[0],
        "starting_col": raw_claim_details[1],
        "ending_col": raw_claim_details[1] + raw_claim_details[3],
        "starting_row": raw_claim_details[2],
        "ending_row": raw_claim_details[2] + raw_claim_details[4]
    }
    return claim


def add_claim_to_area(claim, area):
    for col in range(claim["starting_col"], claim["ending_col"]):
        for row in range(claim["starting_row"], claim["ending_row"]):
            area[col][row] += 1


def solve_part_1(area):
    """How many square inches of fabric are within two or more claims?"""
    return len(list(filter(lambda x: x > 1, chain.from_iterable(zip(*area)))))


def is_claim_intact(claim, area):
    for col in range(claim["starting_col"], claim["ending_col"]):
        for row in range(claim["starting_row"], claim["ending_row"]):
            if area[col][row] > 1:
                return False
    return True


def solve_part_2(claims, area):
    for claim in claims:
        if is_claim_intact(claim, area):
            return claim["id"]


def read_claims(t_input):
    claims = []
    for line in t_input:
        claim = parse_claim(line)
        claims.append(claim)
    return claims


def fill_area(claims):
    area = [[0 for x in range(size)] for y in range(size)]
    for claim in claims:
        add_claim_to_area(claim, area)
    return area


def print_area(area):
    sns.heatmap(area)
    plt.show()


prepared_claims = read_claims(read_input())
prepared_area = fill_area(prepared_claims)
print('Part 1 answer: ', solve_part_1(prepared_area))
print('Part 2 answer: ', solve_part_2(prepared_claims, prepared_area))
print_area(prepared_area)


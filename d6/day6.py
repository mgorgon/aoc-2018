import matplotlib.colors as colors
import matplotlib.cm as cm
import numpy as np
from PIL import Image, ImageDraw
import itertools

DIM = (500, 500)
DIST_TRESHOLD = 10000
DRAW_POINT_RAD = 2
DRAW_TEXT_OFFSET = 3


def read_input():
    with open('secret.txt') as fp:
        for line in fp.readlines():
            yield [int(s) for s in line.split(',')]


def closest_point_manhattan(coordinates, curr_coor):
    minimum_dist = DIM[0] * DIM[1]
    curr_ix = None
    has_dupl = False
    for ix, coor in enumerate(coordinates):
        distance = abs(curr_coor[0] - coor[0]) + abs(curr_coor[1] - coor[1])
        if distance < minimum_dist:
            minimum_dist = distance
            curr_ix = ix
            has_dupl = False
        elif distance == minimum_dist:
            has_dupl = True
    return -1 if has_dupl else curr_ix


def convert_to_color_map(area):
    flatten = list(itertools.chain(*area))
    minima = min(flatten)
    maxima = max(flatten)
    norm = colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=cm.tab20b)
    res = np.zeros((DIM[0], DIM[1], 3), 'uint8')
    for x in range(DIM[0]):
        for y in range(DIM[1]):
            mapped = mapper.to_rgba(area[x][y], bytes=True)
            colo_point = list([mapped[0], mapped[1], mapped[2]])
            res[x][y] = colo_point
    return res


def draw_voronoi(coordinates, area):
    color_map = convert_to_color_map(area)
    img = Image.fromarray(color_map)
    draw = ImageDraw.Draw(img)
    for i in range(len(coordinates)):
        coor = coordinates[i]
        draw.text((coor[1] + DRAW_TEXT_OFFSET, coor[0] + DRAW_TEXT_OFFSET), text=str(i), fill=(255, 255, 255))
        draw.ellipse([coor[1] - DRAW_POINT_RAD, coor[0] - DRAW_POINT_RAD, coor[1] + DRAW_POINT_RAD, coor[0] + DRAW_POINT_RAD], fill=(255, 255, 255))
    img.show()


def get_inf_area_ids(area):
    border_owners = set([])
    for i in range(0, DIM[0]):
        border_owners.add(area[0][i])
        border_owners.add(area[DIM[0] - 1][i])

    for i in range(0, DIM[1]):
        border_owners.add(area[i][0])
        border_owners.add(area[i][DIM[1] - 1])
    return border_owners


def largest_non_inf_area(area):
    flatten = list(itertools.chain(*area))
    counts = [(i, len(list(c))) for i, c in itertools.groupby(sorted(flatten))]
    border_owners = get_inf_area_ids(area)
    internal_counts = [(k, v) for (k, v) in counts if k not in border_owners]
    return max(internal_counts, key=lambda item: item[1])


def draw_dinstances(distances_map):
    color_map = convert_to_color_map(distances_map)
    img = Image.fromarray(color_map)
    img.show()


def solve_part_1(coordinates):
    area = np.zeros((DIM[0], DIM[1]), 'int')
    for x in range(DIM[0]):
        for y in range(DIM[1]):
            closest_point_index = closest_point_manhattan(coordinates, [x, y])
            area[x][y] = closest_point_index
    draw_voronoi(coordinates, area)
    return largest_non_inf_area(area)[1]


def solve_part_2(coordinates):
    area = np.zeros((DIM[0], DIM[1]), 'int')
    region_sum = DIM[0] * DIM[1]
    for y in range(DIM[0]):
        for x in range(DIM[1]):
            for ix, coor in enumerate(coordinates):
                area[x][y] += abs(x - coor[0]) + abs(y - coor[1])
            if area[x][y] >= DIST_TRESHOLD:
                region_sum -= 1
    draw_dinstances(area)
    return region_sum


coordinates_input = list(read_input())
print('Part 1 answer: ', solve_part_1(coordinates_input))
print('Part 2 answer: ', solve_part_2(coordinates_input))

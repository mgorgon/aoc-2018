T_CHILD = 0
T_META = 0

NODE_ID = ord('A')


class Node:
    def __init__(self, childs, metas):
        global NODE_ID
        self.nodeId = chr(NODE_ID)
        self.childs = self.origChilds = childs
        self.metas = self.origMetas = metas
        self.childNodes = []
        self.metaNodes = []
        NODE_ID += 1

    def __str__(self):
        return "[ID=" + self.nodeId + "]"

    def print_childs(self, offset):
        print("--" * offset + self.nodeId)
        for node in self.childNodes:
            node.print_childs(offset + 1)

    def sum_meta(self):
        meta_sum = 0
        for node in self.metaNodes:
            meta_sum += node
        for node in self.childNodes:
            meta_sum += node.sum_meta()
        return meta_sum

    def calc_value(self):
        if len(self.childNodes) == 0:
            return sum(self.metaNodes)
        child_value = 0
        for meta in self.metaNodes:
            if meta <= len(self.childNodes):
                child_value += self.childNodes[meta - 1].calc_value()
        return child_value


def read_input():
    with open('secret.txt') as fp:
        for line in fp.readlines():
            return [int(s) for s in line.split(' ')]


def parse_nodes(licence):
    stack = []
    ix = 2
    current_item = Node(licence[0], licence[1])
    stack.append(current_item)
    while ix < len(licence):
        # print("New loop, ix:", ix, ", licence_val:", licence[ix], "current_item=", current_item)
        if current_item.childs == 0:
            if current_item.metas == 0:
                current_item = stack.pop()
                if current_item.childs > 0:
                    stack.append(current_item)
            else:
                current_item.metas -= 1
                current_item.metaNodes.append(licence[ix])
                ix += 1
        else:
            current_item.childs -= 1
            new_node = Node(licence[ix], licence[ix+1])
            current_item.childNodes.append(new_node)
            stack.append(new_node)
            current_item = new_node
            ix += 2

    return current_item


def solve_part_1(node):
    return node.sum_meta()


def solve_part_2(node):
    return node.calc_value()


licence_input = read_input()
root_node = parse_nodes(licence_input)
print('Part 1 answer: ', solve_part_1(root_node))
print('Part 2 answer: ', solve_part_2(root_node))

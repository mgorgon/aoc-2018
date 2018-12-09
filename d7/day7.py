WORKERS_NO = 5
STEP_DURATION_ADDON = 60


def read_input():
    with open('secret.txt') as fp:
        instructions = []
        for line in fp.readlines():
            instructions.append((line[5], line[36]))
        reqs = list(map(lambda x: x[0], instructions))
        tars = list(map(lambda x: x[1], instructions))
        return reqs, tars


def get_next_components_for_queue(reqs, tars, orig, done):
    requirements = sorted([x for x in reqs if x not in tars])
    if len(requirements) == 0:
        # if none req is left, do remaining components
        available_comps = sorted([x for x in orig if x not in done])
        if len(available_comps) == 0:
            return None
        return available_comps
    return requirements


def do_component(reqs, tars, orig, done=""):
    component = get_next_components_for_queue(reqs, tars, orig, done)
    if component is None:
        return done
    ix = 0
    while ix < len(reqs):
        if reqs[ix] == component[0]:
            reqs.pop(ix)
            tars.pop(ix)
        else:
            ix += 1
    return do_component(reqs, tars, orig, done + component[0])


def solve_part_1(reqs, tars):
    return do_component(reqs, tars, tars.copy(), "")


def get_comp_time(component):
    return ord(component) - 64 + STEP_DURATION_ADDON


def print_header():
    header = "total_time\t"
    for i in range(WORKERS_NO):
        header += "worker_" + str(i) + "\t"
    header += "done_components"
    print(header)


def print_state(total_time, workers, done_components):
    res_row = str(total_time) + "\t"
    working_comps = [k for k in workers]
    for i in range(WORKERS_NO):
        if i >= len(working_comps):
            res_row += " \t"
        else:
            res_row += str(working_comps[i]) + "\t"
    res_row += done_components
    print(res_row)


def solve_part_2(reqs, tars):
    print_header()
    orig = tars.copy()
    current_time = 0
    workers = {}
    done_components = ""
    while len(tars) > 0 or len(workers) > 0:
        print_state(current_time, workers, done_components)

        done_components += collect_finished_components(reqs, tars, workers)
        next_components = get_next_components_for_queue(reqs, tars, orig, done_components)
        if next_components is not None:
            assign_work(next_components, workers)

        current_time += 1
    return current_time - 1


def collect_finished_components(reqs, tars, workers):
    comp_id = 0
    worker_comps = [k for k in workers]
    done_comps = ""
    while comp_id < len(worker_comps):
        comp = worker_comps[comp_id]
        workers[comp] -= 1
        if workers[comp] <= 0:
            done_comps += comp
            del workers[comp]
            ix = 0
            while ix < len(reqs):
                if reqs[ix] == comp:
                    reqs.pop(ix)
                    tars.pop(ix)
                else:
                    ix += 1
        comp_id += 1
    return done_comps


def assign_work(next_components, workers):
    free_workers = WORKERS_NO - len(workers)
    if free_workers > 0:
        for free_worker in range(free_workers):
            for comp in next_components:
                if comp not in workers:
                    workers[comp] = get_comp_time(comp)
                    break


reqiurements, targets = read_input()
print('Part 1 answer: ', solve_part_1(reqiurements, targets))

reqiurements, targets = read_input()
print('Part 2 answer: ', solve_part_2(reqiurements, targets))

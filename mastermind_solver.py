#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import print_function
import pulp
import pulp.solvers

DEBUG = False


def read_file(fname):
    # Read file
    with open(fname, 'rt') as f:
        data = [line for line in map(str.strip, f.readlines()) if len(line) and line[0] not in '!;#']

    # we need at least one clue
    assert(len(data))

    # Get possible values and parse lines
    clue = None
    values = set()
    clue_lines = dict()
    for line in data:
        clue, right_values, in_place = line.split()
        clue = tuple(clue)
        values.update(clue)
        in_place = int(in_place)
        right_values = int(right_values) + in_place
        assert(clue not in clue_lines)
        clue_lines[clue] = right_values, in_place
    solution_size = len(clue)
    return tuple(values), solution_size, clue_lines


def init_model_vars(solution_size, values):

    # Create model
    model = pulp.LpProblem('mastermind', pulp.LpMinimize)
    model += 0  # No objective function

    # Create model flags and auxiliary options
    flags = pulp.LpVariable.dicts("Flags", (range(solution_size), values), 0, 1, pulp.LpInteger)
    options = pulp.LpVariable.dicts("Option", (values, ), 0, 1, pulp.LpInteger)

    # Allow only 1 value per cell and 0 in empty spaces
    for i in range(solution_size):
        model += pulp.lpSum([flags[i][v] for v in values]) == 1, 'Cell_{:02d}_v'.format(i)

    # Allow Option in cells only if Option exists
    for v in values:
        model += pulp.lpSum([flags[i][v] for i in range(solution_size)]) >= options[v],\
            'Option_min_{:02d}'.format(v)
        model += pulp.lpSum([flags[i][v] for i in range(solution_size)]) <= solution_size * options[v],\
            'Option_max_{:02d}'.format(v)

    return model, flags, options


def parse_clue(model, flags, options, clue, right_values, in_place):
    model += pulp.lpSum([options[v] for v in clue]) == right_values, 'options_in_{}'.format(str(clue))
    model += pulp.lpSum([flags[i][v] for i, v in enumerate(clue)]) == in_place, \
        'in_place_{}_in_{}'.format(in_place, str(clue))
    return model


def get_solution(flags, solution_size, mapped_values, values):
    solution = ['-'] * solution_size
    for i in range(solution_size):
        for v in mapped_values:
            if pulp.value(flags[i][v]) == 1:
                solution[i] = values[v]
                break
    return tuple(solution)


def solve_mastermind(values, solution_size, clue_lines):
    mapped_values = range(len(values))
    model, flags, options = init_model_vars(solution_size, mapped_values)
    for clue, score in clue_lines.items():
        mapped_clue = tuple([values.index(k) for k in clue])
        parse_clue(model, flags, options, mapped_clue, *score)

    # Debugging: Write the lp problem model
    if DEBUG:
        model.writeLP('Mastermind_Model.lp')

    # Find all solutions
    while True:
        model.solve()

        # Exit when no more 'optimal' solutions are available
        if model.status != 1:
            break

        # provide the solution
        yield get_solution(flags, solution_size, mapped_values, values)

        # Add a new constraint to forbid finding this solution again
        model += pulp.lpSum([flags[i][v] for i in range(solution_size) for v in mapped_values
                            if pulp.value(flags[i][v]) == 1]) <= solution_size - 1


def main():
    import sys
    values, solution_size, clue_lines = read_file(sys.argv[1])
    solution_generator = solve_mastermind(values, solution_size, clue_lines)

    for solution in solution_generator:
        print(solution)


if __name__ == '__main__':
    main()

import re
import math
from matplotlib import pyplot as plt

class Result:
    def __init__(self, full, independent, separate):
        self.full = full
        self.independent = independent
        self.separate = separate

    def __str__(self):
        return """Result(full        = {0}
       independent = {1}
       separate    = {2})""".format(self.full, self.independent, self.separate)


class Subresult:
    def __init__(self, puzzle_type, satisfiability, conflicts, decisions, propagations, conflict_literals, memory, time):
        self.puzzle_type = puzzle_type
        self.satisfiability = satisfiability
        self.conflicts = conflicts
        self.decisions = decisions
        self.propagations = propagations
        self.conflict_literals = conflicts
        self.memory = memory
        self.time = time

    def __str__(self):
        return """[satisfiable: {0: <2}| restarts: {1: <4}| decisions: {2: <5}| propagations: {3: <6}| conflicts: {4: <6}| memory: {5: <4}: time: {6: <4}]"""\
            .format(self.satisfiability, self.restarts, self.decisions, self.propagations, self.conflicts, self.memory, self.time)


def load_data(filename = "sudoku_output.txt", items = 5354):
    results = []

    with open(filename) as file:
        full_threedoku_data = get_next_set_from(file)
        independent_layers_data = get_next_set_from(file)
        separate_layers_data = get_next_set_from(file)

    for i in xrange(items):
        full = parse_result_from(full_threedoku_data[i], "full")
        independent = parse_result_from(independent_layers_data[i], "independant")
        separate = parse_result_from(separate_layers_data[i], "separate")
        results.append(Result(full, independent, separate))

    return results


def find_numbers_in(string):
    return re.findall(r"[-+]?\d*\.\d+|\d+", string)


def get_next_set_from(file):
    return file.readline()[5:-3].split("], [")


def parse_result_from(data, puzzle_type):
    numbers = find_numbers_in(data)
    return Subresult(puzzle_type,
                     int(float(numbers[0])),
                     int(numbers[1]),
                     int(numbers[2]),
                     int(numbers[3]),
                     int(float(numbers[4])),
                     float(numbers[5]),
                     float(numbers[6])
                     )


def plot_decisions(number):
    data = load_data()
    plt.figure(figsize=(50, 80))

    for i in range(number):
        plt.scatter(i, data[i].full.decisions, color='blue', s = 2)
        plt.scatter(i, data[i].separate.decisions, color='green', s = 2)
        plt.scatter(i, data[i].independent.decisions, color='red', s = 2)

    plt.show()


def plot_time(number):
    data = load_data()
    plt.figure(figsize=(50, 80))

    for i in range(number):
        plt.scatter(i, data[i].full.time, color='blue', s = 2)
        plt.scatter(i, data[i].separate.time, color='green', s = 2)
        plt.scatter(i, data[i].independent.time, color='red', s = 2)

    plt.show()


def plot_decisions_log(number):
    data = load_data()
    plt.figure(figsize=(50, 80))

    for i in range(number):
        plt.scatter(i, math.log(data[i].full.decisions), color='blue', s = 2)
        plt.scatter(i, math.log(data[i].separate.decisions), color='green', s = 2)
        plt.scatter(i, math.log(data[i].independent.decisions), color='red', s = 2)

    plt.show()

plot_decisions(1000)




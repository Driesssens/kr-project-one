# pycosat way source: https://raw.githubusercontent.com/ContinuumIO/pycosat/master/examples/sudoku.pyd
# zchaff way source: http://modelai.gettysburg.edu/2011/clue/SATSolver.py


import pycosat
from pprint import pprint
import json
import subprocess
import time

from satispy import Variable, Cnf
from satispy.solver import Minisat


############# vvvv zChaff vvvvv ##############

def test_kb(clauses):
    maxVar = 0
    for clause in clauses:
        for literal in clause:
            maxVar = max(abs(literal), maxVar)
    out = open('query.cnf', 'w')
    print >> out, 'c This DIMACS format CNF file was generated by SATSolver.py'
    print >> out, 'c Do not edit.'
    print >> out, 'p cnf', maxVar, len(clauses)
    for clause in clauses:
        for literal in clause:
            print >> out, literal,
        print >> out, '0'
    out.close();

    return False, 0

    process = subprocess.Popen('zchaff query.cnf', stdout=subprocess.PIPE, shell=True)
    process.wait()
    stdout = process.stdout

    sol = False
    for l in stdout:
        if sol == True:
            sol = l
        if l == 'Instance Satisfiable\n':
            sol = True
        print(l),

    if sol == False:
        sol = '0'

    sol = [int(x) for x in sol.split()]

    result = l.split()
    stdout.close()

    try:
        if 'SAT' in result:
            return (True, sol)
        elif 'UNSAT' in result:
            return (False, [])
        else:
            print("\nError: SAT/UNSAT not indicated in query.cnf.")
            return (False, [])
    except StopIteration:
        print("Error: Unexpected file end in query.cnf.")
        return (False, [])


############# ^^^^^ zChaff ^^^^##############



def runmini(clauses):
    maxVar = 0
    for clause in clauses:
        for literal in clause:
            maxVar = max(abs(literal), maxVar)
    out = open('query.cnf', 'w')
    print >> out, 'c This DIMACS format CNF file was generated by SATSolver.py'
    print >> out, 'c Do not edit.'
    print >> out, 'p cnf', maxVar, len(clauses)
    for clause in clauses:
        for literal in clause:
            print >> out, literal,
        print >> out, '0'
    out.close();

    process = subprocess.Popen('minisat -no-luby -rinc=1.5 -phase-saving=0 -rnd-freq=0.02 -pre -cpu-lim=5 query.cnf Results/res.txt', stdout=subprocess.PIPE, shell=True)
    process.wait()

    f = open('Results/res.txt', 'r')
    l = f.readlines()
    f.close()

    if 'I' in l[0]:
        print("Satisfiable: INDET")
        return False, -1

    sat = not ('U' in l[0])
    print("Satisfiable: " + str(sat))


    sol = l[1]
    sol = sol[:-3]
    sol = sol.split(' ')

    sol = map(int, sol)
    return sat, sol


def num_rep(lay, row, col, dig):
    """
        Creates a bijection between the set of variables with elements <layer,row,column,digit> and
        the set of natural numbers [1..6561]
    """
    return 729 * (lay - 1) + 81 * (row - 1) + 9 * (col - 1) + dig


def sudoku_3d_clauses():
    """
    Generates constraints (clauses) for the 3D sudoku
    """

    res = []
    # for all cells, ensure that the each cell:
    for lay in range(1, 10):
        for row in range(1, 10):
            for col in range(1, 10):
                # denotes (at least) one of the 9 digits (1 clause)
                res.append([num_rep(lay, row, col, dig) for dig in range(1, 10)])
                # does not denote two different digits at once (36 clauses)
                for dig in range(1, 10):
                    for dig_dif in range(dig + 1, 10):
                        res.append([-num_rep(lay, row, col, dig), -num_rep(lay, row, col, dig_dif)])

    def valid(lay, cells):
        # Ensure the input cells contain different values
        for row, xrow in enumerate(cells):
            for col, xcol in enumerate(cells):
                if row < col:
                    for dig in range(1, 10):
                        res.append([-num_rep(lay, xrow[0], xrow[1], dig), -num_rep(lay, xcol[0], xcol[1], dig)])

    # Ensure rows and columns have distinct values
    for lay in range(1, 10):
        for i in range(1, 10):
            valid(lay, [(i, j) for j in range(1, 10)])
            valid(lay, [(j, i) for j in range(1, 10)])

    # Ensures that no numbers repeat within the same bar, i.e., across layers in the same (row, column) position
    for row in range(1, 10):
        for col in range(1, 10):
            for dig in range(1, 10):
                for lay1 in range(1, 10):
                    for lay2 in range(1, 10):
                        if lay1 == lay2:
                            continue
                        res.append([-num_rep(lay1, row, col, dig), -num_rep(lay2, row, col, dig)])

    # Ensure 3x3 sub-grids "regions" have distinct values
    for lay in range(1, 10):
        for i in 1, 4, 7:
            for j in 1, 4, 7:
                valid(lay, [(i + k % 3, j + k // 3) for k in range(9)])

    return res


def solve3d(grid):
    """
    Solves a 3D sudoku
    """
    clauses = sudoku_3d_clauses()
    for lay in range(1, 10):
        for row in range(1, 10):
            for col in range(1, 10):
                dig = grid[lay - 1][row - 1][col - 1]
                # If there is a given at the particular location, add a unit clause to the KB with the corresponding
                # constraint
                if dig > 0:
                    clauses.insert(0,[num_rep(lay, row, col, dig)])

    # Executes the pycosat solver
    # sol = pycosat.solve(clauses)

    # Executes minisat solver
    sat, sol = runmini(clauses)

    # Executes the zChaff solver
    # sat, sol = test_kb(clauses)
    if not (sat):
        return -1

    sol = set(val for val in sol if val > 0)

    def read_cell(lay, row, col):
        # Obtains the corresponding number assigned to each position in the cube
        for dig in range(1, 10):
            if num_rep(lay, row, col, dig) in sol:
                return dig

    for lay in range(1, 10):
        for row in range(1, 10):
            for col in range(1, 10):
                grid[lay - 1][row - 1][col - 1] = read_cell(lay, row, col)


def sudoku_str_2_list(sud_str, n):
    sud_list = [[0 for x in range(n)] for x in range(n)]
    for row in range(n):
        for col in range(n):
            sud_list[row][col] = int(sud_str[n * row + col])
    return sud_list


def check_3d_cube(curr_cube):
    # Bar constraint
    for row in range(1, 10):
        for col in range(1, 10):
            s = 0
            for lay in range(1, 10):
                s += curr_cube[lay - 1][row - 1][col - 1]
            assert s == 45
            # print ('Row: ' + str(row) + ' Col: ' + str(col) + ' Sum: ' + str(s))

    # Row constraint
    for lay in range(1, 10):
        for col in range(1, 10):
            s = 0
            for row in range(1, 10):
                s += curr_cube[lay - 1][row - 1][col - 1]
            assert s == 45
            # print ('Lay: ' + str(lay) + ' Col: ' + str(col) + ' Sum: ' + str(s))

    # Column constraint
    for lay in range(1, 10):
        for row in range(1, 10):
            s = 0
            for col in range(1, 10):
                s += curr_cube[lay - 1][row - 1][col - 1]
            assert s == 45
            # print ('Lay: ' + str(lay) + ' Row: ' + str(col) + ' Sum: ' + str(s))

    # Box constraint
    for lay in range(1, 10):
        for i in 1, 4, 7:
            for j in 1, 4, 7:
                s = 0
                for k in range(9):
                    s += curr_cube[lay - 1][i + k % 3 - 1][j + k // 3 - 1]
                assert s == 45
                # print ('Lay: ' + str(lay) + ' Row: ' + str(i) + ' Column: ' + str(j) +' Sum: ' + str(s))

    print('All constraints satisfied')


if __name__ == '__main__':

    with open('3d-puzzles.json', 'r+') as f:
        data = json.load(f)

    # Creates a list of cubes
    cube_list = [[] for x in range(len(data) / 9)]
    for id in range(len(data)):
        x = data[id]
        p = x['puzzle']
        cube_list[id // 9].append(sudoku_str_2_list(p, 9))

    # Creates a list of solutions
    sol_list = [[] for x in range(len(data) / 9)]
    for id in range(len(data)):
        x = data[id]
        p = x['solution']
        sol_list[id // 9].append(sudoku_str_2_list(p, 9))

    # pprint(cube_list[8])
    # pprint(sol_list[8])
    # check_3d_cube(sol_list[8])

    # Argument of the range refers to the number of cubes you want to solve
    for cube in range(1000):
        t1 = time.time()
        print('Cube: ' + str(cube))

        ok = solve3d(cube_list[cube])
        if ok == -1:
            #print('Skipping cube ' + str(cube))
            print("Time: " + str(time.time() - t1))
            print('\n')
            continue

        # pprint(cube_list[cube])
        #print(cube_list[cube] == sol_list[cube])
        print("Time: " + str(time.time() - t1))
        #check_3d_cube(cube_list[cube])
        print('\n')
        import time
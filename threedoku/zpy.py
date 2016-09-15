#source: http://modelai.gettysburg.edu/2011/clue/SATSolver.py

'''SATSolver.py - a simple Python interface to the zchaff SAT solver.
Originally by Todd Neller
Ported to Python by Dave Musicant

Copyright (C) 2008 Dave Musicant

'''

import subprocess
import math
import json

def testKb(clauses):
    maxVar = 0
    for clause in clauses:
        for literal in clause:
            maxVar = max(abs(literal),maxVar)
    out = open('query.cnf','w')
    print >> out, 'c This DIMACS format CNF file was generated by SATSolver.py'
    print >> out, 'c Do not edit.'
    print >> out, 'p cnf',maxVar,len(clauses)
    for clause in clauses:
        for literal in clause:
            print >> out,literal,
        print >> out,'0'
    out.close();
    process = subprocess.Popen('zchaff query.cnf',stdout=subprocess.PIPE,
                shell=True)
    process.wait()
    stdout = process.stdout

    sol = False
    for l in stdout:
        if sol == True:
            sol = l
        if l == 'Instance Satisfiable\n':
            sol = True
        print l,

    if sol == False:
        sol = '0'
    print(sol.split())

    result = l.split()
    stdout.close()

    try:
        if 'SAT' in result:
            return True
        elif 'UNSAT' in result:
            return False
        else:
            print "Error: SAT/UNSAT not indicated in query.cnf."
            return False
    except StopIteration:
            print "Error: Unexpected file end in query.cnf."
            return False



def create_sudoku_vars(n):
    # Variables: <i,j,k,d> = 1 if square (i,j) in layer k is assigned with number d, 0 i.o.c.
    # Creates two dictionaries, D and I, in order to enumerate the corresponding variables
    # <i,j,k,d> with the numbers from 1 to n^4 where n is the dimension of the sudoku.

    D = {}
    I = {}
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for d in range(n):
                    pos = len(D)+1
                    atom = str(i+1)+str(j+1)+str(k+1)+str(d+1)
                    D[atom] = pos
                    I[pos] = atom
    return [D, I]


def print_sudoku(sud,n):
    r = 1
    s = ''
    for i, c in enumerate(sud):
        if i < (r * n):
            s += str(c)
            if ((i + 1) % math.sqrt(n) == 0) & (i > 0):
                s += '|'
        if ((i + 1) % n == 0) & (i > 0):
            print(s)
            if ((i + 1) % (n * math.sqrt(n)) == 0) & (i > 0):
                print(int(n + math.sqrt(n)) * '-')
            s = ''
        r += 1

if __name__ == '__main__':
    clauses = [[-1, -2], [2, 1], [-2, -3], [3, 2], [-3, -1], [-3, -2], [1, 2, 3]]
    res = testKb(clauses)
    print 'KB is satisfiable:', res

    [D, I] = create_sudoku_vars(9)

    with open('3d-puzzles.json', 'r+') as f:
        data = json.load(f)

    for i in range(80):
        x = data[i]

    p = x['puzzle']
    z = x['solution']

    print_sudoku(p,9)
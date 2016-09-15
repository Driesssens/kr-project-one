def print_sudoku(sud):
    r = 1
    s = ''
    for i, c in enumerate(sud):
        if i < (r * 9):
            s += str(c)
            if ((i + 1) % 3 == 0) & (i > 0):
                s += '|'
        if ((i + 1) % 9 == 0) & (i > 0):
            print(s)
            if ((i + 1) % 27 == 0) & (i > 0):
                print(12 * '-')
            s = ''
        r += 1
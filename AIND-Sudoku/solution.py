import time

assignments = []



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    crossed = [r+c for r in A for c in B]
    return crossed


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows,cols)
row_units = [cross(r,cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
square_units = [cross(r,c) for r in ('ABC','DEF','GHI') for c in ('123','456','789')]
diag_units = [[rows[ind]+cols[ind] for ind in range(len(rows))]] + [[rows[ind]+cols[::-1][ind] for ind in range(len(rows))]]
unitlist = row_units + col_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    for unit in unitlist:
        for i in range(len(unit)):
            if len(values[unit[i]]) == 2:
                for j in range(i+1, len(unit)):
                    if values[unit[i]] == values[unit[j]]:
                        a = values[unit[i]][0]
                        b = values[unit[i]][1]
                        #print (a,b)
                        for box in unit:
                            if values[box] !=  values[unit[i]]:
                                if a in values[box]:
                                    values = assign_value(values,box,values[box].replace(a,''))
                                if b in values[box]:
                                    values = assign_value(values,box,values[box].replace(b,''))
    return values




def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    all_digits = '123456789'
    values = {}
    for ind in range(len(boxes)):
        if grid[ind] == '.':
            values[boxes[ind]] = all_digits
        else:
            values[boxes[ind]] = grid[ind]
    return values

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*width*3]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    for key in values.keys():
        if len(values[key])==1:
            for peer in peers[key]:
                #values[peer] = values[peer].replace(values[key],'')
                values = assign_value(values,peer,values[peer].replace(values[key],''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            count = 0
            for box in unit:
                if (digit in values[box]):
                    count += 1
                    mark = box
            if count == 1:
                #values[mark] = digit
                values = assign_value(values,mark,digit)

    return values

def reduce_puzzle(values):
    stalled = False
    #print ('reduction')
    while not stalled:
        reduce_puzzle.counter += 1
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        #return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            #print ('reduction error:' )
            return False
    return values
reduce_puzzle.counter = 0

def search(values):
    # reduce the puzzle, it will return false if there is box with zero available values after reduction
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[k])==1 for k in boxes):
        return values  #puzzle solved

    # Choose an unfilled squares with the fewest possibilities
    min_p = float("inf")
    for k in boxes:
        if (len(values[k]) < min_p) & (len(values[k]) > 1):
            min_box = k
            min_p = len(values[k])

    # recursion to solve each one of the branch sudokus untill a solution is found
    for value in values[min_box]:
        #print ('search'+min_box)
        new_values = values.copy()
        new_values[min_box] = value
        solution = search(new_values)
        if solution:
            return solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    #setting the units
    values = grid_values(grid)
    #display(values)
    sol = search(values)
    return sol


'''
if __name__ == '__main__':

    start = time.time()
    for i in range(1):
        #sol = solve('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
        #sol = solve('4.......6.5.3...1...2...9...1.859......1.7......6...8.9.....4...7...8.5...6..3..2')
        sol = solve('8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..')
    end = time.time()
    print('time elapsed: {}'.format(end - start))
    print ('count:', reduce_puzzle.counter)
    display(sol)

'''

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

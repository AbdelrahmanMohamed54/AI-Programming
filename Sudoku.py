def is_goal(state):
    """Check if we've totally solved the Sudoku puzzle (no more '0's left)."""
    return all(0 not in row for row in state)

def next_states(state):
    """Let's see what we can do next in our Sudoku adventure."""
    i, j = find_empty_cell(state)
    extensions = []
    for n in range(1, 10):
        if allowed(state, i, j, n):
            new_state = fill(state, i, j, n)
            extensions.append(new_state)
    return extensions

def find_empty_cell(state):
    """Hunting for empty cells in the Sudoku grid. Any out there?"""
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                return i, j
    return None, None

def allowed(state, i, j, n):
    """Is it okay to put number 'n' in cell (i, j) of our Sudoku puzzle? Let's check."""
    return (
        not in_row(state, i, n) and
        not in_column(state, j, n) and
        not in_square(state, i, j, n)
    )

def in_row(state, i, n):
    """Checking if number 'n' is already in the same row as cell (i, j)."""
    return n in state[i]

def in_column(state, j, n):
    """Checking if number 'n' is already in the same column as cell (i, j)."""
    return n in [state[i][j] for i in range(9)]

def in_square(state, i, j, n):
    """Digging into the 3x3 square to find if number 'n' is already there."""
    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
    for row in range(start_row, start_row + 3):
        for col in range(start_col, start_col + 3):
            if state[row][col] == n:
                return True
    return False

def fill(state, i, j, n):
    """Filling cell (i, j) with our chosen number 'n' and getting a new state to continue our journey."""
    new_state = [row[:] for row in state]
    new_state[i][j] = n
    return new_state

def a_star_search(initial_state, heuristic):
    """We're on an adventure to solve Sudoku using the A* search method."""
    to_do = [[initial_state]]  # Starting with a list of paths to explore

    while to_do:
        to_do.sort(key=lambda path: heuristic(path))  # Sorting paths by our chosen heuristic
        path = to_do[0]  # Grabbing the path that seems promising
        to_do = to_do[1:]  # Removing the chosen path from the list

        current = path[-1]  # Checking where we are now

        if is_goal(current):  # Is this the destination we've been searching for?
            return path

        for state in next_states(current):
            if not any(state == p for p in path) and not any(state == p[-1] for p in to_do):
                new_path = path + [state]
                to_do.append(new_path)

    return "FAILURE: NO PATH FOUND"

# Time to choose our heuristic function for our Sudoku journey.
def heuristic(path):
    # You can pick any heuristic you like to prioritize paths.
    # For simplicity, we're counting empty cells as our guide.
    return sum(row.count(0) for row in path[-1])

# Our starting point, the unsolved Sudoku puzzle in a list of lists.
grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 0, 0]
]

# Time to set off on our Sudoku-solving adventure using A* search and our chosen heuristic.
solution = a_star_search(grid, heuristic)

# Did we make it to the treasure? Let's find out.
if solution == "FAILURE: NO PATH FOUND":
    print("Uh-oh, no solution found. Keep exploring!")
else:
    for row in solution[-1]:
        print(row)

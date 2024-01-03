
N = 3  # You can change N to the desired puzzle size


def isGoal(s):
    goal = [[i * N + j for j in range(N)] for i in range(N)]  # Define the goal state as a 2D list based on the size N
    return s == goal


def find0(state):
    for i in range(N):
        for j in range(N):
            if state[i][j] == 0:
                return i, j
    return None


def allowed(i, j, d):
    if d == 'Up':
        return i > 0
    elif d == 'Down':
        return i < N - 1
    elif d == 'Left':
        return j > 0
    elif d == 'Right':
        return j < N - 1
    return False


def move(s, d):
    i, j = find0(s)
    if d == 'Up':
        s[i][j], s[i - 1][j] = s[i - 1][j], s[i][j]
    elif d == 'Down':
        s[i][j], s[i + 1][j] = s[i + 1][j], s[i][j]
    elif d == 'Left':
        s[i][j], s[i][j - 1] = s[i][j - 1], s[i][j]
    elif d == 'Right':
        s[i][j], s[i][j + 1] = s[i][j + 1], s[i][j]
    return s


def nextStates(state):
    dirs = ['Up', 'Down', 'Left', 'Right']
    result = []
    i, j = find0(state)

    for d in dirs:
        if allowed(i, j, d):
            new_state = [row[:] for row in state]  # Copy the current state
            new_state = move(new_state, d)
            result.append(new_state)

    return result


def DepthFirstSearch(s):
    toDo = [[s]]  # Initialize a stack of paths to explore

    while toDo:
        path = toDo.pop()  # Pop the last path from the stack (LIFO)
        current = path[-1]  # Get the last node on the path

        if isGoal(current):  # If the current state is the goal, return the path
            return path

        for state in nextStates(current):  # Generate successor states
            if state not in [p[-1] for p in path]:  # Check if the state is not previously explored
                new_path = list(path)
                new_path.append(state)
                toDo.append(new_path)  # Add the extended path to the stack

    return ["Error: No path found"]


# Example usage:
start = [[1, 2, 5], [3, 7, 4], [0, 6, 8]]  # Initial state

result = DepthFirstSearch(start)

# Print the result in a more organized way
for state in result:
    for row in state:
        print(row)
    print()  # Add an empty line between states

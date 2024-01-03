from collections import deque

# Maze representation
maze = [[' ', 'W', ' ', ' ', 'G'],
        [' ', 'W', ' ', 'W', ' '],
        [' ', 'W', ' ', ' ', ' '],
        [' ', ' ', 'W', 'W', ' '],
        [' ', ' ', ' ', ' ', ' ']]

# Dimensions of the maze
rows = len(maze)
cols = len(maze[0])

# Define the possible moves
dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

# Function to check if a state is the goal state
def isGoal(s):
    i, j = s
    return maze[i][j] == 'G'

# Function to generate valid next states
def nextStates(s):
    i, j = s
    valid_states = [(i + di, j + dj) for di, dj in dirs if 0 <= i + di < rows and 0 <= j + dj < cols and maze[i + di][j + dj] != 'W']
    return valid_states

# Breadth-First Search to find the shortest path
def bfs(start):
    queue = deque()
    visited = set()
    parent = {}  # For tracking the path

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if isGoal(current):
            # Reconstruct the path
            path = [current]
            while current != start:
                current = parent[current]
                path.append(current)
            path.reverse()
            return path  # Shortest path found

        for neighbor in nextStates(current):
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)

                parent[neighbor] = current

    return []  # No path to the goal

# Starting position (bottom left)
start = (4, 0)

# Find the shortest path to the goal using BFS
shortest_path = bfs(start)

if shortest_path:
    print("Here is the shortest path to the goal:", shortest_path)
else:
    print("No path to the goal from the starting position.")

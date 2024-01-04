import random

NUM_GAMES = 100
EPSILON = 0.1  # Epsilon for the epsilon-greedy strategy
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor

def display_board(board):
    """Display the tic-tac-toe board."""
    print("|", board[0], "|", board[1], "|", board[2], "|")
    print("|", board[3], "|", board[4], "|", board[5], "|")
    print("|", board[6], "|", board[7], "|", board[8], "|")
    print("-" * 14)  # Add a separator line

def check_winner(board):
    """Check if there is a winner or if the board is full (a tie)."""
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != "_":
            return board[i]

    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != "_":
            return board[i]

    # Check diagonals
    if board[0] == board[4] == board[8] != "_":
        return board[0]
    if board[2] == board[4] == board[6] != "_":
        return board[2]

    # Check if the board is full (tie)
    if "_" not in board:
        return "Tie"

    return None


def choose_action(q_table, state):
    """Choose an action based on the epsilon-greedy strategy."""
    if random.uniform(0, 1) < EPSILON or state not in q_table:
        return random.choice([i for i, x in enumerate(state) if x == "_"])
    else:
        return max([i for i, x in enumerate(state) if x == "_"], key=lambda a: q_table.get((state, a), 0))


def make_move(q_table, state, action):
    """Make a move on the board."""
    state_list = list(state)
    empty_cells = [i for i, x in enumerate(state_list) if x == "_"]

    if action in empty_cells:
        # Use the actual index of the empty cell for the move
        chosen_cell = action
        state_list[chosen_cell] = "O" if state_list.count("X") > state_list.count("O") else "X"

        # Update the state after the move
        new_state = "".join(state_list)

        # Add the new state to the Q-table if it doesn't exist
        if (state, action) not in q_table:
            q_table[(state, action)] = 0.0

    return "".join(state_list)


def update_q_table(q_table, state, action, reward, next_state):
    """Update the Q-table based on the Q-learning update rule."""
    old_value = q_table.get((state, action), 0.0)
    next_max = max([q_table.get((next_state, a), 0.0) for a in range(9)])
    new_value = old_value + ALPHA * (reward + GAMMA * next_max - old_value)
    q_table[(state, action)] = new_value


def OneGame(q_table):
    """Play one game and update the Q-table."""
    state = "_________"
    history = []

    while "_" in state:
        # Display the board if needed:
        # display_board(state)

        action = choose_action(q_table, state)
        history.append((state, action))

        state = make_move(q_table, state, action)

        winner = check_winner(state)
        if winner is not None:
            if winner == "Tie":
                reward = 0.5  # Tie
            elif state.count(winner) % 2 == 0:
                reward = 1.0  # Win
            else:
                reward = -1.0  # Lose

            for s, a in history:
                update_q_table(q_table, s, a, reward, state)
            break


def play_against_q_table(q_table):
    """Play a game against the Q-learning agent and update the Q-table."""
    state = "_________"
    history = []  # Initialize history for this game

    while "_" in state:
        display_board(state)

        # Human player's move
        while True:
            try:
                player_move = int(input("Enter your move (0-8): "))
                if 0 <= player_move <= 8 and state[player_move] == "_":
                    break
                else:
                    print("Invalid move. Please choose an empty cell (0-8).")
            except ValueError:
                print("Invalid input. Please enter a number.")

        state = make_move(q_table, state, player_move)
        history.append((state, player_move))  # Append to history after the move

        if check_winner(state) is not None:
            display_board(state)
            if check_winner(state) == "Tie":
                print("It's a Tie!")
            else:
                print("You Win!")
            break

        display_board(state)
        print("Agent is thinking...")
        agent_action = choose_action(q_table, state)
        state = make_move(q_table, state, agent_action)
        history.append((state, agent_action))  # Append to history after the agent's move

        if check_winner(state) is not None:
            display_board(state)
            if check_winner(state) == "Tie":
                print("It's a Tie!")
            else:
                print("Agent wins!")
            break


if __name__ == "__main__":
    q_table = {}

    # Train the Q-learning agent by playing multiple games against itself
    for _ in range(NUM_GAMES):
        print(f"Training Game no: {_ + 1}")
        OneGame(q_table)
        print("End of this game reached!")
        print(" ")

    # Play a game against the Q-learning agent
    play_against_q_table(q_table)

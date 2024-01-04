import random

NUM_GUMDROPS = 100


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


def choose(weights):
    """Choose a move based on the weights."""
    total = max(0, sum(weights))

    if total == 0 or not weights:
        return random.randint(0, len(weights) - 1)

    roll = random.randint(1, total)

    for i, w in enumerate(weights):
        if roll <= w:
            return i
        roll -= w


def make_move(state, action, is_menace_move=True):
    """Make a move on the board."""
    state_list = list(state)

    if is_menace_move:
        # MENACE move logic
        empty_cells = [i for i, x in enumerate(state_list) if x == "_"]
        if action < len(empty_cells):
            chosen_cell = empty_cells[action]
        else:
            return state  # If action is out of bounds, return the same state
    else:
        # Human move logic
        if state_list[action] == "_":
            chosen_cell = action
        else:
            return state  # If cell is not empty, return the same state

    # Update the cell with the current player's symbol
    state_list[chosen_cell] = "O" if state_list.count("X") > state_list.count("O") else "X"

    # Update the state after the move
    return "".join(state_list)


def update_menace(menace, history, winner):
    """Update the MENACE dictionary based on the game outcome."""
    for state, move_index in history:
        if state not in menace:
            continue  # Skip updating if the state is not in the menace dictionary

        if winner == "Tie":
            for i in range(len(menace[state])):
                menace[state][i] += 5
        elif state.count(winner) % 2 == 0 and 0 <= move_index < len(menace[state]):
            menace[state][move_index] += 10
        elif 0 <= move_index < len(menace[state]):
            menace[state][move_index] -= 15


def OneGame(menace):
    """Play one game and update the MENACE dictionary."""
    state = "_________"
    history = []

    while "_" in state:
        #display_board(state)  #remove the "#" if you want to make sure that the function works

        if state not in menace:
            menace[state] = [NUM_GUMDROPS] * state.count("_")

        move_index = choose(menace[state])
        history.append((state, move_index))

        state = make_move(state, move_index)

        winner = check_winner(state)
        if winner is not None:
            #display_board(state)  #remove the "#" if you want to make sure that the function works
            if state not in menace:
                menace[state] = [NUM_GUMDROPS] * state.count("_")
            update_menace(menace, history, winner)
            break


def play_against_menace(menace):
    """Play a game against MENACE and update MENACE."""
    state = "_________"
    history = []  # Initialize history for this game

    while "_" in state:
        display_board(state)

        # Human player's move
        while True:
            try:
                player_move = int(input("Enter your move (0-8): "))
                if 0 <= player_move <= 8 and state[player_move] == "_":
                    state = make_move(state, player_move, False)  # False for human move
                    history.append((state, player_move))  # Append to history after the move
                    break
                else:
                    print("Invalid move. Please choose an empty cell (0-8).")
            except ValueError:
                print("Invalid input. Please enter a number.")

        winner = check_winner(state)
        if winner is not None:
            display_board(state)
            print_winner_message(winner)
            update_menace(menace, history, winner)  # Update MENACE for the outcome
            break

        # Check and add new state for MENACE if not present
        if state not in menace:
            menace[state] = [NUM_GUMDROPS] * state.count("_")

        # MENACE's move
        display_board(state)
        print("MENACE is thinking...")
        move_index = choose(menace[state])
        state = make_move(state, move_index)  # MENACE's move
        history.append((state, move_index))  # Append to history after MENACE's move

        winner = check_winner(state)
        if winner is not None:
            display_board(state)
            print_winner_message(winner)
            update_menace(menace, history, winner)  # Update MENACE for the outcome
            break

def print_winner_message(winner):
    """Prints the winning message."""
    if winner == "Tie":
        print("It's a Tie!")
    elif winner == "X":
        print("You Win!")
    elif winner == "O":
        print("MENACE wins!")


def play_match(menace, menace2):
    state = "_________"
    history = []

    while "_" in state:
        display_board(state)

        # Player 1 (my MENACE)
        move_index1 = choose(menace[state])
        history.append((state, move_index1))
        state = make_move(state, move_index1)

        if check_winner(state) is not None:
            display_board(state)
            print("Player 1 wins!")
            update_menace(menace, history, "X")
            break

        # Player 2 (Friend's MENACE)
        display_board(state)
        print("Player 2 (Friend's MENACE) is thinking...")
        move_index2 = choose(menace2[state])
        history.append((state, move_index2))
        state = make_move(state, move_index2)

        if check_winner(state) is not None:
            display_board(state)
            print("Player 2 wins!")
            update_menace(menace2, history, "O")
            break

    print("Game Over.")


# My Menace system can play against another MENACE system
"""
if __name__ == "__main__":
    # Assuming menace1 is my MENACE and menace2 is my friend's MENACE
    menace = {}
    menace2 = {}

    # Train both MENACE systems independently
    for _ in range(1000):
        OneGame(menace)
        OneGame(menace2)

    # Play a match between MENACE systems
    play_match(menace, menace2)
"""
menace = {}

if __name__ == "__main__":

    # Train MENACE by playing multiple games against itself
    for _ in range(10000):
        if _ <= 9999:
            print(f"Training Game no :{_+1}")
        OneGame(menace)
        print("End of this game reached!")
        print(" ")

    # Play a game against MENACE
    play_against_menace(menace)

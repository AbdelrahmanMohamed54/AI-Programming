# MENACE (Matchbox Educable Noughts And Crosses Engine)

This Python program implements MENACE, a machine learning algorithm developed by Donald Michie in the 1960s, to play the game of Tic-Tac-Toe (Noughts and Crosses). MENACE stands for "Matchbox Educable Noughts And Crosses Engine."

## Introduction

MENACE learns to play Tic-Tac-Toe through reinforcement learning, specifically using the Q-learning algorithm. Reinforcement learning is a type of machine learning where an agent learns to make decisions by interacting with an environment and receiving feedback in the form of rewards or penalties. Q-learning is a popular reinforcement learning algorithm that enables an agent to learn the optimal action-selection policy for a given environment.

## Program Structure

- `MENACE.py`: This file contains the Python code for the MENACE algorithm.
- `README.md`: This file provides an overview of the MENACE program and instructions for running it.

## Dependencies

The MENACE program requires Python 3.x to run. It also uses the `random` module for generating random moves.

## Usage

To use the MENACE program, follow these steps:

1. Ensure you have Python 3.x installed on your system.
2. Run the `MENACE.py` file using a Python interpreter.
3. Follow the prompts to play Tic-Tac-Toe against MENACE.

## How It Works

1. **Training MENACE**: MENACE is trained by playing multiple games against itself. During each game, MENACE selects moves based on the current game state and updates its strategy based on the outcome of the game.

2. **Playing Against MENACE**: After training, you can play Tic-Tac-Toe against MENACE. MENACE selects its moves based on the strategy it has learned during training.

3. **Game Outcome**: MENACE updates its strategy based on the outcome of each game. If MENACE wins or ties the game, it strengthens its strategy for the moves that led to the outcome. If MENACE loses, it weakens its strategy for the moves that led to the outcome.

## References

- Donald Michie, *"Experiments on the mechanization of game-learning."* Nature 218.5137 (1968): 19-22.
- Wikipedia contributors. (2022, February 9). [Matchbox Educable Noughts And Crosses Engine](https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_And_Crosses_Engine). In Wikipedia, The Free Encyclopedia.

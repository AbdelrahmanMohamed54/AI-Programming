# AI-Programming

This repository showcases a diverse collection of Python-based algorithms tailored for solving a variety of puzzles and computational problems. Ranging from classic puzzles like mazes and Sudoku to more advanced concepts in artificial intelligence like neural networks and symbolic computation, this collection serves as a valuable resource for understanding different algorithms and their applications.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

```bash
# Clone the repository
git clone https://github.com/AbdelrahmanMohamed54/AI-Programming

# Navigate to the repository directory
cd AI-Programming
```

## Usage

Make sure you have python installed in your machine.

```bash
# Example command to run a script
python Maze.py
```

---

## Features

### SearchProblems:

#### 1. Maze Solver (`Maze.py`)
   - **Description**: Implements the Breadth-First Search (BFS) algorithm to find the shortest path through a maze, represented as a 2D grid.
   - **Functionality**: Solves mazes with walls, open paths, and a specified goal.
  
#### 2. Sliding Puzzle Solver (`Sliding_Tiles_A_Star.py`)
   - **Description**: Uses the A* search algorithm to solve N x N sliding puzzles.
   - **Functionality**: Arranges numbered tiles to achieve a specific goal state.

#### 3. Depth-First Search for Sliding Tiles (`Sliding_Tiles_DFS.py`)
   - **Description**: Applies the Depth-First Search (DFS) algorithm to solve N x N sliding tile puzzles.
   - **Functionality**: Handles the challenge of rearranging numbered tiles in a grid format.

#### 4. BFS for Sliding Tiles (`BreadthFirstSearch_SlidingTiles.py`)
   - **Description**: Implements Breadth-First Search (BFS) to solve sliding tile puzzles in an N x N grid.
   - **Functionality**: Finds the shortest path to arrange tiles in a specified sequence.

#### 5. Sudoku Solver (`sudoku.py`)
   - **Description**: Utilizes the A* search algorithm for solving Sudoku puzzles.
   - **Functionality**: Fills a 9x9 grid following Sudoku rules, ensuring each row, column, and 3x3 subgrid contains all digits from 1 to 9.

### Reinforcement-Learning: 

#### 6. Tic-Tac-Toe Learning Algorithm (`MENACE.py`)
   - **Description**: Implements the MENACE (Matchbox Educable Noughts and Crosses Engine) for playing and learning Tic-Tac-Toe.
   - **Functionality**: Uses reinforcement learning to enhance gameplay strategy over time.
   - 
#### 7. Q-Learning for Tic-Tac-Toe (Q-learning.py)
   - **Description**: Implements the Q-learning algorithm for training an agent to play Tic-Tac-Toe.
   - **Functionality**: Trains through self-play and then allows a human player to challenge the AI agent.

### Perceptrons:

#### 8. Basic Perceptron Implementation (`Simple_perceptron.py`)
   - **Description**: Demonstrates the training of a basic Perceptron for digit recognition.
   - **Functionality**: Recognizes patterns in data using a generated dataset of noisy samples.

#### 9. Sigmoidal Perceptron (`Sigmoid_perceptron.py`)
   - **Description**: Extends the basic Perceptron model with a sigmoid activation function.
   - **Functionality**: Handles more complex patterns for digit recognition, training with noisy samples.

### Symbolic-Computation:

#### 9. Symbolic Computation (`Symbolic_computation.py`)
   - **Description**: Provides a framework for symbolic computation in algebraic expressions.
   - **Functionality**: Facilitates handling and differentiation of algebraic expressions.

#### 10. Symbolic Perceptron (`SymbolicPerceptron.py`)
   - **Description**: Merges symbolic computation with perceptron mechanics.
   - **Functionality**: Manipulates expressions in perceptron operations for a deeper understanding of neural networks.

### SAT-SMT:

#### 11. Logical Puzzle Solver (`SAT-SMT.py`)
   - **Description**: Solves complex logical puzzles using the Z3 SMT solver.
   - **Functionality**: Handles relationships between different sets of variables under constraints.

---

## Contributing

Your contributions are most welcomed! Please follow these steps to contribute:-

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

For questions regarding the project, please reach me at:

- Abdelrahman Mohamed - [Email](mailto:budimohamed572@gmail.com)
- Project Link: [https://github.com/AbdelrahmanMohamed54/AI-Programming](https://github.com/AbdelrahmanMohamed54/AI-Programming)


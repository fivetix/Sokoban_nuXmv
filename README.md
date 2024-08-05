# Sokoban_nuXmv

Formal Verification Final Project

## Overview

Sokoban, Japanese for “warehouse keeper”, is a transport puzzle created by Hiroyuki Imabayashi in 1980. The goal of the game is to push the boxes to designated locations in the warehouse. The warehouse is depicted as a grid with walls creating a labyrinth.

### Game Rules:
- The warehouse keeper can only move horizontally or vertically in the grid, one cell at a time.
- Boxes can only be pushed, not pulled, into an empty space.
- The warehouse keeper and boxes cannot enter “wall” cells.

### Board Symbols:
- `@`: Warehouse keeper
- `+`: Warehouse keeper on goal
- `$`: Box
- `*`: Box on goal
- `#`: Wall
- `.`: Goal
- `-`: Floor

## Project Structure

### Part 1

1. Defined an FDS for a general `n × m` Sokoban board using XSB format.
2. Defined a general temporal logic specification for a win of the Sokoban board.

### Part 2

1. Automated the definition of input boards into SMV models using Python. These models contain both the model and the temporal logic formulae defining a win.
2. Ran each model in nuXmv and documented the commands used and the outputs.
3. Determined if each board is winnable and provided the winning solution in LURD format.

### Part 3

1. Measured performance of nuXmv’s BDD and SAT Solver engines on each model.
2. Compared the performance of the two engines to determine which is more efficient.

### Part 4

1. Solved the boards iteratively by solving for one box at a time.
2. Indicated runtime for each iteration and the total number of iterations needed for each board.
3. Tested the iterative solution on larger, more complex Sokoban boards.

## Files in the Repository

- `board_to_XSB_gui.py`: A Python script with a GUI to quickly create Sokoban boards. Users can place the warehouse keeper, boxes, and goals on the board, and the script will output the board in the required format.
- `part2.py`: The main Python script that performs tasks from Parts 2, 3, and 4.
  - Allows selection between BDD or SAT solvers.
  - Supports iterative mode to solve one box at a time.
  - Generates the Sokoban board based on input.
  - Creates an SMV file that describes the board and the game rules.
  - Runs the SMV file in nuXmv and outputs the results and run times.

## Running the Project

### Prerequisites

Ensure you have the following installed:
- Python
- nuXmv
- Required Python packages: tkinter (for GUI), os, subprocess

### Steps

1. Clone this repository to your local machine.
2. Place the Python files (`part2.py`, `board_to_XSB_gui.py`) inside the nuXmv folder under `...\bin`.
3. To create a Sokoban board:
   - Run `board_to_XSB_gui.py` and use the GUI to create your board. Copy the board output.
4. To run the main script:
   - Open `part2.py` and paste your board in the `board_str10` variable.
   - Choose the solver (BDD/SAT) and mode (iterative/regular) in the GUI.
   - Open the command line, navigate to the nuXmv bin directory, and run:
     ```bash
     python part2.py
     ```
5. The script will generate and run the SMV model in nuXmv, creating output files with the results and run times.

### Output Files

- `result_model.smv`: SMV file containing the Sokoban code for the input board.
- `result_model.out`: Output file with nuXmv results in LURD format.
- `result_for_model.out`: Output file with running times for BDD and SAT runs.
- `cumulative_results_for_model.out`: Output file with cumulative running times for iterative runs.

## Submission

- Upload all codes, XSB Sokoban boards, SMV files, and outputs to a GitHub repo. Include this README explaining how to run the codes.
- Compile all answers and results into a PDF report.
- Include a link to your GitHub repo in your PDF submission.

## Sample Boards

You can find sample Sokoban boards in the repository to help set up your codes and test different scenarios.

---

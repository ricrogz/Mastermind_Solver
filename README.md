# Mastermind_Solver
A python PuLP solver for "[MasterMind](https://en.wikipedia.org/wiki/Mastermind_(board_game))" games.

The shape of the game (any *clue* length is allowed) as well as the possible values are detected from the input file (therefore, the *clues* you provide should contain all potential values that may be used). The program will generate all possible solutions for the *clue* set given in the input file. If no solution is provided, then the game is impossible.

**Note on repetitions**: *evaluations* of the *clues* should be understood "peg-wise". For more details, see the description of the [MasterMind Game in Wikipedia](https://en.wikipedia.org/wiki/Mastermind_(board_game)). 

# Input file format

The format of the input files is very simple. It just contains a set of lines with the following format:
```
[clue] [correct color, wrong placing] [correct color, right placing]
```

The *clues* are strings of characters (i.e. both numbers and letters are allowed). 

# Usage

Just run the program with the path to the input file as argument. Both of the following examples should work:

```bash
./mastermind_solver.py example/sample1.mastermind
python mastermind_solver.py example/sample1.mastermind
```

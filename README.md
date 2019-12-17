# sudokuAI2019


sudoku.py
--------------------------
contains sudoku module

HOW TO RUN:
Run the file sudoku.py with the following argument options:

-h : Help (Prints this info basically)

-b : Board name

-f : File type. Either 's' for sample (.sudoku files) or 'w' for Warwick puzzles

-w : Which row. An integer specifying which puzzle to use. Only applicable to Warwick puzzles

-a : Solve with AI!

-s : Specify what form of search to use. Only applicable to AI mode. Options:  b= basic search, p= with constraint propagation as pre-processing only, f=with forward-checking, m= MAC search

-v: Specify what variable ordering heuristic to use. Only applicable to AI mode. Options: m= MRV, r= random, o= In order

Example Commands to run the Solver:

"python sudoku.py -b debug.sudoku -a -f s"

"python sudoku.py -b top95.txt -a -f w -w 1"


--------------------------

Experiments:

1. Importance of ordering heuristics
Measure time+ number of nodes expanded:
  - without any ordering heuristics
  - with MRV heuristic
  - (optional) with LCV heuristic
  - (optional) with both MRV and LCV heuristics

2. Importance of constraint propagation
Measure time+ number of nodes expanded:
  - no constraint propagation (basic backtracking)
  - (maybe) AC3 as pre-processing only
  - backtracking + forward checking
  - MAC (imposes arc consistency at each step)  



My thoughts:
- these seem like plenty of experiments to be sufficient for our write-up

- the next thing we need to do that is important (for gathering results) is make a list of puzzles of increasing difficulty that we want to use for our testing set (and decide how big that testing set should be)

- i don't _especially_ want to implement LCV at the moment - it doesn't *seem* like it would be that important and if we have limited time/resources, it doesn't seem like the highest priority
- other optional stretch goal from before: one thing we could experiment with (if we need it) is implementing k-consistency and then testing it with different values of k

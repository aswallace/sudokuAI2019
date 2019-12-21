import array
import copy
import json
import random
from neighborDict import neighbors

# Global variables
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
NROWS = 9
NCOLS = 9

# pass in solution and see if we ever rule out the correct solution
# MRV? without inference
# in order variable heuristic disrupting MRV?

# experiment: take out MRV, make it do the bottom to top order, try with and
# without inference
# (Ramya and Arielle result that MRV is not the best?)

# ^if we

# can borrow Ramya and Arielle code (acknowledge if you see anything but try not see anything)

# AC-3 is probably right (Prof. Erin thinks)
# and we think backtracking is probably right

# we set out to discover how much inference matters
# maybe we discover an interesting interaction between MRV and inference? (hold variable
# ordering constant)

class SudokuSolver:
    def __init__(self, sudokuGame):
        self.game = sudokuGame
        self.assignment = self.makeAssignment(sudokuGame.start_puzzle)
        self.nodesExpanded = 0

    def makeAssignment(self, board):
        '''populates the assignment dictionary with the initial board values'''
        assignment = {}
        for row in range(NROWS):
            for col in range(NCOLS):
                currCell = board[row][col]
                if currCell != 0: #if the cell is filled, assign that value to the dictionary
                    assignment[(row, col)] = [currCell]
                else: #otherwise, assign all values in the domain to the dictionary
                    assignment[(row, col)] = DOMAIN
        return assignment

    def solveSudoku(self, solverMode, variableChoice):
        '''wrapper function that interprets which algorithm to use. Takes in a
        constraint satisfaction problem and an algorithm to use (b (basic), f
        (forward-checking), or m (MAC)) as input and returns assignments for all
        the variables (as a dictionary) and number of nodes expanded'''
        if solverMode == 'p': #AC3 as pre-processing
            worklist = set()
            for key in neighbors.keys():
                for value in neighbors[key]:
                    worklist.add((key, value))
                    worklist.add((value, key))
            if self.AC3(worklist):
                assignment = self.recursiveBacktrack('b', variableChoice)
            else:
                assignment = False
        else:
            assignment = self.recursiveBacktrack(solverMode, variableChoice)

        return (assignment, self.nodesExpanded)

    def recursiveBacktrack(self, solverMode, variableChoice):
        '''recursive helper for backtracking-search().
        Returns null if there is no solution for the given assignments, returns the solution otherwise'''
        self.nodesExpanded += 1
        # if self.nodesExpanded % 20000 == 0:
        #     print(self.nodesExpanded)
        # if self.nodesExpanded >= 500000:
        #     print(">500,000")
        #     return False
        assignment = self.assignment
        if self.isComplete():
            return assignment
        else:
            var = self.chooseVar(variableChoice)

            oldAssign = copy.deepcopy(assignment) #store a copy of current assignment

            for val in oldAssign[var]:
                if self.consistent(var, val): #if a value is consistent with constraints
                    assignment[var] = [val] #assign the value to the cell
                    self.game.addToGame(var, val)
                    if self.imposeConsistency(solverMode, var):

                        result = self.recursiveBacktrack(solverMode, variableChoice) #recurse

                        if result != False: #if the subtree finds a solution, return it
                            return result


                    self.game.removeFromGame(var) #otherwise un-assign the value and try again
                    self.assignment = copy.deepcopy(oldAssign)
                    assignment = self.assignment
        return False #FAIL


    def chooseVar(self, VariableChoice):
        if VariableChoice == 'm':
            return self.MRV()
        if VariableChoice == 'r':
            return self.randomVar()
        if VariableChoice == 'o':
            return self.varInOrder()
        else:
            print("what the heck how did you even get here. bad")
            return



    def allDiff(self, cellArray):
        '''Takes in an array of 9 values as input and checks if they are all different.
        0s are treated as empty values (not checked for differences).
        Returns True if they are, False otherwise. Note: values must be 1-9'''
        valsSeen = array.array('l', [0]*9)
        for val in cellArray:
            if val != 0: #if the cell is filled
                index = val - 1
                if valsSeen[index] != 0:
                    return False
                else:
                    valsSeen[index] = 1
        return True

    def isComplete(self):
        '''checks if all of the cells in the puzzle have been filled (aka, assigned
        a value)'''
        for row in range(NROWS):
            for col in range(NCOLS):
                if self.game.puzzle[row][col] == 0:
                    return False
        return True

    def consistent(self, var, val):
        ''' Checks that assignment of variable var does not violate Sukodu's constraints '''
        row = self.game.getRow(var[0]).copy() #make a copy of the values in the current row
        row[var[1]] = val #assign the new value to the row


        col = self.game.getCol(var[1]).copy() #repeat with column
        col[var[0]] = val

        box = self.game.getBox(var[0], var[1]).copy() #repeat with box
        index = ((var[0]%3)*3) + ((var[1]%3))
        box[index] = val


        # return whether all the values are different
        return self.allDiff(row) and self.allDiff(col) and self.allDiff(box)

    ### TODO: Think about implementing highest degree variable tie breaker
    def MRV(self):
        '''minimum remaining values, a variable order heuristic. Returns the variable
        with the fewest options left in its domain. Breaks ties arbitrarily '''
        assignment = self.assignment
        minSoFar = ()
        minLen = 9
        for key in assignment.keys():
            if len(assignment[key]) <= minLen:
                if (len(assignment[key]) == 1) and (self.game.getCell(key) == 0):
                    return key
                elif (len(assignment[key]) > 1):
                    minSoFar = key
                    minLen = len(assignment[key])
        return minSoFar

    def randomVar(self):
        '''chooses a random unassigned variable'''
        assignment = self.assignment
        var = (random.choice(range(9)), random.choice(range(9)))
        while len(assignment[var]) <= 1: #if the variable is already assigned, choose a new one
            var = (random.choice(range(9)), random.choice(range(9)))
        return var

    def varInOrder(self):
        '''from the bottom right corner of the board to the top left corner, selects
        the first unassigned variable'''
        for row in range(8, -1, -1): #from 8-0
            for col in range(8, -1, -1):
                var = (row, col)
                if self.game.getCell(var) == 0:
                    return var

    ###TODO
    def orderByLCV(self, var):
        '''least constraining value, a value order heuristic. Given a variable and a CSP,
        re-orders the Availablevalues for that variable in assignment from most constraining to least constraining
         the values in the variables domain that rules out the fewest values for
        neighboring variables '''
        #numConstraints = dictionary with (value, number of constraints) pairs

        #for each variable in the variable's row:
            #for value in assignment[var]:
                #if the value is in that variable's possible domains:
                    #add one to numConstraints[val]
        #also do for column
        #also do for the cells in the box (that aren't in the same row/column)

        #sort the values by lowest value in numConstraints to highest
        #make this sorted list the new value of assignment[var]

    def imposeConsistency(self, solverMode, var):
        if solverMode == 'b':
            return True

        if solverMode == 'f':
            worklist = self.makeWorkList(var)
            return self.forwardChecking(worklist)

        if solverMode == 'm':
            worklist = self.makeWorkList(var)
            return self.AC3(worklist)

    ###TODO
    def arcReduce(self, X, Y):
        '''helper function for AC3. Imposes arc consistency on the relation from X to Y'''

        reduced = False

        assignment = self.assignment
        domainX = copy.deepcopy(assignment[X]) #list of values that X can be
        options = copy.deepcopy(domainX)
        for x in options:
            consistent = False
            for y in assignment[Y]:
                if y != x:
                    consistent = True
            if not consistent:
                # print("X's domain was ", domainX)
                # print("notconsistent")
                domainX.remove(x)
                assignment[X] = domainX
                # assignment[X].remove(x)
                # print("now it is ", domainX)
                reduced = True
        return reduced

    ###TODO
    def AC3(self, worklist):
        '''implements constraint propogation and updates the domains of all the variables'''
        # get the neighbors of the value, add them to set as pair with value
        # Make a set that has pairs of tuples
        # print(worklist)
        assignment = self.assignment
        while len(worklist): # while worklist is not empty
            X, Y = worklist.pop() # choose a pair of cells
            if self.arcReduce(X, Y): # it reduced something
                # print("REDUCED", assignment[X])
                # print(neighbors[X])
                if len(assignment[X])==0:
                    return False
                for Z in neighbors[X]:
                    if (Z != Y):
                        worklist.add((Z,X))
        return True # Success

    def makeWorkList(self, key):
        worklist = set()
        for y in neighbors[key] :
            worklist.add((y, key))
        # print(worklist)
        return worklist


    def forwardChecking(self, worklist):
        '''implements constraint propogation and updates the domains of all the variables'''
        # get the neighbors of the value, add them to set as pair with value
        # Make a set that has pairs of tuples
        assignment = self.assignment
        while len(worklist): # while worklist is not empty
            X, Y = worklist.pop() # choose a pair of cells
            if self.arcReduce(X, Y):
                if len(assignment[X]) == 0:
                    return False
        return True # Success

import array
import copy
import json
from neighborDict import neighbors

# Global variables
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
NROWS = 9
NCOLS = 9

##Check that domain of everything in assignment is always 9 when we arrive to it

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

    def backtrackingSearch(self):
        '''Takes in a constraint satisfaction problem as input and returns assignments
        for all the variables (as a dictionary)'''
        # return self.recursiveBacktrack(self.assignment
        assignment = self.recursiveBacktrack()
        return (assignment, self.nodesExpanded)


    def recursiveBacktrack(self):
        '''recursive helper for backtracking-search().
        Returns null if there is no solution for the given assignments, returns the solution otherwise'''
        self.nodesExpanded += 1
        assignment = self.assignment
        if self.isComplete():
            return assignment
        else:
            var = self.MRV() #choose a cell to assign using MRV heuristic

            #self.orderByLCV(var) #order values for var using LCV heuristic
            oldAssign = copy.deepcopy(assignment) #store a copy of current assignment

            for val in oldAssign[var]:
                if self.consistent(var, val): #if a value is consistent with constraints
                    assignment[var] = [val] #assign the value to the cell
                    self.game.addToGame(var, val)
                    result = self.recursiveBacktrack() #recurse

                    if result != False: #if the subtree finds a solution, return it
                        return result
                    else:
                        self.game.removeFromGame(var) #otherwise un-assign the value and try again
                        self.assignment = copy.deepcopy(oldAssign)
                        assignment = self.assignment
        return False #FAIL

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
        index = ((var[0]%3)+1) * ((var[1]%3)+1) -1
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
            if len(assignment[key]) <= minLen and len(assignment[key]) > 1:
                minSoFar = key
                minLen = len(assignment[key])
        return minSoFar

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

    ###TODO
    def arcReduce(self, CSP, X, Y):
        '''helper function for AC3. Imposes arc consistency on the relation from X to Y'''
        return 0
        #pseudocode in notes

    ###TODO
    def AC3(self, CSP):
        '''implements constraint propogation and updates the domains of all the variables'''
        return 0
        #pseudocode in notes

    ###TODO
    def MAC(self, CSP):
        '''Maintaining Arc Consistency. Alternates between interleave search and AC3.
        I think this is an alternative to backtracking-search? not super sure'''
        #instead of checking consistency with csp.constraints, impose arc-consistency w AC3
        # then run MACtracking (recursive backtracking) again

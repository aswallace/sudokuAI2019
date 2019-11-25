# Global variables 
DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
NROWS = 9
NCOLS = 9

import array
import copy

###TODO: integrate with sudoku.py
class SudokuSolver:
    def __init__(self, sudokuGame):
        self.game = sudokuGame
        self.assignment = self.makeAssignment(sudokuGame.start_puzzle)
    
    def makeAssignment(self, board):
        assignment = {}
        for row in range(NROWS):
            for col in range(NCOLS):
                currCell = board[row][col]
                if currCell != 0:
                    assignment[(row, col)] = [currCell]
                else:
                    assignment[(row, col)] = DOMAIN
        return assignment
    

    def allDiff(self, cellArray):
        '''Takes in an array of 9 values as input and checks if they are all different.
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
        # return self.recursiveBacktrack(self.assignment)
        return self.recursiveBacktrack()


    def recursiveBacktrack(self):
        '''recursive helper for backtracking-search().
        Returns null if there is no solution for the given assignments, returns the solution otherwise'''
        assignment = self.assignment
        #if self.isComplete(assignment): # check if assignment is complete
        if self.isComplete(): 
            return assignment
        else:
            var = self.MRV(assignment)
            # print("var: ", var)
            oldAssign = copy.deepcopy(assignment[var])
            options = oldAssign.copy() # to avoid skipping options
          #  oldAssign = self.LCV(oldAssign) #TODO: Order values in old assignment of var
            for val in options:
                if self.consistent(var, val):
                    assignment[var] = [val]
                    self.game.addToGame(var, val)
                    result = self.recursiveBacktrack() #REmember yiouc ahnged this
                    if result != False:
                        return result
                    # print("found result for", var)
                    else:
                #     print("removing val")
                        oldAssign.remove(val)
                        assignment[var] = oldAssign
                        self.game.removeFromGame(var)
            return False  #TODO: Do we need this? PROF ERIN

        return False #FAIL

    ### TODO: Optimize this
    # def isComplete(self, assignment):
    #     '''checks if every variable in assignment has only 1 value assigned'''
    #     for key in assignment.keys():
    #         if len(assignment[key]) > 1:
    #             print("key is", key)
    #             print(assignment[key])
    #             return False
    #     return True 

    def isComplete(self): 
        for row in range(9): 
            for col in range(9): 
                print('current row', row, 'current col', col, 'value!', self.game.puzzle[row][col])
                if self.game.puzzle[row][col] == 0: 
                    return False
        return True 

    ### TODO: game object does not seem to be updated with the assignment
    def consistent(self, var, val):
        ''' Checks that assignment of variable var does not violate CSP constraints '''
        # print("In consistent: ", var, val)
        row = self.game.getRow(var[0]).copy()
        row[var[1]] = val
        print("row is ", row)
        col = self.game.getCol(var[1]).copy()
        col[var[0]] = val
        print("col is ", col)
        box = self.game.getBox(var[0], var[1]).copy()
        index = ((var[0]%3)+1) * ((var[1]%3)+1) -1
        box[index] = val
        print("box is ", box)
        return self.allDiff(row) and self.allDiff(col) and self.allDiff(box)

    ### TODO: Think about implementing highest degree variable tie breaker
    def MRV(self, assignment):
        '''minimum remaining values, a variable order heuristic. Returns the variable
        with the fewest options left in its domain. Breaks ties arbitrarily '''
        minSoFar = ()
        minLen = 9
        for key in assignment.keys():
            if len(assignment[key]) <= minLen and len(assignment[key]) > 1:
                minSoFar = key
                minLen = len(assignment[key])
        return minSoFar

    ###TODO
    def LCV(self, oldAssign):
        '''least constraining value, a value order heuristic. Given a variable and a CSP,
        returns the value in the variables domain that rules out the fewest values for 
        neighboring variables '''
        return oldAssign

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



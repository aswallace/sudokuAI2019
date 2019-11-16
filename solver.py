# AI sudoku solver goes here
# DOMAIN = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# NROWS = 9
# NCOLS = 9

import array



####TODO: make this into a class, which takes in puzzle/problem as argument

def allDiff(cellArray):
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

#todo; put these in the sudoku file 
def getRow(row):
    '''given a row index, returns the values of all the cells in that row'''
    return 0

def getCol(col):
    '''given a column index, returns the values of all the cells in that row'''
    return 0

def boxNumber(row, col):
    '''given the row and column of a cell, returns which 3x3 box that cell is part of'''
    return (col//3) + 1 + (row//3)*3


def getBox(boxNumber):
    '''given the number of a box, returns the value of all the cells in the box'''
    return 0




def backtrackingSearch(CSP):
    '''Takes in a constraint satisfaction problem as input and returns assignments
    for all the variables (as a dictionary)'''
    return recursiveBacktrack(CSP, {})
    #pseudocode in notes


def recursiveBacktrack(CSP, assignment):
    '''recursive helper for backtracking-search().
    Returns null if there is no solution for the given assignments, returns the solution otherwise'''
    return 0
    #pseudocode in notes

def MRV():
    '''minimum remaining values, a variable order heuristic. Returns the variable
    with the fewest options left in its domain. Breaks ties by returning the highest
    degree variable (the most connected variable) '''
    return 0


def LCV(CSP, variable):
    '''least constraining value, a value order heuristic. Given a variable and a CSP,returns the value in the variables domain that rules out the fewest values for neighboring variables '''
    return 0



def arcReduce(CSP, X, Y):
    '''helper function for AC3. Imposes arc consistency on the relation from X to Y'''
    return 0
    #pseudocode in notes


def AC3(CSP):
    '''implements constraint propogation and updates the domains of all the variables'''
    return 0
    #pseudocode in notes


def MAC(CSP):
    '''Maintaining Arc Consistency. Alternates between interleave search and AC3.
    I think this is an alternative to backtracking-search? not super sure'''
    #instead of checking consistency with csp.constraints, impose arc-consistency w AC3
    # then run MACtracking (recursive backtracking) again

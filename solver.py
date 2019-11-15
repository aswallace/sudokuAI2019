# AI sudoku solver goes here



def backtracking-search(CSP):
    '''Takes in a constraint satisfaction problem as input and returns assignments
    for all the variables (as a dictionary)'''
    return recursive-backtrack(CSP, {})
    #pseudocode in notes


def recursive-backtrack(CSP, assignment):
    '''recursive helper for backtracking-search().
    TODO: docstring'''
    return 0
    #pseudocode in notes

def MRV():
    '''minimum remaining values, a variable order heuristic. Returns the variable
    with the fewest options left in its domain. Breaks ties by returning the highest
    degree variable (the most connected variable) '''
    return 0




def LCV(CSP, variable):
    '''least constraining value, a value order heuristic. Given a variable and a CSP,
    returns the value in the variables domain that rules out the fewest values for
     neighboring variables '''
     return 0



def arc-reduce(CSP, X, Y):
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

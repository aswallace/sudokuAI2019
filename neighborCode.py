cells = [(i,j) for i in range(9) for j in range(9)]

def makeNeighbors(cell):
    row, col = cell[0], cell[1]
    rowN = [(row, j) for j in range(9) if j != col]
    colN = [(i, col) for i in range(9) if i != row]
    boxN = [(i, j) 
            for i in range(3*(row//3), 3*(row//3)+3) 
            for j in range(3*(col//3), 3*(col//3)+3)
            if not(i == row and j == col)]
    assert(len(rowN) == len(colN) == len(boxN) == 8)
    neighbors = set(rowN + colN + boxN)
    assert(len(neighbors) == 20)
    return neighbors

neighborDict = {cell: makeNeighbors(cell) for cell in cells}

neighborFile = open("neighbors.txt", "w")
neighborFile.write(str(neighborDict))
neighborFile.close()
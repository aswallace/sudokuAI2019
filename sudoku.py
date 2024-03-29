# downloaded from http://newcoder.io/gui/part-4/

import argparse
import solver

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM


BOARDS = ['debug', 'n00b', 'l33t', 'error']  # Available sudoku boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board


class SudokuError(Exception):
    """
    An application specific error.
    """
    pass


### TODO: we want to change this to take in files of the form we want to input and parse those correctly
# not just take in things on the list
# TODO: add more flags for various arguments
def parse_arguments():
    """
    Parses arguments of the form:
        sudoku.py <board name>
    Where `board name` must be in the `BOARD` list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-b', "--board",
                            help="puzzle board file name", required=True)
    arg_parser.add_argument('-f', '--fileformat', default='w', help='File format. w=Warwick, s=sample')
    arg_parser.add_argument('-w', '--which', type=int, default=0, help='which line of puzzle you want to use (only applicable for Warwick puzzle file format)')
    arg_parser.add_argument('-a', '--ai', action='store_true', default=False, help='Solve puzzle with AI')

    #todo: check syntax
    arg_parser.add_argument('-s', '--solverMode', choices=['b', 'p', 'f', 'm'], default='b', help='Which form of backtracking search to use. b= basic search, p= with constraint propagation as pre-processing only, f=with forward-checking, m= MAC search')

    args = arg_parser.parse_args()
    return args


class SudokuUI(Frame):
    """
    The Tkinter UI, responsible for drawing the board and accepting user input.
    """
    def __init__(self, parent, game):
        self.game = game
        Frame.__init__(self, parent)
        self.parent = parent

        self.row, self.col = -1, -1

        self.__initUI()

    def __initUI(self):
        self.parent.title("Sudoku")
        self.pack(fill=BOTH)
        self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,
                              text="Clear answers",
                              command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in range(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]
                    color = "black" if answer == original else "sea green"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="victory",
            fill="white", font=("Arial", 32)
        )

    def __cell_clicked(self, event):
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE
            print("row, col", row, col, isinstance(row, float), isinstance(col, float))
            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row, self.col = row, col
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            self.game.puzzle[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.game.check_win():
                self.__draw_victory()

    def __clear_answers(self):
        self.game.start()
        self.canvas.delete("victory")
        self.__draw_puzzle()


class SudokuBoard(object):
    """
    Sudoku Board representation
    """
    def __init__(self, board_file, fileformat, which):
        self.board = self.__create_board(board_file, fileformat, which)

    def __create_board(self, board_file, fileformat, which):
        board = []
        if fileformat == 's':
            board = self.__sampleCreateBoard(board_file)
        elif fileformat == 'w':
            board = self.__warwickCreateBoard(board_file, which)
        else:
            raise SudokuError(
                "You dummy, you put in an invalid file format. Shame!"
            )
        return board


    def __warwickCreateBoard(self, board_file, which):
        '''board (list of lists) creator for files from warwick website. reads file
        until it gets to the desired line, populates the board, replaces empty cells with
        0 instead of .'''
        board = []

        #read to the correct line
        line = ''
        for i in range(which+1):
            line = board_file.readline()

        #populate the board with the desired puzzle
        for j in range(9):
            board.append([])

            for k in range(9):
                char = line[j*9 +k]
                if char == '.': #empty cells
                    board[-1].append(0)
                elif not char.isdigit(): #bad input :(
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9. Shame!"
                    )
                else: #numbers (filled cells)
                    board[-1].append(int(char))


        return board


    def __sampleCreateBoard(self, board_file):
        '''board (list of lists) creator for sample .sudoku files'''
        board = []
        for line in board_file:
            line = line.strip()
            if len(line) != 9:
                raise SudokuError(
                    "Each line in the sudoku puzzle must be 9 chars long."
                )
            board.append([])

            for c in line:
                if not c.isdigit():
                    raise SudokuError(
                        "Valid characters for a sudoku puzzle must be in 0-9"
                    )
                board[-1].append(int(c))

        if len(board) != 9:
            raise SudokuError("Each sudoku puzzle must be 9 lines long")
        return board


class SudokuGame(object):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board_file, fileformat, which):
        #self.board_file = board_file
        self.start_puzzle = SudokuBoard(board_file, fileformat, which).board

    def start(self):
        self.game_over = False
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])

    def check_win(self):
        for row in range(9):
            if not self.__check_row(row):
                return False
        for column in range(9):
            if not self.__check_column(column):
                return False
        for row in range(3):
            for column in range(3):
                if not self.__check_square(row, column):
                    return False
        self.game_over = True
        return True

    def __check_block(self, block):
        '''checks that the values are all between 1-9'''
        return set(block) == set(range(1, 10))

    def __check_row(self, row):
        return self.__check_block(self.puzzle[row])

    def __check_column(self, column):
        return self.__check_block(
            [self.puzzle[row][column] for row in range(9)]
        )

    def __check_square(self, row, column):
        return self.__check_block(
            [
                self.puzzle[r][c]
                for r in range(row * 3, (row + 1) * 3)
                for c in range(column * 3, (column + 1) * 3)
            ]
        )


    def getRow(self, row):
        '''given a row index, returns the values of all the cells in that row'''
        return self.puzzle[row]

    def getCol(self, col):
        '''given a column index, returns the values of all the cells in that row'''
        colList = []
        for i in range(9):
            colList.append(self.puzzle[i][col])
        return colList

    def getBox(self, row, col):
        '''given the row and column for a cell in the box, returns the value of all the cells in the box'''
        startCol = (col//3) * 3
        startRow = (row//3) *3
        boxList = []
        for i in range(3):
            for j in range(3):
                boxList.append(self.puzzle[startRow+ i][startCol+j])
        return boxList

    def solveSudoku(self, solverMode):
        '''Solve the puzzle and print the solution'''
        self.puzzle = []
        for i in range(9):
            self.puzzle.append([])
            for j in range(9):
                self.puzzle[i].append(self.start_puzzle[i][j])
        sudokuMan = solver.SudokuSolver(self)
        assignment, numExpanded = sudokuMan.solveSudoku(solverMode)
        if not assignment:
            print ("AAAAAAAAAAAAAAA dummy")
        else:
            for key in assignment.keys():
                row = key[0]
                col = key[1]
                self.puzzle[row][col] = assignment[key]
            self.printSolution(self.puzzle)
        return numExpanded

    def printSolution(self, puzzle):
        for row in range(9):
            rowStr = ""
            for col in range(9):
                rowStr += str(puzzle[row][col][0])
            print(rowStr)

    def addToGame(self, var, val):
        row = var[0]
        col = var[1]
        self.puzzle[row][col] = val

    def removeFromGame(self, var):
        row = var[0]
        col = var[1]
        self.puzzle[row][col] = 0





if __name__ == '__main__':
    args = parse_arguments()

    #TODO: add error handling
    boards_file = open(args.board)

    game = SudokuGame(boards_file, args.fileformat, args.which)

    if args.ai:
        numExpanded = game.solveSudoku(args.solverMode)
        print("Nodes Expanded: " + str(numExpanded))

    else:
        game.start()
        root = Tk()
        SudokuUI(root, game)
        root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
        root.mainloop()

import random
from copy import deepcopy


class Board:
    """
    Class to represent the board/grid of a Sudoku puzzle (Solution Space)
    """
    # Class Attribute which can be changed to affect the running of the code
    FILL = "random"
    FILL = "weighted"

    def __init__(self, vals):
        """
        initialiser function to set the value of the elements in the board and calculate the fitness
        :param vals:
        """
        # print("CREATE BOARD")
        self.brd = vals
        self.fitness = 0
        self.set_fitness()

    def __str__(self):
        """
        override the str function to cater for a more user-friendly output of board instances
        :return: string representation of the board instance
        """
        res = ""
        for row in self.brd:
            res = res + str(row) + "\n"
        return res

    def __lt__(self, other):
        """
        override the lt comparison function to allow two boards to be compared using the < operator
        this compares nboards via fitness
        :param other: the other board on the RHS of the < operator
        :return: boolean to represent whether the current fitness is less than the other boards fitness
        """
        return self.fitness < other.fitness

    def fill(self):
        """
        fill empty spaces in the board with values using one of 2 algorithms
        :return: Board instance of the filled board
        """
        if self.FILL == "random":
            return self.random_fill()
        elif self.FILL == "weighted":
            return self.weighted_random_fill()
        else:
            print("INCORRECT FILL CONSTANT ENTERED IN board.py")
            exit()

    def random_fill(self):
        """
        puts a random value between 0 and 8 in each blank space in the board
        :return: Board instance of the filled board
        """
        res = deepcopy(self.brd)
        for row in range(0, len(res)):
            for col in range(0, len(res)):
                # print(str(row) + " : " + str(col))
                if res[row][col] == 0:
                    res[row][col] = random.randint(1, 9)
        return Board(res)

    def weighted_random_fill(self):
        """
        fills blank spaces with a value that isnt already used in that row, col or 3x3 box
        any blanks that cannot be filled are filled with a random value between 0 and 8
        :return: Board instance of the filled board
        """
        # find a value that is not in the row, col or box
        res = deepcopy(self.brd)
        for row in range(0, len(res)):
            for col in range(0, len(res[row])):
                if res[row][col] == 0:
                    used = self.collate_vals(res, row, col)
                    valid = []
                    for val in range(0, 9):
                        if val not in used:
                            valid.append(val)
                    # print( str(row) + " : " + str(col) + " SET " + str(used))
                    if len(valid) >= 1:
                        res[row][col] = random.choice(valid)
                        break
        return Board(res).random_fill()

    def collate_vals(self, board, row, col):
        """
        returns a set of values that are already used in the row, column and 3x3 box
        of the tile which is at the row,col coordinates of the board
        :param board: board layout passed in
        :param row: integer row the tile is in
        :param col: integer column the tile is in
        :return: set of integers between 8 and 0
        """
        # create set of used values in the row, col and box of that coordinate
        res = set()
        # elems in the row
        for val in board[row]:
            res.add(val)
        # elems in the col
        for row in range(0, len(board)):
            res.add(board[row][col])
        # elems in the box
        tmpx = row
        tmpy = col
        while tmpx % 3 != 0:
            tmpx -= 1
        while tmpy % 3 != 0:
            tmpy -= 1
        box = self.get_3x3_boxes((tmpx, tmpy))
        for val in box:
            res.add(val)
        return res

    def get_3x3_boxes(self, box):
        """
        returns a 3x3 box that contains the element in the coordinates passed in via 'box'
        :param box: the coordinates of the top left element of the box to get elements from
        :return: an array of values in the box
        """
        tmp_row = []
        for row in range(box[0], box[0] + 3):
            for col in range(box[1], box[1] + 3):
                tmp_row.append(self.brd[row][col])
        return tmp_row

    def get_all_boxes(self):
        """
        returns an array of all the boxes in the board
        :return: an array of arrays for each box, with inside arrays holding values in each box (2D array)
        """
        res = []
        starts = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]
        for box in starts:
            res.append(self.get_3x3_boxes(box))
        return res

    def set_fitness(self):
        """
        calculates the fitness of the board and sets the self.fitness attribute to this value
        :return: None
        """
        # print("SET FITNESS")
        row_fitness = 0
        col_fitness = 0
        box_fitness = 0

        # LOOK AT EACH ROW
        # STORE EACH ELEMENT IN A SET
        for row in self.brd:
            tmp_set = set()
            for num in row:
                tmp_set.add(num)
            row_fitness += len(tmp_set)

        for col in range(0, len(self.brd)):
            tmp_set = set()
            for row in self.brd:
                tmp_set.add(row[col])
            col_fitness += len(tmp_set)

        boxes = self.get_all_boxes()
        for box in boxes:
            tmp_set = set()
            for num in box:
                tmp_set.add(num)
            box_fitness += len(tmp_set)

        self.fitness = (((col_fitness + row_fitness + box_fitness) / 3 )/81)*100

    def mutate(self):
        """
        decides whether to mutate the current board, and if so, swaps 2 random elements in a random row
        :return: None
        """
        # print("MUTATE")
        # DECIDE WHETHER TO MUTATE THE CHILD
        rate = 0.2
        if random.uniform(0, 1) < 0.2:

            # pick a row in the board, and within that, pick 2 values to swap
            row = random.randint(0, 8)
            v1 = v2 = 0
            while v1 == v2:
                v1 = random.randint(0, 8)
                v2 = random.randint(0, 8)

            new_brd = deepcopy(self.brd)
            new_brd[row][v1] = self.brd[row][v2]
            new_brd[row][v2] = self.brd[row][v1]
            # print("MUTATED " + str((self.brd == new_brd)) + " ROW " + str(row))
            self.brd = new_brd

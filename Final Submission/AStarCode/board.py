# Import the deepcopy function from the copy library
from copy import deepcopy


class Board:
    """
    Class to represent a Board in the 8-Puzzle
    """
    # Class Variable to set the choice of algorithm
    algo = ""


    def __init__(self, elems):
        """
        the init function initialises the board object and sets the 'brd' attribute to the passed in 2D array
        :param elems: A 2D array of elements for the board
        """
        self.brd = elems

    def __eq__(self, other):
        """
        overriding the 'eq' function to allow two boards to be compared via the 'brd' attribute only
        :param other: a Board instance of the board to compare this board with
        :return: return a boolean of whether the two boards are equal or not
        """
        return self.brd == other.brd

    def locate(self, num):
        """
        function to find a value in the board and return its coordinates
        :param num: The number to find in the board
        :return: a tuple containing the row and col location of the value in question
        """
        # for reach row
        for row in range(0, len(self.brd)):
            # for each col
            for col in range(0, len(self.brd[row])):
                if self.brd[row][col] == num:
                    # if the value at that row and col combination, return these row and col values
                    return (row, col)

    def get_heuristic(self, goal):
        """
        calls the correct heuristic function based on the heuristic algorithm selected to use
        :param goal: the goal state of the node
        :return: an integer returned by the heuristic function
        """
        if self.algo == "Hamming":
            # If the 'algo' is Hamming, call the get_heuristic_hamming function
            return self.get_heuristic_hamming(goal)
        elif self.algo == "Manhattan":
            # otherwise, if 'algo' is Manhattan, call the get_heuristic_manhattan function
            return self.get_heuristic_manhattan(goal)
        else:
            # otherwise, there is an error, exit the code in this case
            print("NOT A VALID HEURISTIC ALGORITHM")
            exit(1)

    def get_heuristic_hamming(self, goal):
        """
        uses the hamming method to return a value for the heuristic of the node
        :param goal: the goal state of the node
        :return: an integer which is the heuristic
        """
        # set the heuristic to 0
        heuristic = 0
        # iterate through each element of the goal board
        for row in range(0, len(goal.brd)):
            for col in range(0, len(goal.brd[row])):
                # if the tile in each position is out of place and not the blank tile, then increment the heuristic
                if goal.brd[row][col] != self.brd[row][col] and goal.brd[row][col] != 0:
                    heuristic += 1
        # return the heuristic
        return heuristic

    def get_heuristic_manhattan(self, goal):
        """
        uses the manhattan method to return a value for the heuristic of the node
        :param goal: the goal state of the node
        :return: an integer which is the heuristic
        """
        # set the heuristic to 0
        heuristic = 0

        # for each tile possibility
        for num in range(0, 9):
            # find the coordinates of this value in the current board and the goal board
            current_loc = self.locate(num)
            goal_loc = goal.locate(num)
            # generate the distance using the manhattan method formula, and add this to the heuristic
            heuristic += (abs(current_loc[0] - goal_loc[0]) + abs(current_loc[1] - goal_loc[1]))
        # return the heuristic
        return heuristic

    def swap(self, blank, tile):
        """
        function to swap two elements in the board
        :param blank: coordinates of the blank tile
        :param tile: coordinates of the tile to swap it with
        :return: the resulting board instance
        """
        # make a deep copy of the board of this object
        res = deepcopy(self.brd)
        # print(str(res[blank[0]][blank[1]]) + "<->" + str(res[tile[0]][tile[1]]))
        # set the blank tile to the value of the 2nd tile
        res[blank[0]][blank[1]] = res[tile[0]][tile[1]]
        # set the value of the 2nd tile to a 0 (making it a blank tile)
        res[tile[0]][tile[1]] = 0
        # return the resulting board instance
        return Board(res)

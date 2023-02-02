# Import the deepcopy function from the copy library
from copy import deepcopy

class Node:
    """
    Class to represent a node in the 8-Puzzle Game
    """

    def __init__(self, board, goal, g, path, initial=False):
        """
        the init function initialises the Node object and generates h, g, and f values
        :param board: The Board to represent the current layout of the 8-Puzzle
        :param goal: The Board to represent the Goal State of the puzzle
        :param g: The cost of the node that this Node is the child of
        :param path: The Path used to reach this node
        :param initial: A Boolean to specify this is the root node, if so, a different instantiation approach is taken
        """
        # Instantiate Attributes using passed in variables
        self.board = board
        self.goal = goal
        self.path = deepcopy(path)
        # If this node is the root node, then the h, g and f values would be set to 0
        if initial:
            self.g = self.h = self.f = 0
        # If the node is not a root node, then set calculate the h, g and f values as below
        else:
            # The g value would be the g value passed in, incremented
            # g is the cost from the start node to the current node
            self.g = g + 1
            # the h value would be generated using the get_heuristic method of the board object
            self.h = self.board.get_heuristic(goal)
            # the f value would be the sum of the g and h values
            self.f = self.g + self.h

    def __eq__(self, other):
        """
        overriding the 'eq' function to allow two Nodes to be compared via the 'board' attribute only
        :param other: a Node instance of the node to compare this node with
        :return: return a boolean of whether the two boards are equal or not
        """
        return self.board == other.board

    def is_goal(self):
        """
        method to check if the Node is equal to the goal
        :return: A Boolean of whether the board of this node is equal to the goal board
        """
        return self.board == self.goal

    def get_successors(self):
        """
        method to generate all the valid successors of the current node
        :return: an array of Nodes which are the successors of the current node
        """
        # create two empty lists, 'res' and 'points'
        res = []
        points = []
        # locate the blank tile in the board using the Boards locate method
        blank = self.board.locate(0)
        # Consider 4 possible moves for the blank tiles and if the move is possible and valid, then append the new point
        # to the points list
        if blank[0] > 0:
            points.append((blank[0] - 1, blank[1]))
        if blank[0] < 2:
            points.append((blank[0] + 1, blank[1]))
        if blank[1] > 0:
            points.append((blank[0], blank[1] - 1))
        if blank[1] < 2:
            points.append((blank[0], blank[1] + 1))

        # Iterate through all the points
        for point in points:
            # create a deepcopy of the current board
            new_path = deepcopy(self.path)
            # swap the tile and the point from the points list in this copied board
            new_path.append((0, self.board.brd[point[0]][point[1]]))
            # use this board and attributes of the current board to instantiate a new Node
            # append this new Node to the res list
            res.append(Node(self.board.swap(blank, point), self.goal, self.g, new_path))
        # return 'res' the array of successor nodes
        return res

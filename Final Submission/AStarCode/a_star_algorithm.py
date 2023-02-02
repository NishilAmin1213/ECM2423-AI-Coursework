# Import the Node and Board Classes from their respective files
import time
from node import Node
from board import Board

def get_smallest_val(array):
    """
    get_smallest_val is a function which takes an array of nodes and returns the node with the smallest f value
    :param array: array containing nodes
    :return: min_node - the smallest node in the array
    """
    # Assume the first element to be the smallest node
    min_node = array[0]
    # Iterate through the elements of the array
    for node in array:
        # if an element has a smaller f value than the current min node, set the new minimum node to the current node
        if node.f < min_node.f:
            min_node = node
    # the smallest node would be stored in min_node, return this node
    return min_node

def a_star(start_board, goal_board, algo):
    """
    a_star is a function which takes a start and goal board layout and uses the implemented A* algorithm to
    find the shortest number of moves to reach this goal.
    :param start_board: A 2D Array containing values for the start board
    :param goal_board: A 2D Array containing values for the goal board
    :return: An array is returned containing the individual moves required to get from the start to goal node
    """

    #Start Time
    st = time.time()

    # Set the global 'algo' variable of board to the passed in algorithm string
    Board.algo = algo

    # Instantiate the Open and Closed List
    open_list = []
    closed_list = []

    # Create the starting node and append this to the open_list
    open_list.append(Node(Board(start_board), Board(goal_board), 0, [], True))

    # set a counter to count the number of loops used (measurement of comparison which is not affected by hardware)
    counter = 0
    # while there are elements in the open_list do the following
    while len(open_list) > 0:
        # increment counter
        counter += 1
        print(counter)

        # get the node in open_list with the smallest f value and store it in current
        current = get_smallest_val(open_list)
        # remove 'current' from the array
        open_list.remove(current)

        # check if this node is the goal
        if current.is_goal():
            # store the path in an array 'res'
            moves = []
            for move in current.path:
                moves.append(move[1])
                # if the current node is the goal output a string with some basic information
            print("reached goal after " + str(current.g) + " moves, using " + str(counter) + " while loops on open_list")
            print(moves)

            # prepend the current nodes cost (g) and counter of loops to the moves array (for reference in calling code)
            res = [current.g, counter] + moves
            # return this 'res' array with information regarding the solution

            # End Time
            print("--- %s seconds ---" % (time.time() - st))

            return res

        # find all successors of the current node
        successors = current.get_successors()

        # for each successor node
        for node in successors:

            # look for this node in closed list
            # set found token to False
            found = False
            # look at each element in closed_list
            for elem in closed_list:
                # if the current element in the list has the same board as node, then set 'found' to true
                if node == elem:
                    found = True
            # if the successor was found in closed list, skip the rest of the loop for this successor
            # i.e. - discard the successor
            if found:
                continue

            # look for this node in open_list,
            # 'found' does not need to be set to false as reaching here implies it already is
            for elem in open_list:
                # if an element in open_list is found with the same board
                if elem == node:
                    # and this element has a greater cost (g) than the successor
                    if elem.g > node.g:
                        # then remove the element from open_list (the successor will later be added to open_list)
                        open_list.remove(elem)
                    else:
                        # if this element has not got a greater cost than the successor
                        # then, set found to true
                        found = True
            # if the successors board wasn't found in open_list (or is not in open_list anymore)
            if not found:
                # append the successor to open_list
                open_list.append(node)

        # append the current node which was removed from open_list, to closed_list as it has now been searched
        closed_list.append(current)

    # if the code reaches here, assume the problem is unsolvable, and return an empty list
    # End Time
    print("--- %s seconds ---" % (time.time() - st))
    return []

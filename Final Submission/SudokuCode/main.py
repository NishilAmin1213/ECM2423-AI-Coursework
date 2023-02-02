from board import *
import numpy

grid1 = [[3, 0, 0, 0, 0, 5, 0, 4, 7], [0, 0, 6, 0, 4, 2, 0, 0, 1], [0, 0, 0, 0, 0, 7, 8, 9, 0], [0, 5, 0, 0, 1, 6, 0, 0, 2], [0, 0, 3, 0, 0, 0, 0, 0, 4], [8, 1, 0, 0, 0, 0, 7, 0, 0], [0, 0, 2, 0, 0, 0, 4, 0, 0], [5, 6, 0, 8, 7, 0, 1, 0, 0], [0, 0, 0, 3, 0, 0, 6, 0, 0]]
grid2 = [[0, 0, 2, 0, 0, 0, 6, 3, 4], [1, 0, 6, 0, 0, 0, 5, 8, 0], [0, 0, 7, 3, 0, 0, 2, 9, 0], [0, 8, 5, 0, 0, 1, 0, 0, 6], [0, 0, 0, 7, 5, 0, 0, 2, 3], [0, 0, 3, 0, 0, 0, 0, 5, 0], [3, 1, 4, 0, 0, 2, 0, 0, 0], [0, 0, 9, 0, 8, 0, 4, 0, 0], [7, 2, 0, 0, 4, 0, 0, 0, 9]]
grid3 = [[0, 0, 4, 0, 1, 0, 0, 6, 0], [9, 0, 0, 0, 0, 0, 0, 3, 0], [0, 5, 0, 7, 9, 6, 0, 0, 0], [0, 0, 2, 5, 0, 4, 9, 0, 0], [0, 8, 3, 0, 6, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0, 7], [0, 0, 0, 9, 0, 3, 0, 7, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0, 1, 0]]
example = [[5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0], [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6], [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]]

# CONSTANTS WHICH CAN BE CHANGED TO MODIFY THE RUNNING OF THE CODE
POPULATION_SIZE = 10000
SELECTION = "fittest"
SELECTION = "roulette"
# THE GRID TO USE IN THE SOLUTION CAN BE CHANGED HERE
start = example


def get_fittest(my_list):
    """
    Function to take in a list of board instances and return the board with the greatest fitness
    :param my_list: list of board instances
    :return: a board instance which has the highest fitness
    """
    # print("GET FITTEST")
    fittest = my_list[0]
    for board in my_list:
        if board.fitness > fittest.fitness:
            fittest = board
    return fittest


def select_parents(population):
    """
    calls the respective selection algorithm and returns its value
    :param population: array containing all the board instances - the whole population
    :return: a tuple with the 2 parent nodes that have been selected
    """
    if SELECTION == "fittest":
        return select_parents_fittest(population)
    elif SELECTION == "roulette":
        return select_parents_roulette(population)
    else:
        print("INCORRECT SELECTION CONSTANT ENTERED IN main.py")
        exit()


def select_parents_roulette(population):
    """
    uses the roulette method to select 2 parents from the population
    :param population: array containing all the board instances - the whole population
    :return: a tuple with the 2 parent nodes that have been selected
    """
    # print("SELECT PARENTS")
    total_fitness = 0
    for board in population:
        total_fitness += board.fitness

    board_probs = []
    for board in population:
        board_probs.append(board.fitness/total_fitness)

    return numpy.random.choice(population, p=board_probs), numpy.random.choice(population, p=board_probs)


def select_parents_fittest(population):
    """
    gets the 2 fittest board instances from the population and returns these
    :param population: array containing all the board instances - the whole population
    :return: a tuple with the 2 parent nodes that have been selected
    """
    #print("SELECT PARENTS")
    tmp = deepcopy(population)
    b1 = get_fittest(tmp)
    tmp.remove(b1)
    b2 = get_fittest(tmp)
    return b1, b2


def combine(board1, board2):
    """
    the CROSSOVER function which takes two board instances and returns the child board before mutation
    :param board1: one of the parent boards
    :param board2: another on of the parent boards
    :return: a new board instance which is made of a combination of the two parents
    """
    # 1 - swap a randomly selected subset of rows
    # 2 - swap a randomly selected subset of columns
    # 3 - swap a randomly selected subset of 3x3 boxes
    subset = random.randint(1, 3)
    marker = random.randint(0, 8)
    res = []
    if subset == 1:
        # print("ROW CROSSOVER")
        # 1 - swap a randomly selected subset of rows

        res += (board1.brd[0:marker])
        res += (board2.brd[marker:len(board1.brd)])
    elif subset == 2:
        # 2 - swap a randomly selected subset of columns
        # print("COL CROSSOVER")
        for row in range(0, 9):
            res_row = []
            for col in range(0, 9):
                if col <= marker:
                    res_row.append(board1.brd[row][col])
                else:
                    res_row.append(board2.brd[row][col])
            res.append(res_row)
    else:
        # print("BOX CROSSOVER")
        # 3 - swap a randomly selected subset of 3x3 boxes
        b1_boxes = board1.get_all_boxes()
        b2_boxes = board1.get_all_boxes()
        res += (b1_boxes[0:marker])
        res += (b2_boxes[marker:len(b2_boxes)])

    return Board(res)

"""
This main block of code carries out the iterations of the genetic algorithm until a solution is found
"""
# Create the start board
game = Board(start)
# declare an array for the population
population = []
# fill this population array with the max number of boards
for i in range(POPULATION_SIZE):
    population.append(game.fill())

# printout information to the console
print("START CODE HERE")
print(population[0])
print("Start Fitness - " + str(population[0].fitness))

# set a counter for the number of generations
gens = 0

found = False
while not found:

    # Get the best half of the population
    population.sort()
    population.reverse()
    population = population[:len(population)//2]

    # output the best fitness achieved so far
    best_fitness = str(get_fittest(population).fitness)
    # increment generations
    gens += 1
    print("Generation " + str(gens) + ", Best Fitness - " + best_fitness)

    # Select 2 parents
    # This is done by the function defined at the top
    parents = select_parents(population)

    # while the population isnt at max capacity, create new children to fill it
    while len(population) < POPULATION_SIZE:
        # RECOMBINE PAIRS OF PARENTS (CROSSOVER)
        child = combine(parents[0], parents[1])
        # MUTATE THE CHILD - THIS HAPPENS WITH A CERTAIN PROBABILITY
        child.mutate()
        # Append this child to the population
        population.append(child)

        # check if this child is the solution
        if child.fitness == 100:
            print("FOUND SOLUTION")
            print(child)
            found = True

exit()
from functools import partial
from tkinter import *
from tkinter import messagebox
from a_star_algorithm import a_star
import os


def check_validity(input_board):
    """
    check_validity is a function which ensures that the 2D Array representation of the board taken in from the user
    is of a valid format
    * There are numbers 0, 1, 2, 3, 4, 5, 6, 7 and 8
    * There are NO blank spaces
    * There are NO repeating values
    :param input_board: 2D Array of board taken in from the user
    :return: Boolean to notify the calling function whether the board is valid or not
             * True - Valid Input
             * False - Invalid Input
    """
    # check to see that all required numbers are in the board
    # iterate over each required number
    for i in range(0, 9):
        # set 'found' to false
        found = False
        # iterate over each value in the board
        for row in input_board:
            for num in row:
                # if the number in question is found, then set the 'found' flag to true
                if num == i:
                    found = True
        # at the end of the search, if the number in question hasn't been found, then return false
        if not found:
            return False
    # when reaching here, all numbers are present in the code and as a side effect of this check
    # there would be no duplicates on the board, therefore True can be returned
    return True


class InvalidInputError(Exception):
    """
    Define a custom exception 'InvalidInputException' to throw if the board is invalid
    """

    def __init__(self, message="Board Inputted is NOT a valid board"):
        self.message = message
        super().__init__(self.message)


def populate_board(user_in):
    """
    populate_board takes the user's input and creates a 2D array of values for the board
    :param user_in: A tkinter entry type of data in the tables when the submit button was pressed
    :return: A 2D Array of the contents of the input, ready to be turned into a board
    """
    # Create an empty array to store the result
    res = []
    # Iterate through all elements of the input and add these to 'res'
    for row in range(0, len(user_in)):
        # for each row of the inputted board
        # Create a temporary row array and append each element for this row into it
        tmp_row = []
        for col in range(0, len(user_in[row])):
            # For each column in the row, append the value to the tmp_row array
            tmp_row.append(int(user_in[row][col].get()))
        # Append this array of the row into 'res'
        res.append(tmp_row)
    # Ensure the board is valid
    if not check_validity(res):
        # If the board is invalid, raise an error
        raise InvalidInputError
    # Once here, the board in 'res' would be populated and valid, return 'res'
    return res


def run_process(app):
    """
    run_process is the function that actually calls the a_star function implemented by myself
    :param app: the Win instance that called the function
    :return: None
    """
    try:
        # get the selected algorithm option from the dropdown box
        algo = app.str_var.get()
        # use the populate_board function to populate the start and goal board
        start_board = populate_board(start_rows)
        goal_board = populate_board(goal_rows)
        # set the status text to inform the user that the problem is being solved
        app.text_strs[0].set("Status --> Solving ...")
        # update the window to reflect the change
        app.window.update()
        # call the a_star function to run the A* Algorithm on the start and goal state inputted by the user
        res = a_star(start_board, goal_board, algo)
        # Set the status to Complete
        app.text_strs[0].set("Status --> Complete")
        # Expand thw window so the result can be shown
        app.window.geometry("740x545")
        # If the length of 'res' is 0, then the problem is unsolvable
        if len(res) == 0:
            msg = "The puzzle provided is NOT solvable"
        else:
            # otherwise the problem is solvable, construct a message to show specifics of the solution
            msg = "Reached goal after " + str(res.pop(0)) + \
                  " moves, using " + str(res.pop(0)) + " while loops on open_list, moves:"

        # change the live text to the custom message and the result of the A*
        app.text_strs[1].set(msg)
        app.text_strs[2].set(res)
    except (InvalidInputError, ValueError) as e:
        # If there is an InvalidInputError
        # Show a messagebox to alert the user
        messagebox.showerror(title=None,
                             message="InvalidInputError, Please re-enter a valid start and goal board layout")
        # destroy the current window
        app.window.destroy()
        # run a new instance of this python program
        os.system("python main.py")
        # exit this python program instance
        exit()


class Win():
    """
    Class to represent a window and supports its creation, entities and running
    """

    def gui_gen(self, rows, start_row):
        """
        Function to create the grid and store Entry elements into an array for reference later
        :param rows: Array to store rows of entry elements into
        :param start_row: Integer value of the row index to position the top right Entry field
        :return: None
        """
        # Between the start row and 3 rows further
        for i in range(start_row, start_row + 3):
            # Create an empty list to store columns of each row
            cols = []
            # for loops to iterate 3 times (for each column)
            for j in range(3):
                # Create a new Frame
                frame = Frame(master=self.window, relief=RAISED, borderwidth=1)
                # position this frame in the correct position relative to the functions start_row
                frame.grid(row=i, column=j)
                # Create an Entry Field inside this frame and set up options
                e = Entry(master=frame, width=10, font=("Comic Sans MS", 30), justify=CENTER, bg='#e6ffff', relief=FLAT)
                # Append this entry to the cols array
                cols.append(e)
                # pack the entity i.e. send it off to be displayed
                e.pack()
            # Append each completed row to the 'rows' array
            rows.append(cols)

    def __init__(self, start_rows, goal_rows):
        """
        Constructor for the win class, instantiate the window and set up all elemets and aspects of this window
        :param start_rows: array to store the rows of the start board to
        :param goal_rows: array to store the rows of the goal board to
        """

        # Instantiate self.window as a Tk() instance
        self.window = Tk()
        # Set the dimentions of the window
        self.window.geometry("740x485")
        # set the background color of the window
        self.window.configure(bg='#99d6ff')
        # set the title of the window
        self.window.title("Nishil's 8-Puzzle Solver (A* Algorithm with Manhattan or Hamming Heuristic)")

        # Create a Heading Label, set its text, font and background color
        self.heading = Label(self.window,
                             text="Please Enter Values for the Starting Board and choose Heuristic ->",
                             font=("Comic Sans MS", 15),
                             bg='#99d6ff')
        # place this heading window in the correct row and column of the window
        self.heading.grid(row=0, column=0, columnspan=3, sticky='w')

        # Set up the option field for the heuristics
        # Define an array of options
        heuristicOption = ["Manhattan", "Hamming"]
        # Create a StringVar object for this
        self.str_var = StringVar(self.window)
        # set the initial value to Manhattan, as its more effective
        self.str_var.set(heuristicOption[0])
        # Create the option menu using the StringVar object
        self.options = OptionMenu(self.window, self.str_var, *heuristicOption)
        # Configure the font, background and activebackground for the selection box
        self.options.config(font=("Comic Sans MS", 10), bg='#ffff99', activebackground='#ffff99')
        # Place the Option Box in the relevant place in the window
        self.options.grid(row=0, column=2, sticky="e")

        # Create the heading for the goal puzzle, using a Label object
        self.heading1 = Label(self.window,
                              text="Please Enter Values for the Goal Puzzle",
                              font=("Comic Sans MS", 15),
                              bg='#99d6ff')
        # Place this heading in the correct position in the window
        self.heading1.grid(row=5, column=0, columnspan=3)

        # Generate the 2 Input Grids using the gui_gen function
        self.gui_gen(start_rows, 1)
        self.gui_gen(goal_rows, 6)

        # Create the exit button using the Button object
        self.exit_button = Button(self.window,
                                  text="Exit", command=self.window.destroy,
                                  height=2,
                                  width=30,
                                  bg='#ff4d4d',
                                  activebackground='#ff4d4d')
        # Place the exit button in the correct place in the window
        self.exit_button.grid(row=10, column=0)

        # Create the Submit Button and assign the function to pass the input to
        self.submitter = Button(self.window,
                                text="Submit",
                                command=partial(run_process, self),
                                height=2,
                                width=30,
                                bg='#99ff99',
                                activebackground='#99ff99')
        # Place this button in the correct place in the window
        self.submitter.grid(row=10, column=1)

        # Create 2 arrays to hold the StringVar and Strings for dynamic text fields
        self.text_elems = []
        self.text_strs = []
        # For each button (3 Iterations)
        for i in range(0,3):
            # create a StringVar Object
            strs = StringVar()
            # Create a Label object and set the text to be the stringVar object
            elem = Label(self.window, textvariable=strs, font=("Comic Sans MS", 15), bg='#99d6ff')
            # Append these 2 objects to the corresponding lists
            self.text_elems.append(elem)
            self.text_strs.append(strs)

        # Set the text for the status
        self.text_strs[0].set("Status --> Awaiting Input")
        # Position each of the 3 Labels in the correct positions in the window
        self.text_elems[0].grid(row=10, column=2, sticky='e')
        self.text_elems[1].grid(row=11, column=0, columnspan=3, sticky='w')
        self.text_elems[2].grid(row=12, column=0, columnspan=3, sticky='w')

    def run(self):
        """
        call the mainloop function to display the window and allow the user to use the program
        :return: None
        """
        self.window.mainloop()

# Declare 2 Variables
start_rows = []
goal_rows = []
# Create the win object to run the program
app = Win(start_rows, goal_rows)
# Run the app
app.run()
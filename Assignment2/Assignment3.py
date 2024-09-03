import sys

input_file_name = sys.argv[1]

def solve_board_file(file_board): 
    """
    Reads the content of the specified file and converts it into a list (board).

    Parameters:
    - file_board (str): The name of the input file.

    Returns:
    - list: representing the game board.
    """
    board = []
    with open(file_board, "r") as file:
        content = file.read()
        for row in content.strip().split('\n'):
            row_values = list(map(int, row.split()))
            board.append(row_values)
    return board

def print_current_board(board, score):
    """
    Prints the current state of the game board along with the score.

    Parameters:
    - board (list): representing the game board.
    - score (int): Current score.

    Returns:
    - None
    """
    for row in board:
        print(" ".join(map(str, row)))

    print("\nYour score is:", score, "\n")

def is_valid_coordinate(board, row, col):
    """
    Checks if the given row and column coordinates are within the bounds of the board.

    Parameters:
    - board (list): representing the game board.
    - row (int): Row coordinate to check.
    - col (int): Column coordinate to check.

    Returns:
    - bool: True if the coordinates are valid, False otherwise.
    """
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        return True
    else:
        return False

def is_empty_cell(board, row, col): 
    """
    Checks if the specified cell on the board is empty.

    Parameters:
    - board (list): representing the game board.
    - row (int): Row coordinate of the cell.
    - col (int): Column coordinate of the cell.

    Returns:
    - bool: True if the cell is empty, False otherwise.
    """
    if board[row][col] == -1 or board[row][col] == ' ':
        return True
    else:
        return False

def find_set_of_connected_numbers(board, row_to_pop, col_to_pop):
    """
    Finds a set of connected numbers on the board starting from the specified coordinates.

    Parameters:
    - board (list): representing the game board.
    - row_to_pop (int): Row coordinate to start the search.
    - col_to_pop (int): Column coordinate to start the search.

    Returns:
    - tuple: A set of coordinates of connected numbers and the selected number.
    """
    numbers_coordinates = set()
    selected_number = board[row_to_pop][col_to_pop]
    row_count = len(board)
    col_count = len(board[0])

    if selected_number == -1 or selected_number == ' ':
        return set(), -1

    def dfs(row, col):
        if not (0 <= row < row_count) or not (0 <= col < col_count):
            return
        
        if board[row][col] != selected_number:
            return

        if (row,col) in numbers_coordinates:
            return
        numbers_coordinates.add((row,col))
        dfs(row-1,col)
        dfs(row+1, col)
        dfs(row, col+1)
        dfs(row, col-1)

    dfs(row_to_pop, col_to_pop)
    return numbers_coordinates, selected_number

def remove_cells(board, numbers_coordinates):
    """
    Removes cells from the board based on the provided coordinates.

    Parameters:
    - board (list): representing the game board.
    - numbers_coordinates (set): Set of coordinates to be removed.

    Returns:
    - list: Updated game board after removing the specified cells.
    """
    for coord in numbers_coordinates:
        row, col = coord
        board[row][col] = -1  

    return board

def gravite_numbers(board):
    """
    Applies gravity to the numbers on the board, moving them down.

    Parameters:
    - board (list): representing the game board.

    Returns:
    - None
    """
    for col in range(len(board[0])):
        empty_row = -1
        for row in range(len(board) - 1, -1, -1):
            if board[row][col] == -1:
                if empty_row == -1:
                    empty_row = row
            elif empty_row != -1:
                board[empty_row][col], board[row][col] = board[row][col], -1
                empty_row -= 1

def shift_left_col(board, col):
    """
    Shifts the numbers in the specified column to the left.

    Parameters:
    - board (list): representing the game board.
    - col (int): Column index to shift.

    Returns:
    - None
    """
    if all(board[row][col] == ' ' for row in range(len(board))):
        for row in range(len(board)):
            for c in range(col, len(board[0]) - 1):
                board[row][c] = board[row][c + 1]
            board[row][-1] = ' '

def shift_row_to_bottom(board, row):
    """
    Shifts the specified row to the bottom of the board.

    Parameters:
    - board (list): representing the game board.
    - row (int): Row index to shift.

    Returns:
    - None
    """
    if all(element == -1 for element in board[row]):
        board.append(board.pop(row))

def replace_minus_one_with_space(board):
    """
    Replaces all occurrences of -1 with a space in the game board.

    Parameters:
    - board (list): representing the game board.

    Returns:
    - None
    """
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == -1:
                board[row][col] = ' '

def board_list_to_str(board):
    """
    Converts the list representing the game board to a string.

    Parameters:
    - board (list): representing the game board.

    Returns:
    - str: String representation of the game board.
    """
    string_board = ""

    for row in board:
        temp_list = []
        for number in row:
            temp_list.append(str(number))
        string_row = " ".join(temp_list)
        string_board += string_row + "\n"

    return string_board

def get_input_rowcol():  
    """
    Gets user input for a row and a column number.

    Returns:
    - tuple: Row and column indices entered by the user.
    """
    input_str = input("Please enter a row and a column number: ")
    input_list = input_str.split()

    if len(input_list) == 2:
        row = int(input_list[0])
        col = int(input_list[1])
        return row-1, col-1
    else:
        print("Please enter a correct size!")
        return None, None


def is_game_over(board):
    row_count = len(board)
    col_count = len(board[0])

    for row in range(row_count):
        for col in range(col_count):
            to_be_popped_set, value = find_set_of_connected_numbers(board, row, col)
            if len(to_be_popped_set) > 1:
                return False
            
    return True


def play_game(board, puan):
    while True:
        
        if is_game_over(board):
            print("Game over.\n")
            return

        row, col = get_input_rowcol()

        if not is_valid_coordinate(board, row, col):
            print("\nPlease enter a correct size!\n")
            return play_game(board, puan)

        elif is_empty_cell(board, row, col):
            print("\nEmpty cell, try again!\n")
            return play_game(board, puan)

        else:
            numbers_will_pop, selected = find_set_of_connected_numbers(board, row, col)

            if len(numbers_will_pop) == 1:
                print("\nNo movement happened try again\n")
                print_current_board(board, puan)
                return play_game(board, puan)

            removed_count = len(remove_cells(board, numbers_will_pop))
            
            puan += selected * len(numbers_will_pop)
            print()

            gravite_numbers(board)
            shift_row_to_bottom(board, row)
            replace_minus_one_with_space(board)
            shift_left_col(board, col)
            print_current_board(board, puan)

board = solve_board_file(input_file_name)
print_current_board(board, 0)
play_game(board, 0)              

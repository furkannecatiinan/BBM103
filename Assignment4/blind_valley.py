import sys

# Getting the name of the input file from command line arguments.
input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

def readFile(input_file_name):
    """Reads the file and converts its content into a 2D list.

    Parameters:
    input_file_name : str - The name of the file to read.

    Returns:
    grid : list - A 2D list of strings representing the grid.
    """
    with open(input_file_name, "r", encoding="utf-8") as file:
        content = file.read()
        grid = []
        for row in content.strip().split("\n"):
            row_values = list(map(str, row.split()))
            grid.append(row_values)
    return grid

def getSepGrids(grid):
    """Separates the input grid into different components.

    Parameters:
    grid : list - A 2D list representing the input grid.

    Returns:
    letter_grid : list - A 2D list representing the letters 'L' or 'U'.
    new_grid : list - A 2D list initialized for the solution.
    restrictions : list - A list of restriction values for rows and columns.
    """
    restrictions = []
    letter_grid = []
    new_grid = []
    for i in range(len(grid)):
        if i < 4:
            restrictions.append([int(j) for j in grid[i]])
        else:
            letter_grid.append([j for j in grid[i]])
            new_grid.append(["A" for _ in grid[i]])
    return letter_grid, new_grid, restrictions

def checkRowRestrictions(new_grid, row, restrictions):
    """Checks if the row restrictions are met for the current state of the grid.

    Parameters:
    new_grid : list - The current state of the solution grid.
    row : int - The row number to check restrictions for.
    restrictions : list - A list of restriction values for rows and columns.

    Returns:
    bool - True if restrictions are met, else False.
    """
    # Checking 'H' and 'B' counts and consecutive elements in the row
    count_h = new_grid[row].count('H')
    count_b = new_grid[row].count('B')
    if restrictions[0][row] != -1 and count_h != restrictions[0][row]:  # Check 'H' count for row
        return False
    if restrictions[1][row] != -1 and count_b != restrictions[1][row]:  # Check 'B' count for row
        return False
    for i in range(len(new_grid[row]) - 1):
        if new_grid[row][i] == new_grid[row][i+1] and new_grid[row][i] in ['H', 'B']:
            return False
    return True

def checkRestrictions(new_grid, restrictions):
    """Checks if all the restrictions are met for the current state of the grid.

    Parameters:
    new_grid : list - The current state of the solution grid.
    restrictions : list - A list of restriction values for rows and columns.

    Returns:
    bool - True if all restrictions are met, else False.
    """
    # Calculating 'H' and 'B' counts for each row and column
    row_count_h = [0] * len(new_grid)
    col_count_h = [0] * len(new_grid[0])
    row_count_b = [0] * len(new_grid)
    col_count_b = [0] * len(new_grid[0])

    for i in range(len(new_grid)):
        for j in range(len(new_grid[0])):
            if new_grid[i][j] == 'H':
                row_count_h[i] += 1
                col_count_h[j] += 1
            elif new_grid[i][j] == 'B':
                row_count_b[i] += 1
                col_count_b[j] += 1

    # Checking restrictions for rows and columns
    for i in range(len(restrictions[0])):  # Check 'H' restrictions for rows
        if restrictions[0][i] != -1 and row_count_h[i] != restrictions[0][i]:
            return False
    for i in range(len(restrictions[1])):  # Check 'B' restrictions for rows
        if restrictions[1][i] != -1 and row_count_b[i] != restrictions[1][i]:
            return False
    for i in range(len(restrictions[2])):  # Check 'H' restrictions for columns
        if restrictions[2][i] != -1 and col_count_h[i] != restrictions[2][i]:
            return False
    for i in range(len(restrictions[3])):  # Check 'B' restrictions for columns
        if restrictions[3][i] != -1 and col_count_b[i] != restrictions[3][i]:
            return False
    return True  # Return True if all restrictions are met

def is_valid_placement(new_grid, row, col, restrictions):
    """Checks if the current placement is valid according to game rules and restrictions.

    Parameters:
    new_grid : list - The current state of the solution grid.
    row : int - The current row of placement.
    col : int - The current column of placement.
    restrictions : list - A list of restriction values for rows and columns.

    Returns:
    bool - True if the placement is valid, else False.
    """
    # Checking for consecutive 'H' or 'B' horizontally and vertically
    if col > 0 and new_grid[row][col] == new_grid[row][col-1]:  # Check left cell
        return False
    if row > 0 and new_grid[row][col] == new_grid[row-1][col]:  # Check above cell
        return False

    # Checking 'H' and 'B' counts against restrictions for the row and column
    count_h_row = new_grid[row].count('H')
    count_b_row = new_grid[row].count('B')
    count_h_col = sum(1 for r in range(len(new_grid)) if new_grid[r][col] == 'H')
    count_b_col = sum(1 for r in range(len(new_grid)) if new_grid[r][col] == 'B')

    if restrictions[0][row] != -1 and count_h_row > restrictions[0][row]:  # Check 'H' for row
        return False
    if restrictions[1][row] != -1 and count_b_row > restrictions[1][row]:  # Check 'B' for row
        return False
    if restrictions[2][col] != -1 and count_h_col > restrictions[2][col]:  # Check 'H' for column
        return False
    if restrictions[3][col] != -1 and count_b_col > restrictions[3][col]:  # Check 'B' for column
        return False
    return True

def solve_puzzle(row, col, letter_grid, new_grid, restrictions):
    """Solves the puzzle using backtracking algorithm.

    Parameters:
    row : int - The current row in the grid.
    col : int - The current column in the grid.
    letter_grid : list - A 2D list representing the letters 'L' or 'U'.
    new_grid : list - The current state of the solution grid.
    restrictions : list - A list of restriction values for rows and columns.

    Returns:
    list - A 2D list representing the solved grid or None if no solution exists.
    """
    if row == len(letter_grid):  # If end of grid is reached
        if checkRestrictions(new_grid, restrictions):
            return new_grid
        else:
            return None  # No solution found

    if col == len(letter_grid[0]):  # If end of row is reached
        return solve_puzzle(row + 1, 0, letter_grid, new_grid, restrictions)

    if new_grid[row][col] == 'A' and letter_grid[row][col] in ['L', 'U']:
        for attempt in [('H', 'B'), ('B', 'H'), ('N', 'N')]:  # Try 'HB', 'BH', then 'NN'
            new_grid[row][col] = attempt[0]
            delta_row, delta_col = (1, 0) if letter_grid[row][col] == 'U' else (0, 1)
            adjacent_row, adjacent_col = row + delta_row, col + delta_col
            
            if 0 <= adjacent_row < len(letter_grid) and 0 <= adjacent_col < len(letter_grid[0]):
                new_grid[adjacent_row][adjacent_col] = attempt[1]
                
                if is_valid_placement(new_grid, row, col, restrictions):
                    result = solve_puzzle(row, col + 1, letter_grid, new_grid, restrictions)
                    if result:
                        return result  # Successful placement
                
                # Backtrack if not successful or if restrictions aren't met
                new_grid[row][col], new_grid[adjacent_row][adjacent_col] = 'A', 'A'
    return solve_puzzle(row, col + 1, letter_grid, new_grid, restrictions)  # Continue to next cell

def main():
    """Main function to read file, prepare the grid, and solve the puzzle."""
    grid = readFile(input_file_name)
    letter_grid, new_grid, restrictions = getSepGrids(grid)
    solved_grid = solve_puzzle(0, 0, letter_grid, new_grid, restrictions)
    with open(output_file_name, "w") as file:

        if solved_grid:
            for i, row in enumerate(solved_grid):
                if i < len(solved_grid) - 1:  # Check if it's not the last row
                    file.write(" ".join(row) + "\n")
                else:
                    file.write(" ".join(row))  # Don't add a newline character for the last row
        else:
            file.write("No solution found!")

if __name__ == "__main__":
    main()

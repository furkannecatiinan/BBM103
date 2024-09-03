import sys

def solve_sudoku_text(file_sudoku): 
    """
    Converts a Sudoku string to matrix (list[list[int]]).   
    Parameters: file_sudoku (str): String Sudoku text file.
    Returns: list[list[int]] Sudoku matrix.
    """
    with open(file_sudoku, "r") as file:
        sudoku = []

        for satir in file.read().strip().split('\n'):
            sudoku.append(list(map(int, satir.split())))

        return sudoku

def get_row(sudoku, n): 
    """
    Retrieves the value of Sudoku's rows' nth element.
    Parameters: list[list[int]] Sudoku matrix.
    Returns: set{} Set of rows' elements.
    """
    return set(sudoku[n])



def get_col(sudoku, n):
    """
    Retrieves the value of Sudoku's rows' nth element.
    Parameters: list[list[int]] Sudoku matrix, n.
    Returns: set{} Set of columns' elements.
    """
    return set(row[n] for row in sudoku)

def get_submatrix(sudoku, row_of_submatrix, col_of_submatrix):
    """
    Retreives the values of Sudoku's submatrixs' elements.
    Parameters: list[list[int]] Sudoku matrix, int row of submatrix, int col of submatrix.
    Returns: set() Set of submatrix's elements.
    """
    beginning_row_sub = (row_of_submatrix // 3) * 3
    beginning_col_sub = (col_of_submatrix // 3) * 3

    submatrix = set()

    for i in range(beginning_row_sub, beginning_row_sub + 3):
        for j in range(beginning_col_sub, beginning_col_sub + 3):
            submatrix.add(sudoku[i][j])

    return submatrix

def find_possible_numbers(sudoku, row, col):
    """
    Find the possible numbers for empty square. 
    Parameters: list[list[int]] Sudoku matrix, int row, int col.
    Returns: set{} Set of possible numbers.
    """
    row_numbers = get_row(sudoku, row)
    col_numbers = get_col(sudoku, col)
    submatrix_numbers = get_submatrix(sudoku, row, col)
    
    merged = set(row_numbers) | set(col_numbers) | set(submatrix_numbers)
    possibles = set(range(1, 10)) - merged
    if 0 in possibles:
        possibles.remove(0)
    return possibles

def solve_one_square(sudoku):
    """
    Solve a one empty square if there is one possible number.
    Parameters: list[list[int]] Sudoku matrix.
    Returns: tuple() Tuple of row, col and answer.
    """
    for r in range(9):
        for c in range(9):
            if sudoku[r][c] == 0:
                possibles = find_possible_numbers(sudoku, r, c)
                if len(possibles) == 1:
                    answer = possibles.pop()

                    return r, c, answer

def count_zeros(sudoku):
    """
    Count the number of empty squares. 
    Parameters: list[list[int]] Sudoku matrix.
    Returns: int count of zeros.
    """
    count = 0

    for row in sudoku:
        for number in row:
            if number == 0:
                count += 1

    return count

def sudokuToString(sudoku):
    """
    Convert Sudoku matrix to string Sudoku.
    Parameters: list[list[int]] Sudoku matrix.
    Returns: str String Sudoku.
    """
    string_sudoku = ""

    for row in sudoku:
        temp_list = []
        for number in row:
            #Merging a row of integers to a string:
            temp_list.append(str(number))
        string_row = " ".join(temp_list)
        string_sudoku += string_row + "\n"

    return string_sudoku

def solve_sudoku(output_file, sudoku, number_of_zeros): 
    """
    Solves Sudoku and writes the steps and the solves to an output file. 
    Parameters: output_file (str), list[list[int]] Sudoku matrix, int number_of_zeros.
    Returns: None
    """
    step = 1
    with open(output_file, "w") as file:
        for i in range(number_of_zeros):
            row, col, answer = solve_one_square(sudoku)
            sudoku[row][col] = answer

            file.write("-" * 18 + "\n" + f"Step {step} - {answer} @ R{row+1}C{col+1}" + "\n" + "-" * 18 + "\n")
            file.write(sudokuToString(sudoku))
            step += 1
        file.write("-" * 18)

def main():
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    sudoku = solve_sudoku_text(input_file)
    number_of_zeros = count_zeros(sudoku)
    solve_sudoku(output_file, sudoku, number_of_zeros) 

if __name__ == "__main__":
    main()

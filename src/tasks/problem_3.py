class Sudoku:
    def solve(self, grid: list[list[int]]) -> list | None:
        # Validate the initial grid before solving
        if not self._is_valid_grid(grid):
            return None

        # Just a personal preference, I personally always try to avoid mutating the original copy.
        # Unfortunately Python does not support pass by value for mutable objectss so I have to make a deep copy instead.
        grid_copy = []
        for row in grid:
            grid_copy.append(row[:])

        if self._solve(grid_copy):
            return grid_copy
        else:
            return None

    def get_user_grid(self) -> list[list[int]]:
        print("\n=== Sudoku Grid Input ===")
        print("Enter each row as 9 digits (0-9), where 0 represents an empty cell.")
        print("Example: '530070000' for the first row of the default puzzle.")
        print("Press Enter without input to use the default puzzle.\n")

        grid = []

        for i in range(9):
            while True:
                row_input = input(f"Enter row {i+1}: ")

                # Use default grid if user skips input
                if not row_input and i == 0:
                    return None

                # Validate input
                if not row_input:
                    print("Please enter a row or start over.")
                    continue

                if len(row_input) != 9 or not row_input.isdigit():
                    print("Invalid input. Please enter exactly 9 digits (0-9).")
                    continue

                # Convert string to list of integers
                grid.append([int(digit) for digit in row_input])
                break

        return grid

    def print_grid(self, grid: list[list[int]]) -> None:
        for i, row in enumerate(grid):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j, val in enumerate(row):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                print(val if val != 0 else ".", end=" ")
            print()

    def _is_valid_grid(self, grid: list[list[int]]):
        # Check for duplicates in rows
        for row in grid:
            nums = [n for n in row if n != 0]
            if len(nums) != len(set(nums)):
                return False

        # Check for duplicates in columns
        for col in range(9):
            nums = [grid[row][col] for row in range(9) if grid[row][col] != 0]
            if len(nums) != len(set(nums)):
                return False

        # Check for duplicates in 3x3 boxes
        for row in range(3):
            for col in range(3):
                nums = [
                    grid[i][j]
                    for i in range(row // 3 * 3, row // 3 * 3 + 3)
                    for j in range(col // 3 * 3, col // 3 * 3 + 3)
                    if grid[i][j] != 0
                ]
                if len(nums) != len(set(nums)):
                    return False

        return True

    def _solve(self, grid: list[list[int]], row: int = 0, col: int = 0) -> bool:
        # Index starts at 0 so if row is 9 (out of bound) then that means it has gone through every row
        if row == 9:
            return True

        # Index starts at 0 so if the column is 9 (out of bound for that row) then that means this row is done and can move to next row
        if col == 9:
            return self._solve(grid, row + 1, 0)

        # If the current cell is not zero, it means that the cell is solved so we can move to the next column
        if grid[row][col] != 0:
            return self._solve(grid, row, col + 1)

        # We need to try every value from 1 till 9 (inclusive) for the current cell
        for value in range(1, 10):
            if self._is_valid(grid, row, col, value):
                # Set the current cell to a value to test it
                grid[row][col] = value

                # Test the value of the cell by recursively calling the solve method which will eventually backtrack after setting the cell to 0 again
                # If trying to solve again reaches the base case then exit the loop and terminate the algorithm
                if self._solve(grid, row, col + 1):
                    return True

                # If the cell was found to be the wrong solution, it will be backtracked to and set back to 0
                grid[row][col] = 0

        return False

    def _is_valid(self, grid: list[list[int]], row: int, col: int, value: int) -> bool:
        not_in_row = value not in grid[row]
        not_in_col = value not in [grid[i][col] for i in range(9)]
        not_in_sub_grid = value not in [
            grid[i][j]
            for i in range(row // 3 * 3, row // 3 * 3 + 3)
            for j in range(col // 3 * 3, col // 3 * 3 + 3)
        ]

        return not_in_row and not_in_col and not_in_sub_grid


def problem_3():
    print("Problem 3: Sudoku Solver")

    solver = Sudoku()

    """
    0 - empty cell
    1-9 - filled cell

    AI dislcaimer: The sudoku grid below is generated using Generative AI.
    Prompt given:
    "
      0 - empty cell
      1-9 - filled cell

      sudoku_grid = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
      ]

      generate me a sudoku grid
    "
    
    This default grid is for testing purposes (so it's quicker to debug than manually typing in the grid every time)
    """
    sudoku_grid = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    # Ask user if they want to use the default grid or input their own
    choice = input("Use default Sudoku grid? (y/n): ").lower()

    if choice == "y" or choice == "yes":
        grid = sudoku_grid
    else:
        user_grid = solver.get_user_grid()
        grid = user_grid if user_grid else sudoku_grid

    solved = solver.solve(grid)

    print("\nOriginal:")
    solver.print_grid(grid)

    if solved is None:
        print("No solution found.")
        return

    print("\nSolution:")
    solver.print_grid(solved)

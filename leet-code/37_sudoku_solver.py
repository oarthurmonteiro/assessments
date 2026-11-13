class Solution:
    def solveSudoku(self, board: list[list[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        row_has = [[False] * 9 for _ in range(9)]
        col_has = [[False] * 9 for _ in range(9)]
        grid_has = [[False] * 9 for _ in range(9)]

        module = int(len(board) ** (.5))
        for row in range(9):
            for col in range(9):
                if board[row][col] == ".":
                    continue

                idx = int(board[row][col]) - 1
                grid = calculate_grid(module, row, col)

                row_has[row][idx] = True
                col_has[col][idx] = True
                grid_has[grid][idx] = True

        def solve():
            min_options = 10
            best_cell = None
            best_valid_numbers = []
            for row in range(9):
                for col in range(9):
                    if board[row][col] == ".":
                        grid = calculate_grid(module, row, col)
                        valid_numbers = []

                        for number in range(9):
                            if not (row_has[row][number] or col_has[col][number] or grid_has[grid][number]):
                                valid_numbers.append(number)

                        if len(valid_numbers) == 0:
                            return False

                        if len(valid_numbers) < min_options:
                            min_options = len(valid_numbers)
                            best_cell = (row, col)
                            best_valid_numbers = valid_numbers

                            # Optimization: if a cell has only 1 choice, pick it immediately
                            if min_options == 1:
                                break
                if min_options == 1:
                    break

            if best_cell is None:
                return True

            row, col = best_cell
            grid = calculate_grid(module, row, col)

            # 3. Try each valid number for this most-constrained cell
            for number in best_valid_numbers:
                row_has[row][number] = True
                col_has[col][number] = True
                grid_has[grid][number] = True
                board[row][col] = str(number + 1)

                if solve():
                    return True

                # Backtrack
                row_has[row][number] = False
                col_has[col][number] = False
                grid_has[grid][number] = False
                board[row][col] = "."

            return False

        solve()

def calculate_grid(module, row, col):
    return (row // module) * module + (col // module)

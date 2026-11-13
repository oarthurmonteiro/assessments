class Solution:
    def solveNQueens(self, n: int) -> list[list[str]]:
        board = [["."] * n for _ in range(n)]
        row_has = [False] * n
        pos_diag_has = [False] * ((2 * n) - 1)
        neg_diag_has = [False] * ((2 * n) - 1)

        result = []
        def solve(c):
            if c >= n:
                result.append(["".join(row) for row in board])
                return

            for r in range(n):
                if (row_has[r] or pos_diag_has[r+c] or neg_diag_has[r-c+(n - 1)]):
                    continue

                row_has[r] = True
                pos_diag_has[r+c] = True
                neg_diag_has[r-c+(n-1)] = True
                board[r][c] = "Q"

                solve(c + 1)

                row_has[r] = False
                pos_diag_has[r+c] = False
                neg_diag_has[r-c+(n-1)] = False
                board[r][c] = "."

            return False

        solve(0)

        return result

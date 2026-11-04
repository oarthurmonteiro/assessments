class Excel:
    def __init__(self, height: int, width: str):
        self.cells = [[0] * self._convert_letter_to_number(width) for _ in range(height)]

    @staticmethod
    def _convert_letter_to_number(letter: str) -> int:
        return ord(letter.lower()) - ord("a") + 1

    def set(self, row: int, column: str, val: int) -> None:
        self.cells[row-1][self._convert_letter_to_number(column) - 1] = val

    def get(self, row: int, column: str) -> int:
        return self.cells[row-1][self._convert_letter_to_number(column) - 1]

    @staticmethod
    def _convert_coordinate_to_position(cell: str) -> tuple[int,str]:
        col_letter = cell[0]
        row_num = int(cell[1:])

        return (row_num, col_letter)

    @staticmethod
    def _convert_range_to_cells_arr(range_cells: str) -> list[tuple[int, str]]:
        start, end = range_cells.split(":")
        start_row, start_col = Excel._convert_coordinate_to_position(start)
        end_row, end_col = Excel._convert_coordinate_to_position(end)

        positions = []
        for col_code in range(ord(start_col), ord(end_col) + 1):
            col_letter = chr(col_code)
            for row in range(start_row, end_row + 1):
                positions.append((row, col_letter))

        return positions

    def sum(self, row: int, column: str, numbers: list[str]) -> int:
        cells = []
        for cell in numbers:
            if ":" in cell:
                cells.extend(self._convert_range_to_cells_arr(cell))
                continue

            cells.append(self._convert_coordinate_to_position(cell))

        value = 0
        for r, c in cells:
            value += self.get(r, c)

        self.set(row, column, value)
        return value


e = Excel(3, "C")
e.set(1, "A", 2)
print(e.get(1, "A"))
print(e.cells)
print(e._convert_range_to_cells_arr("A1:B2"))
print(e.sum(3, "C", ["A1", "A1:B2"]))
print(e.cells)



# A1:B2 -> A1,A2,B1,B2
# A1:C2 -> A1,A2,B1,B2,C1,C2

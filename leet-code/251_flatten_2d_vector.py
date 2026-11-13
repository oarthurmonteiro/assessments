class FlatVector2D:
    def __init__(self, arr: list[list[int]]):
        self.arr = self._flatten_2d_arr(arr)
        self.size = len(arr)
        self.curr_pos = 0

    def next(self) -> int|None:
        if not self.hasNext():
            return None

        val = self.arr[self.curr_pos]
        self.curr_pos += 1
        return val

    def hasNext(self) -> bool:
        return self.curr_pos <= self.size

    @staticmethod
    def _flatten_2d_arr(arr: list[list[int]]) -> list[int]:
        r = []
        for a in arr:
            r.extend(a)

        return r


class Vector2D:
    def __init__(self, arr: list[list[int]]):
        self.arr = arr
        self.i = 0
        self.j = 0
        self.size = len(self.arr)
        self.curr_size = len(self.arr[self.i])

    def hasNext(self) -> bool:
        return self.i < self.size and self.j <= self.curr_size

    def next(self) -> int|None:
        if not self.hasNext():
            return None

        val = self.arr[self.i][self.j]
        if self.j < self.curr_size -1 :
            self.j += 1
        elif self.i < self.size:
            self.i += 1
            self.j = 0
            self.curr_size = len(self.arr[self.i]) if self.i < self.size else 0

        return val

i = Vector2D([[1,2],[3],[4]])
while i.hasNext():
    print(i.next())

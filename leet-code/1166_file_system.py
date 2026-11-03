class FileSystem:
    def __init__(self):
        self.dirs = {"/": {}}

    @staticmethod
    def _convert_path_str_in_arr(dir_path: str) -> list[str]:
        # /a/b/c
        # / -> a -> b -> c
        # [a, b, c]

        return list(filter(lambda x: x, dir_path.split("/")[1:]))

    def _navigate_through(self, paths: list[str]) -> dict | None:
        curr = self.dirs["/"]
        for path in paths:
            if path not in curr:
                return None

            curr = curr[path]

        return curr


    def createPath(self, path: str, value: object) -> bool:
        paths = self._convert_path_str_in_arr(path)
        if not paths:
            return False

        dir = self._navigate_through(paths[:-1])
        if dir is None:
            return False

        file_name = paths[-1]
        if file_name in dir:
            return False

        dir[file_name] = value
        return True

    def get(self, path) -> object:
        paths = self._convert_path_str_in_arr(path)
        if not paths:
            return -1

        dir = self._navigate_through(paths[:-1])
        if dir is None:
            return -1

        file_name = paths[-1]
        if file_name not in dir:
            return -1

        return dir[paths[-1]]


fs = FileSystem()
print(fs.createPath("/a", 1))
print(fs.get("/a"))

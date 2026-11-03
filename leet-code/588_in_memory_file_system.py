# https://leetcode.ca/all/588.html

class FileSystem:
    def __init__(self):
        self.dirs: dict[str, dict] = {"/": {}}

    @staticmethod
    def _convert_path_str_in_arr(dir_path: str) -> list[str]:
        # /a/b/c
        # / -> a -> b -> c
        # [a, b, c]

        return list(filter(lambda x: x, dir_path.split("/")[1:]))

    def _add_dir(self, dirs: list[str]):
        if len(dirs) == 1:
           return {dirs[0]: {}}

        return {dirs[0]: self._add_dir(dirs[1:])}

    def mkdir(self, dir_path: str) -> None:
        paths = self._convert_path_str_in_arr(dir_path)
        if not paths:
            return

        self._navigate_or_create(paths)

    def _navigate_or_create(self, paths: list[str]) -> dict:
        curr = self.dirs["/"]
        for path in paths:
            if path not in curr:
                curr[path] = {}
            curr = curr[path]

        return curr

    def _navigate_through(self, paths: list[str]) -> dict:
        dir = self.dirs["/"]
        for path in paths:
            dir = dir[path]

        return dir

    def ls(self, dir_path: str) -> list[str]:
        paths = self._convert_path_str_in_arr(dir_path)
        if not paths:
            return sorted(self.dirs["/"].keys())

        dir_or_file = self._navigate_through(paths)
        if isinstance(dir_or_file, dict):
            return sorted(dir_or_file.keys())

        return [paths[-1]]

    def addContentToFile(self, file_name: str, content: str) -> None:
        paths = self._convert_path_str_in_arr(file_name)
        if not paths:
            raise RuntimeError("Did not passed a filename")

        dir = self._navigate_through(paths[:-1])
        file_name = paths[-1]
        if file_name in dir:
            dir[file_name] += content
            return

        dir[file_name] = content

    def readContentFromFile(self, file_name: str) -> str:
        paths = self._convert_path_str_in_arr(file_name)
        if not paths:
            raise RuntimeError("Did not passed a filename")

        dir = self._navigate_through(paths[:-1])
        file_name = paths[-1]
        if file_name not in dir:
            raise RuntimeError("File does not exist yet")

        return dir[file_name]


fs = FileSystem()
fs.mkdir("/a/b/c")
fs.mkdir("/a/b")
print(fs.ls("/a/b"))
fs.addContentToFile("/a/b/c/d", "hello")
print(fs.ls("/a/b/c"))
print(fs.ls("/a/b/c/d"))
print(fs.readContentFromFile("/a/b/c/d"))

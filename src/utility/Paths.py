
import os
from pathlib import Path
from unittest import TestCase


class Paths(object):

    def __init__(self) -> None:
        super().__init__()

    def GetDataset(self, name: str):
        filename: str = f"{name}.xml"
        filePath: str = str(Path(self.GetDataRoot()).joinpath(filename))
        return filePath

    def GetDataRoot(self) -> str:
        return str(Path(self.GetProjectRoot()).joinpath("data"))

    def GetSourceRoot(self) -> str:
        return str(Path(self.GetProjectRoot()).joinpath("src"))

    def GetProjectRoot(self) -> str:
        path = os.getcwd()
        return self._FindProjectRoot(path)

    def _IsFolderExists(self, path: str, subPath: str) -> bool:
        return Path(path).joinpath(subPath).exists()

    def _FindProjectRoot(self, path: str) -> str:
        srcRoot: str = ""

        if ("src" in path.split(os.path.sep)):  # Using os.path.sep for platform independence
            cursor = path
            isSrc: bool = False
            while (not isSrc):
                cursor = Path(cursor).parent
                part = cursor.parts[-1]
                if (part == "src"):
                    isSrc = True
                    srcRoot = str(cursor)
        elif ("src" in path):
            srcRoot = path
        else:
            if (self._IsFolderExists(path, "src")):
                return path
            else:
                raise Exception(f"Please call the library from the parent directory. You are calling from: '{path}'.")

        projectRoot = str(Path(srcRoot).parent)
        return projectRoot


class PathsTest(TestCase):

    def test_FindProjectRoot_NestedSrcPath_ReturnParent(self):
        self.assertEqual(os.path.join("C:", "Projects", "gen-atomic"),
                         Paths()._FindProjectRoot(
                             os.path.join("C:", "Projects", "gen-atomic", "src", "UI", "folder", "StreamlitUI.py")))

    def test_FindProjectRoot_SrcFilePath_ReturnParent(self):
        self.assertEqual(os.path.join("C:", "Projects", "gen-atomic"),
                         Paths()._FindProjectRoot(
                             os.path.join("C:", "Projects", "gen-atomic", "src", "StreamlitUI.py")))

    def test_FindProjectRoot_SrcFolderPath_ReturnParent(self):
        self.assertEqual(os.path.join("C:", "Projects", "gen-atomic"),
                         Paths()._FindProjectRoot(os.path.join("C:", "Projects", "gen-atomic", "src")))

    def test_FindProjectRoot_ProjectFolderPath_ReturnParent(self):
        paths = Paths()
        from unittest.mock import patch
        with patch.object(paths, '_IsFolderExists', return_value=True):
            self.assertEqual(os.path.join("C:", "Projects", "gen-atomic"),
                             paths._FindProjectRoot(os.path.join("C:", "Projects", "gen-atomic")))

    def test_FindProjectRoot_NoProjectPath_RaiseError(self):
        paths = Paths()
        from unittest.mock import patch
        with patch.object(paths, '_IsFolderExists', return_value=False):
            with self.assertRaises(Exception):
                paths._FindProjectRoot(os.path.join("C:", "Projects", "somerandomfolder"))


if __name__ == "__main__":
    print("root: ", Paths().GetProjectRoot())

import os
from pathlib import Path


class PathHelper(object):

    def __init__(self) -> None:
        super().__init__()

    def GetDataset(self, name:str):
        filename = f"{name}.xml"
        filePath = Path(self.GetDataRoot()).joinpath(filename)
        return filePath

    def GetDataRoot(self):
        return Path(self.GetProjectRoot()).joinpath("data")

    def GetSourceRoot(self):
        return Path(self.GetProjectRoot()).joinpath("src")

    def GetProjectRoot(self)->str:
        path = os.getcwd()
        srcRoot:str = ""

        if(path.__contains__("\\src\\")):       #We assume that no subfolders with the name 'src' will be added to the project.
            cursor = path
            isSrc:bool = False
            while(isSrc == False):
                cursor = Path(cursor).parent
                part = cursor.parts[-1]
                if(part == "src"):
                    isSrc = True
                    srcRoot = cursor
        elif(path.__contains__("\\src")):
            srcRoot = path
        else:
            if (Path(path).joinpath("src").exists()):
                return path
            else:
                raise Exception(f"Please call the library from the parent directory. You are calling from: '{path}'.")

        projectRoot = str(Path(srcRoot).parent)
        return projectRoot

    def SetCustomRoot(self, customRoot:str):
        pass

if __name__ == "__main__":
    print("root: ",PathHelper().GetProjectRoot())

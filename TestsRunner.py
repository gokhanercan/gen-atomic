import os
import unittest
from unittest import TextTestRunner

if __name__ == "__main__":

    loader = unittest.TestLoader()
    from pathlib import Path
    currentDirectory = os.getcwd()
    start_dir = Path(currentDirectory)
    srcFolder:str = str(start_dir)
    if not srcFolder.__contains__("\\src"):
        srcFolder = srcFolder + "\\src"
    print(f"Source Folder: '{srcFolder}'")
    suite = loader.discover(start_dir=srcFolder, pattern="*.py", top_level_dir=srcFolder)
    runner = TextTestRunner(verbosity=5, failfast=False)
    result = runner.run(suite)
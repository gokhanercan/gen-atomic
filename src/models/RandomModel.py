import string
import random

from langunits.LangUnitFactory import LangUnitInfo
from models.ModelBase import *


class RandomModel(ModelBase, BaselineModel):
    def __init__(self, length: int = 50) -> None:
        super().__init__()
        self.Length = length

    def Generate(self, description: str, langUnitInfo:LangUnitInfo) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation + ' '
        text = ''.join(random.choice(chars) for _ in range(self.Length))
        return text


if __name__ == "__main__":
    random_text = RandomModel().Generate("here is the sample text",LangUnitInfo("SqlSelect","sql select query"))
    print(random_text)
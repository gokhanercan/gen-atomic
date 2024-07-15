import string
import random

from models.ModelBase import ModelBase
from data.Dataset import *

class RandomModel(ModelBase):
    def __init__(self, length: int = 50) -> None:
        super().__init__()
        self.Length = length

    def Generate(self, description: str, UnitType:UnitType) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation + ' '
        text = ''.join(random.choice(chars) for _ in range(self.Length))
        return text


if __name__ == "__main__":
    random_text = RandomModel().Generate("here is the sample text")
    print(random_text)
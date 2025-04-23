from typing import Optional
from unittest import TestCase


class Prompt:

    def __init__(self, text:str, pid:Optional[str] = None) -> None:
        super().__init__()
        self.text:str = text
        self.pid:Optional[str] = pid

    @staticmethod
    def calc_prompt_hash(prompt: str) -> str:
        import hashlib
        sha1 = hashlib.sha1(prompt.encode('utf-8')).hexdigest()
        return sha1[:7]

    def key(self):
        if (self.pid is None):
            return f"t:{self.calc_prompt_hash(self.text)}"
        else:
            return f"id:{self.pid}"


class PromptTests(TestCase):
    def test_Key_TextValue_HashTextAsKey(self):
        self.assertEqual(Prompt("Hello prompt!").key(), "t:0b290fd")

    def test_key_Prompt_TextReference_UseIdAsKey(self):
        self.assertEqual(Prompt("Hello prompt!","p1001").key(), "id:p1001")


if __name__ == '__main__':
    print(Prompt("Hello prompt!").key())
    print(Prompt("Hello prompt!","p1001").key())
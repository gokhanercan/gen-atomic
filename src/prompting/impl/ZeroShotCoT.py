# from typing import Union
#
# from prompting.Prompt import Prompt
# from prompting.impl.DirectPrompting import DirectPrompting
#
#
# class ZeroShotCoTPrompting(DirectPrompting):
#     """
#     Encourages the model to think step-by-step without giving any examples.
#     """
#
#     def __init__(self, prompt: Prompt) -> None:
#         super().__init__(prompt)
#
#     def generate(self):
#         #TODO: Mutate the prompt to add the zero-shot CoT instruction
#         pass
#
#
# if __name__ == '__main__':
#     print(ZeroShotCoTPrompting(Prompt("Hello prompt!")))
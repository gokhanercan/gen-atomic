from prompting.Prompt import Prompt
from prompting.repo.prompt_repository_base import PromptRepositoryBase


class InMemoryPromptRepository(PromptRepositoryBase):
    def __init__(self):
        super().__init__()
        self.prompts: dict[str, Prompt] = {}

        # region Data
        self.DEFAULT_PROMPT: str = (
            "You are a function that receives a [LANG_UNIT_DESC] instruction.\n"
            "Return **only** a single valid [LANG_UNIT_DESC] expression formatted according to the specified output format.\n"
            "Do not explain or comment.\n\n"
            "Instruction: [GEN_ATOMIC_UNIT_DESC]"
        )
        self.prompts["default"] = Prompt(self.DEFAULT_PROMPT, "default")
        self.prompts["regexval_default"] = Prompt(self.DEFAULT_PROMPT, "regexval_default")
        # decorators
        self.prompts["emotion"] = Prompt("I'm having a really hard time getting this right and I feel a bit stuck.", "emotion")
        self.prompts["hiddenzeroshotcot"] = Prompt(
            "Think step by step and show your reasoning before outputting the final code inside triple backticks.",
            "hiddenzeroshotcot",
        )
        self.prompts["format"] = Prompt(
            "Wrap the Output with the following {self.format_type.label} code block: ```\nOutput\n```", "format"
        )
        # endregion

    def add_prompt(self, prompt: Prompt):
        self.prompts[prompt.key()] = prompt

    def get_prompt(self, pid: str) -> Prompt:
        if pid in self.prompts:
            return self.prompts[pid]
        else:
            raise KeyError(f"Prompt with pid '{pid}' not found.")

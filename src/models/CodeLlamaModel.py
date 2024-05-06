import ollama

from models.ModelBase import ModelBase
from utility import StringHelper
from utility.StringHelper import Coelesce


class CodeLlamaModel(ModelBase):
    SYSTEM_PROMPT = f"""You are a helpful chatbot that has access to the following 
                    open-source models codellama.
                    You can can answer questions for users on any topic."""
    SAMPLE_PROMPT = f"""generate regex of email"""

    def __init__(self, langUnit: str = None) -> None:
        super().__init__()
        self.LangUnit = langUnit
        self.model = 'codellama'

    def Generate(self, description: str) -> str:
        print("<>>>>>>>>>>>>"+description)
        stream = ollama.chat(
            model="codellama",
            messages=[{'role': 'assistant', 'content': self.SYSTEM_PROMPT},
                      {'role': 'user', 'content': f"Model being used is {self.model}.{self.SAMPLE_PROMPT}"}],
            stream=True,
        )
        return stream

    def ModelName(self):
        return self.model

    def _chat(self, user_prompt, model):
        stream = ollama.chat(
            model=model,
            messages=[{'role': 'assistant', 'content': self.SYSTEM_PROMPT},
                      {'role': 'user', 'content': f"Model being used is {model}.{user_prompt}"}],
            stream=True,
        )
        return stream

    # stream response back from LLM
    def stream_parser(self, stream):
        for chunk in stream:
            yield chunk['message']['content']

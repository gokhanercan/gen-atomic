from langunits.LangUnit import LangUnitInfo
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase, GenRequest, GenResponse
import subprocess
import ollama
from colorama import init, Fore, Back, Style
from data.Dataset import *

from models.providers.ModelProviderBase import ModelProviderBase


class OllamaModelProvider(ModelProviderBase):
    def __init__(self, active_model_name: str = None) -> None:
        super().__init__()
        ModelBase.__init__(self)
        ModelProviderBase.__init__(self, active_model_name)

    def provider_name(self):
        return "ollama"

    def provider_abbreviation(self):
        return "ol"

    def model_names(self) -> list[str]:
        """
        Returns a list of names of locally installed/downloaded models.

        Note: This does not include all available models from the registry.

        Returns:
            list[str]: Names of installed models.
        """
        return [m["model"] for m in ollama.list().get("models", []) if "model" in m]

    def start_ollama_server(self):
        """
        #client examples: https://github.com/ollama/ollama-python/tree/main/examples
        # Use WSL command to launch Ollama on localhost (accessible from Windows)
        # For Win, Set env variable OLLAMA_MODELS for root models dir ref:https://github.com/ollama/ollama/blob/main/docs/faq.md#where-are-models-stored
        :return:
        """
        process = subprocess.Popen(
            ["ollama run", self.model_name()],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        process.communicate()
        return process

    @deprecated
    def Generate(self, description: str, langUnitInfo: LangUnitInfo) -> str:
        """
        TODO: https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=71867358
        :param description:
        :param langUnitInfo:
        :return:
        """
        # ollama_server_process = self.start_ollama_server()
        client = ollama.Client("http://localhost:11434")  # Specify full URL with port

        # prompt
        langDesc: str = langUnitInfo.prompt_text
        instruction: str = (
            f"Consider yourself a function that takes the input of asked {langDesc} statement, and "
            f"your output should be a markdown code snippet formatted in the following schema, including "
            f'the leading and trailing "```{langDesc}" and "```". Do not give me an explanation, only give '
            f"me a {langDesc} expression. Do not add any additional characters."
        )
        prompt: str = f"{instruction}\nAsked {langDesc} statement: {description}."
        promptColored: str = f"{instruction}\nAsked {langDesc} statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        # model call
        response = client.generate(model=self.model_name(), prompt=prompt)
        answer = response["response"]

        # ollama_server_process.terminate()       #TODO: Manage the connection. Do not terminate on every call.

        gencode: str = (
            str(answer)
            .strip()
            .replace("Regex: ", "")
            .replace("regexp", "")
            .replace("```", "")
            .replace("`", "")
            .replace("SQL: ", "")
        )  # TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

    def _generate_impl(self, req: GenRequest) -> GenResponse:
        client = ollama.Client("http://localhost:11434")  # TODO:Specify full URL with port

        response = client.generate(model=self.model_name(), prompt=req.final_prompt)
        answer = response["response"]

        # TODO: Output parsers here please!
        # generated: str = (
        #     str(answer)
        #     .strip()
        #     .replace("Regex: ", "")
        #     .replace("regexp", "")
        #     .replace("```", "")
        #     .replace("`", "")
        #     .replace("SQL: ", "")
        # )
        return GenResponse(req.lang_unit_info, answer)


if __name__ == "__main__":
    final_prompt: str = (
        "You are a function that generates 'Regular Expression Validator' code unit by instruction.\n"
        "Return **only** a single valid expression. \n"
        "Do not explain or comment.\n\n"
        "Instruction: 'General email compliant to RFC 5322 official standard'"
    )
    req: GenRequest = GenRequest(LangUnitFactory().create("RegexVal"), "Email address validator", None, final_prompt)
    res: GenResponse = OllamaModelProvider("llama3").generate(req)
    print(res)

    print(f"\n{res.raw_generated}")

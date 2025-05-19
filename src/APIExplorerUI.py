# List available providers and models here letting users to copy and paste keys and possible model configurations.
# usage: streamlit run --server.runOnSave trueL:/Projects/gen-atomic/src/ApiExplorer.py

import sys
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

from api.API import API
from data.Dataset import Dataset, Unit
from experiments.ModelConfiguration import ModelConfiguration
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelProviderMeta
from models.ModelFactory import ModelFactory, ModelFilters
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from prompting.direct.DirectPrompting import DirectPrompting

# region Sidebar
st.title("API Explorer")
st.sidebar.markdown("<h1 style='border1:1px solid red; margin-top:-50px;'>Resources</h1>", unsafe_allow_html=True)
bar = st.sidebar
api = API()
modelFactory = ModelFactory()

# langUnitNames = api.GetAllLangUnitNames()
# default_lang_index = langUnitNames.index("RegexVal")
# selLangUnit = bar.selectbox('LangUnits',langUnitNames, index=default_lang_index)

# Model Provider
modelProviderInfos = modelFactory.GetAllModelProviderInfos()
modelProviderInfos.append( ModelProviderMeta("[No Provider]", None,"np"))
modelProviderInfos.append( ModelProviderMeta("- All -", None,""))
selModelProvider = bar.selectbox('Model Providers',modelProviderInfos,  format_func=lambda u: u.Name + " (" + u.Abbreviation + ")" if u.Abbreviation != "" else u.Name, index=len(modelProviderInfos)-1)
selModelProviderAbbr = selModelProvider.Abbreviation
allProviders:bool = selModelProviderAbbr == ""

# Models
modelKeys:List[str] = modelFactory.FindKeysByFilters(ModelFilters(providerAbbr=None if allProviders else selModelProviderAbbr))
selModelKey = bar.selectbox("Effective Model Keys", modelKeys)

# Prompting
bar.divider()
promptingNames = ["Direct", "Few Shot", "CoT"]      #TODO: Load from factory
default_p_index = promptingNames.index("Direct")
selPrompting:str = bar.selectbox("Prompting Methods", promptingNames, index=default_p_index)
is_ref_prompt = bar.toggle("Is Reference Prompt", value=True)
prompt:Prompt = None
if is_ref_prompt:
    selPromptID: str = bar.selectbox("Prompt ID", ["DF", "P101", "P102"], index=0)      #TODO:Load from prompts repo
    prompt = Prompt("text is the prompt template text",selPromptID)
else:
    selPrompt:str = bar.text_input("Custom Prompt", "This is a sample prompt.", key="prompt")
    prompt = Prompt(selPrompt)
prompting:PromptingBase = DirectPrompting(prompt)

# endregion

# region Main
st.subheader("Model Configuration")
data = {
    'Name': ['Provider', 'ModelKey', 'Prompting'],
    'Value': [selModelProvider.Name.replace("- All -","-"), selModelKey,selPrompting],
}
df = pd.DataFrame(data)
st.dataframe(df, hide_index=True)
# st.markdown("**Model Configuration**")
modelFactory:ModelFactory = ModelFactory()
mc:ModelConfiguration = ModelConfiguration(model=modelFactory.CreateModelByKey(selModelKey), prompting=prompting)
modelConfigKey:str = selModelKey
# st.markdown(f"**Model Configuration Key:** {modelConfigKey}")
st.markdown("**Model Configuration Key**")
st.code(mc.key())
# endregion


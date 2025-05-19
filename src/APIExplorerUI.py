# List available providers and models here letting users to copy and paste keys and possible model configurations.

import sys
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

from api.API import API
from data.Dataset import Dataset, Unit
from experiments.ModelConfiguration import ModelConfiguration, StaticModelConfiguration
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelProviderMeta
from models.ModelFactory import ModelFactory, ModelFilters
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase, PromptingInfo
from prompting.impl.DirectPrompting import DirectPrompting
from prompting.prompting_factory import PromptingFactory

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
promptings:[PromptingInfo] = PromptingFactory().get_all_prompting_meta()
promptingNames = [p.plain_name for p in promptings]
selPrompting:PromptingInfo = bar.selectbox("Prompting Methods", promptings, format_func=lambda p: p.plain_name)
selPromptingImpl:PromptingBase = None
bar.markdown(f"<span style='font-size: 0.9em' title='This information is coming from the docstrings of the implementations'><i>{selPrompting.doc}</i></span>", unsafe_allow_html=True)
bar.divider()

# Dynamic Configurations
bar.subheader("Dynamic Configurations")
if(selPrompting.key == "direct"):
    with bar.expander("DirectPrompting", expanded=True):        # UI support provided manually for DirectPrompting for now!
        is_ref_prompt = st.toggle("Is a Reference Prompt", value=True)
        prompt: Prompt = None
        if is_ref_prompt:
            selPromptID: str = st.selectbox("Prompt ID", ["DF", "P101", "P102"], index=0)  # TODO:Load from prompts repo
            prompt = Prompt("text is the prompt template text", selPromptID)
        else:
            selPrompt: str = st.text_input("Custom Prompt", "This is a sample prompt.", key="prompt")
            prompt = Prompt(selPrompt)
        selPromptingImpl: PromptingBase = DirectPrompting(prompt)
# endregion

# endregion  #sidebar end

# region Main Content
st.subheader("Model Configuration")
data = {
    'Name': ['Provider Name', 'Static ModelKey', 'Static PromptingKey'],
    'Value': [selModelProvider.Name.replace("- All -","-"), selModelKey, selPrompting.plain_name],
}
df = pd.DataFrame(data)
st.dataframe(df, hide_index=True)

# Static Key
def render_static_key():
    smc: StaticModelConfiguration = StaticModelConfiguration(selModelKey, static_prompting_key=selPrompting.key)
    st.markdown("**Model Configuration Key (Static)**")
    st.code(smc.key())
render_static_key()

# Dynamic Key
try:
    mc: ModelConfiguration = ModelConfiguration(model=modelFactory.CreateModelByKey(selModelKey), prompting=selPromptingImpl)
    modelConfigKey: str = selModelKey
    st.markdown("**Model Configuration Key (Dynamic)**")
    st.code(mc.key())
except:
    st.warning("There is no UI support for the selected configuration. Please check the selected model and prompting method.")
    st.stop()

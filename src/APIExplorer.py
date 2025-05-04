# List available providers and models here letting users to copy and paste keys and possible model configurations.

import sys
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st

from api.API import API
from data.Dataset import Dataset, Unit
from experiments.ModelConfiguration import ModelConfiguration
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelFactory import ModelFactory
from prompting.direct.DirectPrompting import DirectPrompting

# region Sidebar
st.title("API Explorer")
st.sidebar.markdown("<h1 style='border1:1px solid red; margin-top:-50px;'>Resources</h1>", unsafe_allow_html=True)
bar = st.sidebar
api = API()

langUnitNames = api.GetAllLangUnitNames()
default_lang_index = langUnitNames.index("RegexVal")
selLangUnit = bar.selectbox('LangUnits',langUnitNames, index=default_lang_index)

modelProviderNames:List[str] = api.GetAllModelProviderNames()
modelProviderNames.append("No Provider (np)")
default_mp_index = modelProviderNames.index("No Provider (np)")
selModelProvider = bar.selectbox('Model Providers',modelProviderNames, index=default_mp_index)

modelKeys:List[str] = api.GetAllModelKeys()
selModelKey = bar.selectbox("Effective Model Keys", modelKeys)

promptingNames = ["Direct", "Few Shot", "CoT"]
default_p_index = promptingNames.index("Direct")
selPrompting:str = bar.selectbox("Prompting Methods", promptingNames, index=default_p_index)

selPrompt:str = bar.text_input("Sample Prompt", "This is a sample prompt.", key="prompt")
# endregion

# region Main
st.subheader("Model Configuration")
data = {
    'Name': ['LangUnit','Provider', 'Model', 'Prompting'],
    'Val': [selLangUnit, selModelProvider, "model",selPrompting],
}
df = pd.DataFrame(data)
st.dataframe(df, hide_index=True)
# st.markdown("**Model Configuration**")
modelFactory:ModelFactory = ModelFactory()
mc:ModelConfiguration = ModelConfiguration(model=modelFactory.CreateModelByKey(selModelKey), prompting=DirectPrompting(selPrompt))
modelConfigKey:str = selModelKey
# st.markdown(f"**Model Configuration Key:** {modelConfigKey}")
st.markdown("**Model Configuration Key**")
st.code(mc.key())
# endregion






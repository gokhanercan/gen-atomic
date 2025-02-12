#Run the following command:
    #streamlit run L:\Projects\gen-atomic\src\StreamlitUI.py

import sys
from pathlib import Path
from typing import List

import streamlit as st

from data.Dataset import Dataset, Unit
from data.DatasetXmlRepository import DatasetXmlRepository
from langunits.LangUnit import LangUnit, LangUnitInfo
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase
# from models.ModelBase import ModelBase, ModelConfInfo
from models.ModelFactory import ModelFactory
from utility.Paths import Paths

print(sys.version)

#region Sidebar
#st.sidebar.header("gen-atomic")         #ref: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
st.sidebar.markdown("<h1 style='border1:1px solid red; margin-top:-50px;'><u>gen-atomic</u></h1>", unsafe_allow_html=True)
bar = st.sidebar

#Dataset
bar.subheader("Dataset")
ds = bar.selectbox('Choose a dataset?',('AtomicRegexValDataset','Other'))
# dsPath = Paths().GetDataset("AtomicRegexValDataset")
dsPath = "../data/AtomicRegexValDataset.xml"    #TODO: Temporarily hardcoded.
bar.write("Dataset Path: ", dsPath)
bar.write("Project Root: ", Paths().GetProjectRoot())
bar.write("Executing Path: ", Path(__file__).resolve())
ds:Dataset = DatasetXmlRepository.Load(dsPath)
bar.write(f'Number of Samples: {len(ds.Units)}')
units = ds.Units
unit = units[0]
unit:Unit = bar.selectbox('Choose a sample to test?',units)
ccase = bar.selectbox('Choose a correct case?',unit.CorrectCases)
icase = bar.selectbox('Choose an incorrect case?',unit.IncorrectCases)
# for cc in field.CorrectCases:
#     st.write("CC -> " + cc)
# for ic in field.IncorrectCases:
#     st.write("IC -> " + ic)
# st.write(f'Selected UnitType: {field.UnitType.name}')

#Model
baselineMode:bool = True        #Should be true if the real models are not really available in the setup. TODO: Set via config.
bar.subheader("Model")
modelFactory = ModelFactory()
modelKeys:List[str] = modelFactory.GetModelKeys(baselineMode)
# bar.write("ModelKeys: ", modelKeys)
modelKey:str = bar.selectbox('Choose a model?', modelKeys)
# bar.write("ModelKey: ", modelKey)
model: ModelBase = ModelFactory().CreateModelByKey(modelKey)
modelName:str = model.Name()
bar.write("Model Name: ", modelName)

if "generatedCode" not in st.session_state: st.session_state.generatedCode = ""
if "result" not in st.session_state: st.session_state.result = False

if(modelName == "StubModel"):
    model.StubUnit = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
# bar.write(f"<b>Model:</b> {modelKey}", unsafe_allow_html=True)      #TODO: We need components to provide commonly used functionality like bolds, text colors etc.
# bar.write("<span style='color:red'>This text is red!</span>", unsafe_allow_html=True)
#endregion

#TRY
st.subheader("Configuration")
# st.write(f"<b>Model:</b> {modelKey}", unsafe_allow_html=True)
st.write(f"<b>LangUnit:</b> {unit.UnitType}", unsafe_allow_html=True)

st.subheader("Try")
# sampleText:str = st.text_input("Sample Text (feel free to update)",ccase)
userDesc:str = st.text_input("Description",unit.Description)
# generated = st.text_input("Generated Unit","")
# unit:UnitBase = UnitFactory().Create(field.UnitType)
langUnit:LangUnit = LangUnitFactory().Create(unit.UnitType)
langUnitInfo:LangUnitInfo = langUnit.CreateInfo()

ccase = st.text_area("Correct Case", ccase)


# if st.button("Generate"):
# st.session_state.generatedCode = st.text_area("Generated Code", st.session_state.generatedCode)
if (st.session_state.generatedCode == ""):
    # st.write(model.Generate(userDesc,langUnitInfo))
    st.session_state.generatedCode = model.Generate(userDesc,langUnitInfo)
st.session_state.generatedCode = st.text_area("Generated Code", st.session_state.generatedCode)

if st.session_state.generatedCode != "":
    st.session_state.result = langUnit.RunTest(st.session_state.generatedCode, ccase, None)
    st.text(f"Test Result: {st.session_state.result}")

if st.button("Generate New"):
    st.session_state.generatedCode = model.Generate(userDesc, langUnitInfo)





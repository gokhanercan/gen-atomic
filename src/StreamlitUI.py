#Run the following command:
    #streamlit run L:\Projects\gen-atomic\src\StreamlitUI.py
from typing import Optional

import streamlit as st
import os
from data.Dataset import Dataset, Unit
from data.DatasetXmlRepository import DatasetXmlRepository
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory
from units.UnitBase import UnitBase
from units.UnitFactory import UnitFactory
from utility.Paths import Paths

#region Sidebar
st.sidebar.header("My Sidebar")         #ref: https://docs.streamlit.io/get-started/tutorials/create-a-multipage-app
bar = st.sidebar

#Dataset
bar.subheader("Dataset")
ds = bar.selectbox('Choose a dataset?',('AtomicDataset','Other'))
dsPath = Paths().GetDataset("AtomicDataset")
bar.write("Dataset Path: ", dsPath)
ds: Dataset = DatasetXmlRepository.Load(dsPath)
bar.write(f'Number of Fields: {len(ds.Units)}')
field:Unit = bar.selectbox('Choose a field?',ds.Units)
ccase = bar.selectbox('Choose a correct case?',field.CorrectCases)
icase = bar.selectbox('Choose an inccorrect case?',field.IncorrectCases)
# for cc in field.CorrectCases:
#     st.write("CC -> " + cc)
# for ic in field.IncorrectCases:
#     st.write("IC -> " + ic)
# st.write(f'Selected UnitType: {field.UnitType.name}')

#Model
bar.subheader("Model")
modelName:str = bar.selectbox('Choose a model?',ModelFactory().ListModelNames())
model:ModelBase = ModelFactory().Create(modelName)
model.StubUnit = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
bar.write(f"<b>Model:</b> {modelName}",unsafe_allow_html=True)      #TODO: We need components to provide commonly used functionality like bolds, text colors etc.
# bar.write("<span style='color:red'>This text is red!</span>", unsafe_allow_html=True)

#endregion

#TRY
st.subheader("Configuration")
st.write(f"<b>Model:</b> {modelName}",unsafe_allow_html=True)
st.write(f"<b>LangUnit:</b> {field.UnitType.name}",unsafe_allow_html=True)

st.subheader("Try")
sampleText:str = st.text_input("Sample Text",ccase)
userDesc:str = st.text_input("Description",field.Description)
#generated = st.text_input("Generated Unit","")
unit:UnitBase = UnitFactory().Create(field.UnitType)
if st.button("Generate"):
    generated = model.Generate(userDesc)
    st.text_area("Generated Unit", generated)
    passed: bool = unit.RunTest(generated, sampleText)
    st.write("Evaluation Result:", passed)
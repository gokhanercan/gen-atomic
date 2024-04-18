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

root = os.getcwd()       #tests folder
#st.write("Root Path: ", root)

#Dataset
st.subheader("Dataset")
ds = st.selectbox('Choose a dataset?',('AtomicDataset','Other'))
dsPath = f"{root}//data//{ds}.xml"        #relation to project root. not src root.
#st.write("Dataset Path: ", dsPath)
ds: Dataset = DatasetXmlRepository.Load(dsPath)
#st.write(f'Number of Fields: {len(ds.Units)}')
field:Unit = st.selectbox('Choose a field?',ds.Units)
ccase = st.selectbox('Choose a correct case?',field.CorrectCases)
icase = st.selectbox('Choose an inccorrect case?',field.IncorrectCases)
# for cc in field.CorrectCases:
#     st.write("CC -> " + cc)
# for ic in field.IncorrectCases:
#     st.write("IC -> " + ic)
# st.write(f'Selected UnitType: {field.UnitType.name}')

#Model
st.subheader("Model")
modelName = st.selectbox('Choose a model?',ModelFactory().ListModelNames())
model:ModelBase = ModelFactory().Create(modelName)
model.StubUnit = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
st.write("Model: " + modelName)

#TRY
st.subheader("Try")
userDesc:str = st.text_input("Description",field.Description)
sampleText:str = st.text_input("Sample Text",ccase)
# generated = st.text_input("Generated Unit","")
unit:UnitBase = UnitFactory().Create(field.UnitType)
if st.button("Generate"):
    generated = model.Generate(userDesc)
    st.text_area("Generated Unit", generated)
    passed: bool = unit.RunTest(generated, sampleText)
    st.write("Evaluation Result:", passed)
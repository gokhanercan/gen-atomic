#Run the following command:
    #streamlit run L:\Projects\gen-atomic\src\StreamlitUI.py

import sys
from typing import List

import streamlit as st

from data.Dataset import Dataset, Unit
from data.DatasetXmlRepository import DatasetXmlRepository
from models.ModelBase import ModelBase, ModelConf
from models.ModelFactory import ModelFactory
from utility.Paths import Paths

print(sys.version)

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
modelFactory = ModelFactory()
modelConfigs:List[ModelConf] = modelFactory.GetModelConfigurations()
configKeys = [obj.ConfigKey() for obj in modelConfigs]

modelConf:ModelConf = bar.selectbox('Choose a model?', modelConfigs)
model: ModelBase = ModelFactory().CreateByCfg(modelConf)
modelName:str = model.ModelName()
modelKey:str = model.ConfigKey()

model.StubUnit = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
bar.write(f"<b>Model:</b> {modelKey}", unsafe_allow_html=True)      #TODO: We need components to provide commonly used functionality like bolds, text colors etc.
# bar.write("<span style='color:red'>This text is red!</span>", unsafe_allow_html=True)
#endregion

#TRY
st.subheader("Configuration")
st.write(f"<b>Model:</b> {modelKey}", unsafe_allow_html=True)
st.write(f"<b>LangUnit:</b> {field.UnitType.name}", unsafe_allow_html=True)

st.subheader("Try")
sampleText:str = st.text_input("Sample Text",ccase)
userDesc:str = st.text_input("Description",field.Description)
#generated = st.text_input("Generated Unit","")
#unit:UnitBase = UnitFactory().Create(field.UnitType)

def stream_parser(generated):       #TODO: Will be removed.
    for chunk in generated:
        yield chunk['message']['content']

if st.button("Generate"):
    generated = model.Generate(userDesc)  #inja 2
    stream_output = st.write_stream(stream_parser(generated))
    st.text_area("Generated Unit", stream_output)



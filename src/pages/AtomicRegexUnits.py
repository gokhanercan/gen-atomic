import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from data.DatasetXmlRepository import DatasetXmlRepository
from utility.Paths import Paths

st.title("Atomic Regex Units")

# Load dataset
path = Paths().GetDataset("AtomicRegexValDataset")

ds = DatasetXmlRepository.Load(path)

# Convert units to DataFrame
records = [{"Name": u.Name, "Description": u.Description, "UnitType": u.UnitType} for u in ds.Units]

df = pd.DataFrame(records)

# Configure AgGrid
builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_default_column(editable=True, resizable=True, filter=True)
options = builder.build()

AgGrid(df, gridOptions=options, allow_unsafe_jscode=True, editable=True)


import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from models.ModelFactory import ModelFactory

st.title("All Models")

# Initialize ModelFactory
modelFactory = ModelFactory()

# Try to get all models, but if providers fail, show only standalone models
model_index = {}
provider_error = None

try:
    model_index = modelFactory.model_index
except Exception as e:
    provider_error = str(e)
    # If full index fails, try to get at least standalone models
    st.warning(f"Could not load provider-based models: {e}")
    st.info("Showing standalone models only. Some model providers may not be available.")
    
    # Build a simplified index with just standalone models
    for name, meta in modelFactory.standalone_models_meta.items():
        try:
            model = modelFactory.create_model(name)
            key = model.key()
            from models.ModelBase import ModelMeta
            model_meta = ModelMeta(
                name=name,
                plain_name=model.plain_name(),
                key=key,
                standalone_model_meta=meta,
                model_provider_meta=None,
            )
            model_index[key] = model_meta
        except Exception as model_error:
            st.warning(f"Could not load model {name}: {model_error}")

if not model_index:
    st.error("No models could be loaded.")
    st.stop()

# Convert model metadata to DataFrame
records = []
for key, meta in model_index.items():
    provider_name = ""
    provider_abbr = ""
    model_type = "Standalone"
    
    if meta.model_provider_meta:
        provider_name = meta.model_provider_meta.name
        provider_abbr = meta.model_provider_meta.abbreviation
        model_type = "Provider-based"
    
    if meta.is_baseline:
        model_type = "Baseline"
    
    records.append({
        "Key": key,
        "Name": meta.name,
        "Plain Name": meta.plain_name,
        "Type": model_type,
        "Provider": provider_name,
        "Provider Abbr": provider_abbr,
    })

df = pd.DataFrame(records)

# Display summary statistics
st.subheader("Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Models", len(records))
with col2:
    baseline_count = len([r for r in records if r["Type"] == "Baseline"])
    st.metric("Baseline Models", baseline_count)
with col3:
    provider_count = len([r for r in records if r["Type"] == "Provider-based"])
    st.metric("Provider-based Models", provider_count)

# Configure AgGrid
st.subheader("Model Details")
builder = GridOptionsBuilder.from_dataframe(df)
builder.configure_default_column(editable=False, resizable=True, filter=True, sortable=True)
builder.configure_selection('single')
builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
options = builder.build()

AgGrid(df, gridOptions=options, allow_unsafe_jscode=True, fit_columns_on_grid_load=True)

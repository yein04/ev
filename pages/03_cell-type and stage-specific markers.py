import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import plotly.express as px
import plotly.graph_objects as go

# Page title
st.set_page_config(page_title='Cell-type and stage-specificitiy', page_icon='🔬')
st.title('🔬 Cell-type and Stage-specificities')

st.markdown("## Single-cell Transcriptomics")
#sc_dataset = st.sidebar.selectbox("Select Dataset:", ["Breast Cancer", "Liver Cancer", "Lung Cancer", "Ovarian Cancer", "Pancreatic Cancer", "Stomach Cancer"])

#adata = sc.read_h5ad("data/scrna/OCA_UNB_10X_E-MTAB-8107.h5ad")

#sc.pl.umap(adata)

#fig = go.Figure()
#fig.add_trace(go.Scatter(x=adata.obsm['X_umap'][:, 0], y=adata.obsm['X_umap'][:, 1]))

#st.plotly_chart(fig)

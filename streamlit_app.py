import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Page title
st.set_page_config(page_title='Extracellular Vesicle Marker Analysis', page_icon='📊')
st.title('📊 EV Biomarker Analysis')

with st.expander('About this app'):
  st.markdown('**What can this app do?**')
  st.info('Insert description')
  st.markdown('**How to use the app?**')
  st.warning('Insert description')
  
# Sidebar inputs
st.sidebar.subheader("Select Cancer to Analyze")
cancer_type = st.sidebar.selectbox("Select Cancer Type:", ["Breast Cancer", "Liver Cancer", "Lung Cancer", "Ovarian Cancer", "Pancreatic Cancer", "Stomach Cancer"])

st.session_state['cancer_type'] = cancer_type

st.markdown("Please select a cancer to analyze on the sidebar. For comparative analysis, you will be able to select ...")

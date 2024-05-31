import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# Page title
st.set_page_config(page_title='Differential Gene Expression', page_icon='🌋')
st.title('Differential Gene Expression')

# Get session state for previously selected cancer type

cancer_type = st.session_state.cancer_type

# Test volcano plot
# Define function to load data based on selected cancer type
def load_data(cancer_types):
    data_path = "data/markers/"
    file_name = {
        "Breast Cancer": "01_DEGsTreat_BRCA_all.csv",
        "Liver Cancer": "01_DEGsTreat_LIHC_all.csv",
        "Lung Cancer": "01_DEGsTreat_LUNG_all.csv",
        "Ovarian Cancer": "01_DEGsTreat_OV_all.csv",
        "Pancreatic Cancer": "01_DEGsTreat_PAAD_all.csv",
        "Stomach Cancer": "01_DEGsTreat_STAD_all.csv"
    }[cancer_types]
    return pd.read_csv(data_path + file_name)


st.markdown('Get genes that are differentially expressed in '+cancer_type.lower()+" TCGA compared to GTEx")


# Sidebar inputs
st.sidebar.subheader("Significance cutoff for Volcano Plot")
st.sidebar.markdown("Set cutoffs here to visualize and export gene list")

#cancer_type = st.sidebar.selectbox("Select Cancer Type:", ["Breast Cancer", "Liver Cancer", "Lung Cancer", "Ovarian Cancer", "Pancreatic Cancer", "Stomach Cancer"])
p_value_cutoff = st.sidebar.slider("P-Value Cutoff:", min_value=0.0, max_value=500.0, value=1.3, step=10.0)
fold_change_cutoff = st.sidebar.slider("Absolute Fold Change Cutoff:", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
top_genes = st.sidebar.slider("Number of Top Genes to Label:", min_value=1, max_value=50, value=2)

st.session_state['p_value_cutoff'] = p_value_cutoff
st.session_state['fold_change_cutoff'] = fold_change_cutoff

# Load data
data = load_data(cancer_type)

# Apply -log10 transformation to 'adj.P.Val'
data['-log10(adj.P.Val)'] = -np.log10(data['adj.P.Val'])

# Generate volcano plot
data_pos = data[data['logFC'].abs() > fold_change_cutoff]
data_neg = data[data['logFC'] < -fold_change_cutoff]

fig = go.Figure()

# Add scatter traces for data points
fig.add_trace(go.Scatter(x=data['logFC'], y=data['-log10(adj.P.Val)'], mode='markers', marker=dict(color='grey', size=5), showlegend=False, text=data_neg['Unnamed: 0']))

fig.add_trace(go.Scatter(x=data_pos['logFC'], y=data_pos['-log10(adj.P.Val)'], mode='markers', marker=dict(color='red', size=5), name='Upregulated Genes', text=data_pos['Unnamed: 0']))
fig.add_trace(go.Scatter(x=data_neg['logFC'], y=data_neg['-log10(adj.P.Val)'], mode='markers', marker=dict(color='blue', size=5), name='Downregulated Genes', text=data_neg['Unnamed: 0']))

# Add grey dotted lines for cutoffs
fig.add_shape(type='line', x0=min(data['logFC']), y0=p_value_cutoff, x1=max(data['logFC']), y1=p_value_cutoff, line=dict(color='grey', width=1, dash='dot'))
fig.add_shape(type='line', x0=-fold_change_cutoff, y0=0, x1=-fold_change_cutoff, y1=max(data['-log10(adj.P.Val)']), line=dict(color='grey', width=1, dash='dot'))
fig.add_shape(type='line', x0=fold_change_cutoff, y0=0, x1=fold_change_cutoff, y1=max(data['-log10(adj.P.Val)']), line=dict(color='grey', width=1, dash='dot'))

# Get top n genes
top_genes_pos = data_pos.nlargest(top_genes, 'logFC')
top_genes_neg = data_neg.nsmallest(top_genes, 'logFC')

# Add annotations for top genes, slightly offset# Add annotations for top genes with slight offset
for index, row in top_genes_pos.iterrows():
    fig.add_annotation(x=row['logFC'], y=row['-log10(adj.P.Val)'], text=row['Unnamed: 0'], opacity=1, font=dict(color="black"), showarrow=False)

for index, row in top_genes_neg.iterrows():
    fig.add_annotation(x=row['logFC'], y=row['-log10(adj.P.Val)'], text=row['Unnamed: 0'], font=dict(color="black"), showarrow=False)

# Remove title and adjust space for it
# Update layout to box legend and place it on the right side
fig.update_layout(
    xaxis_title="Log2 Fold Change",
    yaxis_title="-Log10 Adjusted P-Value",
    showlegend=True,
    legend=dict(
        x=1.02,
        y=0.5
    ),
    yaxis=dict(range=[0, max(data['-log10(adj.P.Val)'])]),
    hovermode="closest",
    margin=dict(t=0, b=0, l=0, r=0)
)

st.plotly_chart(fig)

# Function to download genes
def download_genes():
    filtered_data = data[(data['-log10(adj.P.Val)'] > p_value_cutoff) & (data['logFC'].abs() > fold_change_cutoff)]
    csv = filtered_data.to_csv(index=False)
    return csv

if st.button("Download Significant Genes"):
    csv = download_genes()
    st.download_button(label="Download Genes CSV", data=csv, file_name=f"{cancer_type}_DEGs.csv", mime='text/csv')

# Store top up-regulated or down-regulated genes in session state

top_up = data[(data['-log10(adj.P.Val)'] > p_value_cutoff) & (data['logFC'] > fold_change_cutoff)]
top_down = data[(data['-log10(adj.P.Val)'] > p_value_cutoff) & (data['logFC'] < -fold_change_cutoff)]
top_up_csv = top_up.to_csv(index=False)
top_down_csv = top_down.to_csv(index=False)

st.session_state['top_up'] = top_up_csv
st.session_state['top_down'] = top_down_csv

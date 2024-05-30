import streamlit as st
import pandas as pd
import numpy as np

## Function to load gene lists from CSV files
def load_gene_list(gene_list_names):
    data = {}
    for name in gene_list_names:
        data_path = "data/pathway_genes/"
        file_name = {
            "Immune Pathways": "Immune Pathways.csv",
            "EV-related": "EV-related.csv",
            "Prognosis": "Prognosis.csv"
        }[name]
        data[name] = pd.read_csv(data_path + file_name)
    return data

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

# Page title
st.set_page_config(page_title='Subset and Characterize Markers', page_icon='🔎')
st.title('Subset and Characterize Markers')

# Sidebar inputs
st.sidebar.subheader("Subset markers")
gene_interests = st.sidebar.multiselect("Gene lists:", ["Immune Pathways", "EV-related", "Prognosis"])
cancer_interests = st.sidebar.multiselect("Cancer type:", ["Breast Cancer", "Liver Cancer", "Lung Cancer", "Ovarian Cancer", "Pancreatic Cancer", "Stomach Cancer"])

# Load gene lists 
data = load_gene_list(gene_interests)

# Filter data based on significance cutoffs
top_up = st.session_state.top_up
top_down = st.session_state.top_down

# Load gene lists selected by the user
selected_genes = []
for gene_list in gene_interests:
    genes = load_gene_list(gene_list)
    selected_genes.append(genes)

# Find overlapping genes
if selected_genes:
    overlapping_genes = set(selected_genes[0])
    for genes in selected_genes[1:]:
        overlapping_genes.intersection_update(set(genes))

    st.write("Overlapping Genes:")
    st.write(overlapping_genes)
else:
    st.write("No gene lists selected.")

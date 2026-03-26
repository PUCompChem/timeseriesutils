# + tags=["parameters"]
upstream = ['filter_data']
product = None

# -

import pandas as pd
import os
import glob
import plotly.express as px
import plotly.io as pio
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def generate_2d_pca(data_standardized, node_names) -> None:
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data_standardized)
        
    pca_df = pd.DataFrame({
        "PC1": principal_components[:, 0],
        "PC2": principal_components[:, 1],
        "Node Name": node_names})
    
    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        text="Node Name",
        title="PCA",
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"})

    fig.update_traces(marker=dict(size=5, opacity=0.7), textposition="top center")
    fig.update_layout(scene=dict(
        xaxis_title="Principal Component 1",
        yaxis_title="Principal Component 2",))

    pca_2d_html = 'pca_2d.html'
    pio.write_html(fig, file=os.path.join(product['generated_PCA'], pca_2d_html), auto_open=False)

    pca_2d_png = 'pca_2d.png'
    pio.write_image(fig, file=os.path.join(product['generated_PCA'], pca_2d_png), width=1200, height=800)

def generate_3d_pca(data_standardized, node_names) -> None:
    pca = PCA(n_components=3)
    principal_components = pca.fit_transform(data_standardized)

    pca_df = pd.DataFrame({
        "PC1": principal_components[:, 0],
        "PC2": principal_components[:, 1],
        "PC3": principal_components[:, 2],
        "Node Name": node_names})
    
    fig = px.scatter_3d(
        pca_df,
        x="PC1",
        y="PC2",
        z="PC3",
        text="Node Name",
        title="PCA",
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2", "PC3": "Principal Component 3"})

    fig.update_traces(marker=dict(size=5, opacity=0.7), textposition="top center")
    fig.update_layout(scene=dict(
        xaxis_title="Principal Component 1",
        yaxis_title="Principal Component 2",
        zaxis_title="Principal Component 3"))

    pca_3d_html = 'pca_3d.html'
    pio.write_html(fig, file=os.path.join(product['generated_PCA'], pca_3d_html), auto_open=False)

    pca_3d_png = 'pca_3d.png'
    pio.write_image(fig, file=os.path.join(product['generated_PCA'], pca_3d_png), width=1200, height=800)

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data']['filtered_data'], '*.csv'))[0])

df = df.transpose()

node_names = df.iloc[:, 0]
node_names = node_names.index

numeric_data = df.iloc[:, 0:].values

scaler = StandardScaler()
data_standardized = scaler.fit_transform(numeric_data)

os.makedirs(product['generated_PCA'], exist_ok=True)

generate_2d_pca(data_standardized, node_names)
generate_3d_pca(data_standardized, node_names)
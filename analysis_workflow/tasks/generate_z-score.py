# + tags=["parameters"]
upstream = ['calc_kNN']
product = None

# -

import pandas as pd
import plotly.express as px
import os
import glob
from scipy.stats import zscore

df = pd.read_csv(glob.glob(os.path.join(upstream['calc_kNN']['calculated_kNN'], '*.csv'))[0])
df['Z-Score'] = zscore(df['Row_Mean'])

fig = px.bar(df, 
    x='Nodes', 
    y='Z-Score', 
    title="Z-Score",
    labels={'Z-Score': 'Z-Score', 'Nodes': 'Nodes'},
    text=df['Z-Score'].round(2),
    color=df['Z-Score'],
    color_continuous_scale="bluered")

fig.add_shape(type="line", 
    x0=-0.5, x1=len(df)-0.5, 
    y0=-3, y1=-3, 
    line=dict(color="green", width=2, dash="dash"),
    name="Lower Threshold (-3)")

fig.add_shape(type="line", 
    x0=-0.5, x1=len(df)-0.5, 
    y0=3, y1=3, 
    line=dict(color="red", width=2, dash="dash"),
    name="Upper Threshold (3)")

os.makedirs(product['generated_z-score'], exist_ok=True)

output_file_csv = 'z-score.csv'
df.to_csv(os.path.join(product['generated_z-score'], output_file_csv), index=False)

output_file_html = 'z-score.html'
fig.write_html(os.path.join(product['generated_z-score'], output_file_html), auto_open=False)
# + tags=["parameters"]
upstream = ['filter_data_nodes']
product = None

# -

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def plot_correlation(df, name) -> None:
    correlation_matrix = df[['pm_2.5', 'pm_10.0', 'atm_preassure', 'temperature', 'humidity']].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Correlation Heatmap of ' + name.replace('filtered_', '').replace('.csv', ''))

    output_file_name = name.replace('filtered_', '').replace('.csv', '') + '_heatmap.png'
    plt.savefig(os.path.join(product['generated_heatmap'], output_file_name), bbox_inches='tight')

    plt.clf()

os.makedirs(product['generated_heatmap'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['filter_data_nodes']['filtered_data_nodes'], '*.csv')):
    df = pd.read_csv(file_path)

    aggregated_df = plot_correlation(df, os.path.basename(file_path))
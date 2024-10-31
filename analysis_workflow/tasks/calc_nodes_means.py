# + tags=["parameters"]
upstream = ['filter_data_nodes']
product = None

# -

from scipy.stats import gmean, hmean
import pandas as pd
import numpy as np
import os
import glob

def calc_means(df) -> pd.DataFrame:
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df_with_values = pd.DataFrame()

    for var in df:
        arithmetic_mean = np.mean(df[var])
        quadratic_mean = np.sqrt(np.mean(df[var]**2))

        if (df[var] <= 0).any():
            geometric_mean = np.nan
            harmonic_mean = np.nan
        else:
            geometric_mean = gmean(df[var])
            harmonic_mean = hmean(df[var])
        
        df_with_values[var] = (arithmetic_mean, geometric_mean, harmonic_mean, quadratic_mean)

    return df_with_values

os.makedirs(product['calculated_nodes_means'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['filter_data_nodes']['filtered_data_nodes'], '*.csv')):
    df = pd.read_csv(file_path)

    df_with_means = calc_means(df)
    df_with_means.insert(0, 'mean_type', ['arithmetic_mean', 'geometric_mean', 'harmonic_mean', 'quadratic_mean'])

    output_file_name = 'means_' + os.path.basename(file_path).replace('filtered_', '')
    df_with_means.to_csv(os.path.join(product['calculated_nodes_means'], output_file_name), index=False)
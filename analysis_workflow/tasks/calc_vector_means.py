# + tags=["parameters"]
upstream = ['filter_data']
product = None

# +
from scipy.stats import gmean, hmean
import pandas as pd
import numpy as np
import os
import glob

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data']['filtered_data'], '*.csv'))[0])

df_means = pd.DataFrame({'mean_type': ['arithmetic_mean', 'geometric_mean', 'harmonic_mean', 'quadratic_mean']})

for node_name in df:
    arithmetic_mean = np.mean(df[node_name])
    quadratic_mean = np.sqrt(np.mean(df[node_name]**2))

    if (df[node_name] <= 0).any():
        geometric_mean = np.nan
        harmonic_mean = np.nan
    else:
        geometric_mean = gmean(df[node_name])
        harmonic_mean = hmean(df[node_name])

    df_means[node_name] = (arithmetic_mean, geometric_mean, harmonic_mean, quadratic_mean)

os.makedirs(product['calculated_vector_means'], exist_ok=True)
output_file_name = 'all_nodes_means.csv'
df_means.to_csv(os.path.join(product['calculated_vector_means'], output_file_name), index=False)
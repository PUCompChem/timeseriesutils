# + tags=["parameters"]
upstream = ['aggregate_nodes']
product = None

# -

import pandas as pd
import os
import glob

os.makedirs(product['filtered_data_nodes'], exist_ok=True)
containsZero = False

for file_path in glob.glob(os.path.join(upstream['aggregate_nodes']['aggregated_nodes'], '*.csv')):
    df = pd.read_csv(file_path)

    if df.isna().any().any():
        continue
    elif df.empty:
        continue

    for col in df.columns:
        if (df[col] == 0).any() and (col not in ['temperature', 'humidity']):
            containsZero = True
            break

    if containsZero:
        containsZero = False
        continue

    if df.shape[0] == 1:
        continue

    output_file_name = 'filtered_' + os.path.basename(file_path).replace('agg_', '')
    df.to_csv(os.path.join(product['filtered_data_nodes'], output_file_name), index=False)
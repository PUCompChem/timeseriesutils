# + tags=["parameters"]
upstream = ['aggregate_data_vectors']
product = None
var = None

# -

import pandas as pd
import os
import glob

df = pd.read_csv(glob.glob(os.path.join(upstream['aggregate_data_vectors']['aggregated_data_vectors'], '*.csv'))[0])

if var not in ['temperature', 'humidity']:
    df = df.drop(columns=[col for col in df.columns if (df[col] == 0).all()])
df = df.dropna(axis=1)

os.makedirs(product['filtered_data_with_datetime'], exist_ok=True)
output_file_name = 'filtered_data_with_datetime.csv'
df.to_csv(os.path.join(product['filtered_data_with_datetime'], output_file_name), index=False)
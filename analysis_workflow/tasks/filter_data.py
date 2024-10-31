# + tags=["parameters"]
upstream = ['filter_data_with_datetime']
product = None

# -

import pandas as pd
import os
import glob

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data_with_datetime']['filtered_data_with_datetime'], '*.csv'))[0])

df = df.drop(columns='datetime')

os.makedirs(product['filtered_data'], exist_ok=True)
output_file_name = 'filtered_data.csv'
df.to_csv(os.path.join(product['filtered_data'], output_file_name), index=False)
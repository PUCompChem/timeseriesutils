# + tags=["parameters"]
upstream = None
product = None
folder_input = None
year = None
start_date = None
end_date = None
period = None
agg_type = None

# -

import pandas as pd
import os
import glob

def calc_vector(df, year, start_date, end_date, period, agg_type) -> pd.DataFrame:
    col_datetime_str = 'datetime' if 'datetime' in df.columns else 'Date/Time'
    df['datetime'] = pd.to_datetime(df[col_datetime_str])

    if year != 0:
        df = df[(df['datetime'].dt.year == year)]
    elif start_date != '' and end_date != '':
        df = df[(df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

    if agg_type == 'min':
        df = df.groupby(pd.Grouper(key='datetime', freq=period)).min(numeric_only=True)
    elif agg_type == 'mean':
        df = df.groupby(pd.Grouper(key='datetime', freq=period)).mean(numeric_only=True)
    elif agg_type == 'max':
        df = df.groupby(pd.Grouper(key='datetime', freq=period)).max(numeric_only=True)
    df = df.reset_index()
    del df['unixtime']

    return df

os.makedirs(product['aggregated_nodes'], exist_ok=True)

for file_path in glob.glob(os.path.join(folder_input, '*.csv')):
    df = pd.read_csv(file_path)

    aggregated_df = calc_vector(df, year, start_date, end_date, period, agg_type)

    output_file_name = 'agg_' + os.path.basename(file_path)
    aggregated_df.to_csv(os.path.join(product['aggregated_nodes'], output_file_name), index=False)
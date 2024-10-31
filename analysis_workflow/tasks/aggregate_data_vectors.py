# + tags=["parameters"]
upstream = None
product = None
folder_input = None
var = None
year = None
start_date = None
end_date = None
period = None
agg_type = None

# -

import pandas as pd
import os
import glob

def get_date(year, start_date, end_date, period, agg_type) -> pd.Series:
    df = pd.read_csv(glob.glob(os.path.join(folder_input, '*.csv'))[0])
    df = calculate(df, year, start_date, end_date, period, agg_type)

    vector = ([df['datetime'].iloc[x] for x in range(len(df))])

    return vector

def calc_vector(df, year, start_date, end_date, var, period, agg_type) -> pd.DataFrame:
    df = calculate(df, year, start_date, end_date, period, agg_type)

    agg_df = df[['datetime', var]]

    return agg_df

def calculate(df, year, start_date, end_date, period, agg_type) -> pd.Series:
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

    return df

df_with_vectors = pd.DataFrame()
df_with_vectors['datetime'] = get_date(year, start_date, end_date, period, agg_type)

for file_path in glob.glob(os.path.join(folder_input, '*.csv')):
    input_df = pd.read_csv(file_path)

    agg_df = calc_vector(input_df, year, start_date, end_date, var, period, agg_type)
    agg_df = agg_df.rename(columns={var: os.path.basename(file_path).rstrip('.csv')})

    df_with_vectors = pd.merge(df_with_vectors, agg_df, on='datetime', how='outer')

os.makedirs(product['aggregated_data_vectors'], exist_ok=True)
output_file_name = 'agg_vectors.csv'
df_with_vectors.to_csv(os.path.join(product['aggregated_data_vectors'], output_file_name), index=False)
# + tags=["parameters"]
upstream = ['filter_data_nodes']
product = None
var = None

# -

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import glob

def get_name(var) -> str:
    var_name = ''
    if var in ['pm_2.5', 'pm_10.0']:
        var_name = var + ' Particle Size (µg/m³)'
    elif var == 'temperature':
        var_name = 'Temperature (°C)'
    elif var == 'humidity':
        var_name = 'Humidity (%)'
    elif var == 'atm_preassure':
        var_name = 'Atmospheric Pressure (hPa)'

    return var_name

def plot_correlation(df, var, name, var_name) -> None:
    for df_curr_var in [col for col in df.columns if col != var]:
        correlation_df = pd.DataFrame({var: df[var].values, df_curr_var: df[df_curr_var].values})

        sns.scatterplot(x=var, y=df_curr_var, data=correlation_df)

        df_curr_var_name = get_name(df_curr_var)

        plt.xlabel(var_name)
        plt.ylabel(df_curr_var_name)
        plt.title('Scatter Plot of ' + name.replace('filtered_', '').replace('.csv', ''))

        output_file_name = name.replace('filtered_', '').replace('.csv', '') + '_' + var + '_' + df_curr_var + '.png'
        plt.savefig(os.path.join(product['generated_scatterplot'], output_file_name), bbox_inches='tight')

        plt.clf()

os.makedirs(product['generated_scatterplot'], exist_ok=True)
var_name = get_name(var)

for file_path in glob.glob(os.path.join(upstream['filter_data_nodes']['filtered_data_nodes'], '*.csv')):
    df = pd.read_csv(file_path)
    df.drop(columns=df.columns[0], axis=1, inplace=True)

    aggregated_df = plot_correlation(df, var, os.path.basename(file_path), var_name)
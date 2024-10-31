# + tags=["parameters"]
upstream = ['filter_data_with_datetime']
product = None
var = None

# -

import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def plot_histogram(node_data, node_name, ylabel) -> None:
    plt.figure(figsize=(12, 6))
    plt.bar(df['datetime'], node_data)
    
    plt.xlabel('Date', fontweight='bold')
    plt.xticks(rotation=45)
    plt.ylabel(ylabel, fontweight='bold')
    plt.title(node_name, fontweight='bold')
    
    output_file_name = node_name + '.png'
    plt.savefig(os.path.join(product['generated_histograms'], output_file_name), bbox_inches='tight')

    plt.clf()

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data_with_datetime']['filtered_data_with_datetime'], '*.csv'))[0])
os.makedirs(product['generated_histograms'], exist_ok=True)

ylabel = ''
if var in ['pm_2.5', 'pm_10.0']:
    ylabel = var + ' Concentration (µg/m³)'
elif var == 'temperature':
    ylabel = 'Temperature (°C)'
elif var == 'humidity':
    ylabel = 'Humidity (%)'
elif var == 'atm_preassure':
    ylabel = 'Atmospheric Pressure (hPa)'

for node_name in df.columns[1:]:
    plot_histogram(df[node_name].values, node_name, ylabel)
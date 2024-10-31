# + tags=["parameters"]
upstream = ['filter_data_nodes']
product = None

# -

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

def plot_seriesplot(df, name):
    df['datetime'] = pd.to_datetime(df['datetime'])

    plt.figure(figsize=(16, 8))

    plt.subplot(3, 1, 1)
    plt.plot(df['datetime'], df['pm_2.5'], label='PM2.5', color='red', marker='o')
    plt.plot(df['datetime'], df['temperature'], label='Temperature', color='orange', marker='o')
    plt.title('PM2.5 and Temperature Trends')
    plt.legend(loc='upper right')

    plt.xticks(rotation=45, fontsize=7)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

    plt.subplot(3, 1, 2)
    plt.plot(df['datetime'], df['pm_10.0'], label='PM10', color='blue', marker='o')
    plt.plot(df['datetime'], df['temperature'], label='Temperature', color='orange', marker='o')
    plt.title('PM10 and Temperature Trends')
    plt.legend(loc='upper right')

    plt.xticks(rotation=45, fontsize=7)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

    plt.subplot(3, 1, 3)
    plt.plot(df['datetime'], df['pm_2.5'], label='PM2.5', color='red', marker='o')
    plt.plot(df['datetime'], df['pm_10.0'], label='PM10', color='blue', marker='o')
    plt.plot(df['datetime'], df['temperature'], label='Temperature', color='orange', marker='o')
    plt.plot(df['datetime'], df['humidity'], label='Humidity', color='green', marker='o')
    plt.title('PM2.5, PM10, Temperature and Humidity Trends')
    plt.legend(loc='upper right')

    plt.xticks(rotation=45, fontsize=7)
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

    plt.tight_layout()

    output_file_name = name.replace('filtered_', '').replace('.csv', '') + '_seriesplot.png'
    plt.savefig(os.path.join(product['generated_seriesplot'], output_file_name), bbox_inches='tight')

    plt.clf()

os.makedirs(product['generated_seriesplot'], exist_ok=True)

for file_path in glob.glob(os.path.join(upstream['filter_data_nodes']['filtered_data_nodes'], '*.csv')):
    df = pd.read_csv(file_path)

    aggregated_df = plot_seriesplot(df, os.path.basename(file_path))
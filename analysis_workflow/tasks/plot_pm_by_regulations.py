# + tags=["parameters"]

upstream = ['aggregate_nodes']
product = None
folder_input = None
year = None
start_date = None
end_date = None
period = None
agg_type = None
# -

import glob
import os
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def pm_by_year_norm(df1, feature1, feature2, date, output_filename):
    """
       The function works as expected when the period is 'Y', 'YE', or 'YS',
       based on yearly regulatory norms for PM 10 and PM 2.5.
       It also works for monthly periods such as 'M', 'ME', and 'MS'
    """

    fig = go.Figure()
    df1[feature1] = pd.to_numeric(df1[feature1], errors='coerce')
    df1[feature2] = pd.to_numeric(df1[feature2], errors='coerce')
    df1[feature1] = df1[feature1].fillna(0)
    df1[feature2] = df1[feature2].fillna(0)

    df1['color1'] = df1[feature1].apply(lambda x: 'LimeGreen' if x > 40 else 'Green')
    df1['color2'] = df1[feature2].apply(lambda x: 'DeepSkyBlue' if x > 20 else 'Blue')

    fig.add_trace(go.Scatter(x=df1[date].values, y=df1[feature1].values,
                             mode='markers',
                             text=df1[feature1].values,
                             textposition="top center",
                             marker=dict(size=df1[feature1], color=df1['color1'].values),
                             hoverinfo='x+name+text',
                             name='PM10 [ug/m3]'))

    fig.add_trace(go.Scatter(x=df1[date].values, y=df1[feature2].values,
                             mode='markers',
                             marker=dict(size=df1[feature2], color=df1['color2'].values),
                             text=df1[feature2].values,
                             textposition="top center",
                             hoverinfo='x+name+text',
                             name='PM2.5 [ug/m3]'))

    #     fig.update_layout(
    #     margin=dict(l=20, r=20, t=35, b=20))
    fig.update_layout(
        # xaxis_title="year",
        yaxis_title="PM [ug/m3]",
        legend_title="values exceeding regulation norm")
    fig.add_hline(y=40, line_color='Green', line_dash='dash')
    fig.add_hline(y=20, line_color='Blue', line_dash='dash')

    fig.write_html(output_filename)


def pm_by_daily_norm(df, feature, data, output_filename):

    """
       The function works as expected when the period is 'D',
       based on the daily regulatory norm for PM 10.
    """

    df.reset_index(inplace=True)
    df[data] = pd.to_datetime(df[data])
    df['year'] = df[data].dt.year
    df['month'] = df[data].dt.month
    df['day'] = df[data].dt.day
    df[feature] = pd.to_numeric(df[feature], errors='coerce')
    df[feature] = df[feature].fillna(0)

    df['color1'] = df[feature].apply(lambda x: 'Red' if x > 50 else 'Blue')
    fig = px.scatter(df, x="month", y=feature, facet_col="year", size=feature,
                     hover_data=['day'], color="color1")
    fig.update_xaxes(matches=None)
    fig.update_layout(showlegend=False)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    fig.write_html(output_filename)


csv_files = glob.glob(os.path.join(upstream['aggregate_nodes']['aggregated_nodes'], '*.csv'))

os.makedirs(product['plots'], exist_ok=True)

for file in csv_files:
    df = pd.read_csv(file)
    file_name = os.path.basename(file)
    output_file = os.path.join(product['plots'], os.path.splitext(file_name)[0])

    pm_by_year_norm(df, 'pm_10.0', 'pm_2.5', 'datetime', f'{output_file}_by_year.html')
    pm_by_daily_norm(df, 'pm_10.0', 'datetime', f'{output_file}_by_day.html')

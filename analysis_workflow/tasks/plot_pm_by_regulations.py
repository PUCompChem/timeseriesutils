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


def pm_by_year_norm(df, feature1, feature2, date, output_filename):
    """
       The function works as expected when the period is 'Y', 'YE', or 'YS',
       based on yearly regulatory norms for PM 10 and PM 2.5.
       It also works for monthly periods such as 'M', 'ME', and 'MS'
    """
    df1 = df.copy(deep=True)
    fig = go.Figure()
    df1[feature1] = pd.to_numeric(df1[feature1], errors='coerce')
    df1[feature2] = pd.to_numeric(df1[feature2], errors='coerce')
    df1[feature1] = df1[feature1].fillna(0)
    df1[feature2] = df1[feature2].fillna(0)

    df1['color1'] = df1[feature1].apply(lambda x: 'LimeGreen' if x > 40 else 'Green')
    df1['color2'] = df1[feature2].apply(lambda x: 'DeepSkyBlue' if x > 20 else 'Blue')

    date_labels = pd.to_datetime(df1[date]).dt.year.astype(str)

    #use date_labels instead of df1[date].values
    #to avoid  Plotly/pandas issue with how year-end dates are handled
    fig.add_trace(go.Scatter(x=date_labels, y=df1[feature1].values,
                             mode='markers+text',
                             text=df1[feature1].round(1).values,
                             textposition="middle right",
                             marker=dict(size=df1[feature1], color=df1['color1'].values),
                             hoverinfo='x+name+text',
                             name='PM10 [ug/m3]'))

    fig.add_trace(go.Scatter(x=date_labels, y=df1[feature2].values,
                             mode='markers+text',
                             marker=dict(size=df1[feature2], color=df1['color2'].values),
                             text=df1[feature2].round(1).values,
                             textposition="middle right",
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
    df1 = df.copy(deep=True)
    df1.reset_index(inplace=True)
    df1[data] = pd.to_datetime(df1[data])
    df1['year'] = df1[data].dt.year
    df1['month'] = df1[data].dt.month
    df1['day'] = df1[data].dt.day
    df1[feature] = pd.to_numeric(df[feature], errors='coerce')
    df1[feature] = df1[feature].fillna(0)

    df1['color1'] = df1[feature].apply(lambda x: 'Red' if x > 50 else 'Blue')
    fig = px.scatter(df1, x="month", y=feature, facet_col="year", size=feature,
                     hover_data=['day'], color="color1")
    fig.update_xaxes(matches=None)
    fig.update_layout(showlegend=False)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

    fig.write_html(output_filename)
    return df1


csv_files = glob.glob(os.path.join(upstream['aggregate_nodes']['aggregated_nodes'], '*.csv'))

os.makedirs(product['plots'], exist_ok=True)

combined_df = pd.DataFrame()
for file in csv_files:
    df = pd.read_csv(file)
    file_name = os.path.basename(file)
    output_file = os.path.join(product['plots'], os.path.splitext(file_name)[0])

    pm_by_year_norm(df, 'pm_10.0', 'pm_2.5', 'datetime', f'{output_file}_by_year.html')
    df_result = pm_by_daily_norm(df, 'pm_10.0', 'datetime', f'{output_file}_by_day.html')

    node_name = file_name.split('_')[1].split('.')[0]
    result = df_result.groupby(['year', 'color1']).size().reset_index(name='count')
    result['node'] = node_name
    red_data = result[result['color1'] == 'Red']
    combined_df = pd.concat([combined_df, red_data], ignore_index=True)

del combined_df['color1']
combined_df['year'] = combined_df['year'].astype(str)
combined_df['year'] = pd.Categorical(combined_df['year'], categories=sorted(combined_df['year'].unique()), ordered=True)
combined_df = combined_df.sort_values('year')
print(combined_df)

all_years = sorted(combined_df['year'].unique())
all_nodes = combined_df['node'].unique()
all_combinations = pd.MultiIndex.from_product([all_years, all_nodes], names=['year', 'node']).to_frame(index=False)
merged_df = pd.merge(all_combinations, combined_df, on=['year', 'node'], how='left')
merged_df['count'] = merged_df['count'].fillna(0)
print(merged_df)

fig = px.bar(
    # combined_df,
    merged_df,
    x='node',
    y='count',
    color='year',
    barmode='group',
    title=f'Number of exceeded values aggregated by {period}',
    labels={'count': 'Count', 'node': 'Node'},
    text='count'
)
fig.update_traces(marker=dict(line=dict(color='grey', width=2)))

fig.update_layout(
    legend_title='Year',
    xaxis_title='Location',
    yaxis_title='Count',
    bargap=0.2,
    bargroupgap=0.15,
    template='plotly_white',
    legend=dict(traceorder='normal'),
    xaxis=dict(categoryorder='array', categoryarray=sorted(combined_df['year'].unique()))
)
output_file = os.path.join(product['plots'], 'summary.html')

fig.write_html(output_file)
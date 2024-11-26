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
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np
import plotly.graph_objects as go

csv_files = glob.glob(os.path.join(upstream['aggregate_nodes']['aggregated_nodes'], '*.csv'))
os.makedirs(product['profiles'], exist_ok=True)
param1 = 'temperature'
param2 = 'pm_2.5'


def calc_params(df, param1, param2):
    """

    :param df: df after aggregation
    :param param1: x
    :param param2: y
    :return:    a =  x^2
                b = x
                c = Intercept
    """

    x = df[param1].values.reshape(-1, 1)
    y = df[param2].values
    x_quad = np.hstack((x, x ** 2))
    model = LinearRegression()
    model.fit(x_quad, y)
    a, b = model.coef_[1], model.coef_[0]
    c = model.intercept_

    y_pred_quadratic = a * df[param1] ** 2 + b * df[param1] + c
    r2_quadratic = r2_score(y, y_pred_quadratic)

    return a, b, c, r2_quadratic


def plot_correlation(df, param_x, param_y, a, b, c):
    """
    :param df: df after aggregation
    :param param1: x
    :param param2: y
    :param a:  x^2
    :param b:  x
    :param c:  intercept
    :return:
            figure with param1 and param2 profile with quadratic correlation line
    """
    x = df[param_x]
    y = df[param_y]

    linear_model = LinearRegression()
    x_regg = df[param_x].values.reshape(-1, 1)
    linear_model.fit(x_regg, y)
    y_pred_quadratic = a * x ** 2 + b * x + c

    r2_quadratic = r2_score(y, y_pred_quadratic)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data Points', marker=dict(color='blue')))

    fig.add_trace(
        go.Scatter(x=x, y=y_pred_quadratic, mode='lines', name='Quadratic Regression', line=dict(color='green')))

    fig.update_layout(
        title="Scatter Plot with Quadratic Regression",
        xaxis_title=param_x,
        yaxis_title=param_y,
        showlegend=True
    )
    fig.add_annotation(
        x=0.5, y=0.95,
        xref="paper", yref="paper",
        text=f"R² = {r2_quadratic:.4f}",
        showarrow=False,
        font=dict(size=16, color="black"),
        align="center"
    )
    return fig


result_df = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(file)
    file_name = os.path.basename(file)
    output_file = os.path.join(product['profiles'], os.path.splitext(file_name)[0])
    node_name = file_name.split('_')[1].split('.')[0]
    df_cleaned = df.dropna()

    a, b, c, r2 = calc_params(df_cleaned, param1, param2)
    temp_df = pd.DataFrame({"node_name": [node_name], "x^2": [a], "x": [b], "intercept": [c], 'R2': [r2]})
    result_df = pd.concat([result_df, temp_df], ignore_index=True)

    fig = plot_correlation(df_cleaned, param1, param2, a, b, c)
    output_file_plot = os.path.join(product['profiles'], f'correlation_profiles_{node_name}.html')
    fig.write_html(output_file_plot)

print(result_df)
output_file = os.path.join(product['profiles'], 'correlation_profiles.csv')
result_df.to_csv(output_file, index=False)

# + tags=["parameters"]
upstream = ['filter_data']
product = None
k_count = None

# -

import pandas as pd
import numpy as np
import os
import glob
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import pdist, squareform

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data']['filtered_data'], '*.csv'))[0])
df = df.transpose()
numpy_array = df.to_numpy()

dist_matrix = squareform(pdist(numpy_array, metric='euclidean'))
dist_matrix = pd.DataFrame(dist_matrix, index=df.index, columns=df.index)

node_names = dist_matrix.iloc[0]
node_names = node_names.index

k = k_count

nearest_neighbors_distances = np.sort(dist_matrix, axis=1)[:, 1:k+1]
nearest_neighbors_distances_df = pd.DataFrame(nearest_neighbors_distances)

df_mean = nearest_neighbors_distances_df.mean(axis=1)

df = pd.DataFrame({'Nodes': node_names})
df['Row_Mean'] = df_mean

os.makedirs(product['calculated_kNN'], exist_ok=True)
output_file_name = 'kNN.csv'
df.to_csv(os.path.join(product['calculated_kNN'], output_file_name), index=False)
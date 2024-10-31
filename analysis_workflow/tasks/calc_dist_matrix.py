# + tags=["parameters"]
upstream = ['filter_data']
product = None
dist_matrix_type = None

# -

from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import pairwise
import pandas as pd
import os
import glob

def calculate_distance_matrix(numpy_array, dist_matrix_type, df) -> pd.DataFrame:
    if dist_matrix_type in ['cityblock', 'euclidean']:
        dist_matrix = squareform(pdist(numpy_array, metric=dist_matrix_type))
    elif dist_matrix_type == 'cosine':
        cos_sim_matrix = pairwise.cosine_similarity(df)
        dist_matrix = 1 - pd.DataFrame(cos_sim_matrix, index=df.index, columns=df.index)
        dist_matrix.values[range(len(dist_matrix)), range(len(dist_matrix))] = 0

    return dist_matrix

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data']['filtered_data'], '*.csv'))[0])
df = df.transpose()
numpy_array = df.to_numpy()

dist_matrix = calculate_distance_matrix(numpy_array, dist_matrix_type, df)
dist_matrix = pd.DataFrame(dist_matrix, index=df.index, columns=df.index)

os.makedirs(product['calculated_dist_matrix'], exist_ok=True)
output_file_name = 'distance_matrix.csv'
dist_matrix.to_csv(os.path.join(product['calculated_dist_matrix'], output_file_name), index=False)
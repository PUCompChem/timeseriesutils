# + tags=["parameters"]
upstream = ['filter_data']
product = None
dist_matrix_type = None
clusters = None
method = None

# -

import pandas as pd
import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.cluster import KMeans

def find_threshold_for_n_clusters(Z, num_clusters) -> np.float64:
    distances = Z[:, 2]
    max_distance = distances.max()

    for threshold in np.linspace(0, max_distance, 1000):
        clusters = fcluster(Z, t=threshold, criterion='distance')
        if len(np.unique(clusters)) == num_clusters:
            return threshold
        
    return max_distance

def clusters_by_elbow(features) -> int:
    cluster_range = range(2, 21)
    inertia_values = []

    for n_clusters in cluster_range:
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(features)
        inertia_values.append(kmeans.inertia_)

    first_derivative = np.diff(inertia_values)
    second_derivative = np.diff(first_derivative)
    elbow_index = np.argmin(second_derivative)
    optimal_clusters = cluster_range[elbow_index]

    return optimal_clusters

def clusters_by_silhouette(features) -> int:
    silhouette_scores = []
    cluster_range = range(2, 21)

    for n_clusters in cluster_range:
        agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
        cluster_labels = agglomerative.fit_predict(features)

        silhouette_avg = silhouette_score(features, cluster_labels)
        silhouette_scores.append(silhouette_avg)
        
    max_index = np.argmax(silhouette_scores)
    optimal_clusters = cluster_range[max_index]

    return optimal_clusters

df = pd.read_csv(glob.glob(os.path.join(upstream['filter_data']['filtered_data'], '*.csv'))[0])

labels = df.columns.tolist()
features = df.transpose()

distance_matrix = pdist(features, metric=dist_matrix_type)
linked = linkage(distance_matrix, method=method)

if clusters == 'elbow':
    num_clusters = clusters_by_elbow(features)
elif clusters == 'silhouette':
    num_clusters = clusters_by_silhouette(features)
elif isinstance(clusters, int) and 2 <= clusters <= 20:
    num_clusters = clusters
else:
    raise ValueError("Invalid value for 'clusters'. Must be 'elbow', 'silhouette', or an integer between 2 and 20.")

cluster_labels = fcluster(linked, num_clusters, criterion='maxclust')

silhouette_avg = silhouette_score(features, cluster_labels, metric=dist_matrix_type)
davies_bouldin_avg = davies_bouldin_score(features, cluster_labels)
calinski_harabasz_avg = calinski_harabasz_score(features, cluster_labels)

threshold = find_threshold_for_n_clusters(linked, num_clusters)

fig, ax = plt.subplots(figsize=(16, 9))
dendrogram(
    linked,
    labels=labels,
    color_threshold=threshold - 0.1,
    above_threshold_color='black',
    orientation='top',
    show_contracted=True,
    leaf_font_size=6
)

ax.set_title('Hierarchical Clustering Dendrogram')
ax.set_xlabel('Material')
ax.set_ylabel('Distance')
ax.tick_params(axis='y', rotation=0, labelsize=8)
plt.tight_layout()

textstr = '\n'.join((
    f'Silhouette Score: {silhouette_avg:.4f}',
    f'Davies-Bouldin Score: {davies_bouldin_avg:.4f}',
    f'Calinski-Harabasz Score: {calinski_harabasz_avg:.4f}'
))

ax.text(
    0.98, 0.96, textstr, transform=ax.transAxes, 
    fontsize=12, verticalalignment='top',
    horizontalalignment='right', 
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
)

os.makedirs(product['generated_clusters'], exist_ok=True)

df_linkage = pd.DataFrame(linked, columns=['Cluster 1', 'Cluster 2', 'Distance', 'Cluster Size'])
output_file_name = 'clusters.csv'
df_linkage.to_csv(os.path.join(product['generated_clusters'], output_file_name), index=False)

output_file_name = 'cluster_dendrogram.png'
fig.savefig(os.path.join(product['generated_clusters'], output_file_name), bbox_inches='tight')
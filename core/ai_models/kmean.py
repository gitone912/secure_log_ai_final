import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score, precision_score, recall_score
from data_prep import process_logs




def plot_kmeans_clusters(logs_df, save_path='k-mean_charts/kmeans_clusters_3d.jpg'):
    features = ['encoded_refers', 'encoded_user-agent', 'encoded_status', 'encoded_method']

    # Create and train the K-means clustering model
    kmeans = KMeans(n_clusters=2, random_state=42)
    logs_df['cluster'] = kmeans.fit_predict(logs_df[features])

    # Identify anomalies based on cluster membership
    anomaly_cluster = logs_df['cluster'].value_counts().idxmin()
    logs_df['anomaly_kmeans'] = logs_df['cluster'] == anomaly_cluster

    # Visualize K-means clusters in 3D (example assumes 3 clusters)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    colors = ['blue', 'green', 'red']

    for cluster, color in zip(range(2), colors):
        cluster_data = logs_df[logs_df['cluster'] == cluster]
        ax.scatter(cluster_data['encoded_refers'], cluster_data['encoded_user-agent'], cluster_data['encoded_status'],
                c=color, label=f'Cluster {cluster}')

    ax.set_xlabel('Encoded Refers')
    ax.set_ylabel('Encoded User-Agent')
    ax.set_zlabel('Encoded Status')
    ax.set_title('K-means Clustering')
    ax.legend()

    # Save the plot
    plt.savefig(save_path)
    plt.close()

# # Example usage
# logs_df = process_logs('access.log', percentage=0.001)
# plot_kmeans_clusters(logs_df)

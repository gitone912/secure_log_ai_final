from sklearn.ensemble import IsolationForest
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from .data_prep import process_logs
import matplotlib.pyplot as plt

def train_isolation_forest(logs_df, features, contamination=0.05, random_state=42):
    # Prepare data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(logs_df[features])

    # Train Isolation Forest model
    isolation_model = IsolationForest(contamination=contamination, random_state=random_state)
    isolation_model.fit(scaled_data)

    # Obtain anomaly scores
    isolation_scores = isolation_model.decision_function(scaled_data)

    return isolation_scores, scaler, isolation_model

def evaluate_anomaly_detection(isolation_scores, true_labels):
    # Convert anomaly scores to binary labels (anomaly or not)
    predicted_labels = (isolation_scores < 0).astype(int)

    # Calculate and print evaluation metrics
    accuracy = accuracy_score(true_labels, predicted_labels)
    precision = precision_score(true_labels, predicted_labels)
    recall = recall_score(true_labels, predicted_labels)

    print(f'Accuracy: {accuracy:.4f}')
    print(f'Precision: {precision:.4f}')
    print(f'Recall: {recall:.4f}')

    return accuracy, precision, recall

import os

def plot_anomaly_detection_with_pie(isolation_scores, save_path_scatter='/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/isolation_charts/anomaly_detection_scatter.jpg', save_path_pie='/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/isolation_charts/anomaly_detection_pie.jpg'):
    # Check if the files already exist
    if os.path.exists(save_path_scatter):
        os.remove(save_path_scatter)
    if os.path.exists(save_path_pie):
        os.remove(save_path_pie)

    # Scatter plot
    plt.figure(figsize=(12, 6))
    plt.scatter(range(len(isolation_scores)), isolation_scores, c=isolation_scores, cmap='coolwarm')
    plt.title('Isolation Forest Anomaly Detection')
    plt.xlabel('Data Points')
    plt.ylabel('Isolation Forest Anomaly Score')
    plt.savefig(save_path_scatter)
    plt.close()

    # Pie chart
    plt.figure(figsize=(8, 8))
    labels = ['Normal', 'Anomaly']
    sizes = [len(isolation_scores) - sum(isolation_scores < 0), sum(isolation_scores < 0)]
    colors = ['lightblue', 'lightcoral']
    explode = (0, 0.1)  # explode 2nd slice
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode)
    plt.title('Data Distribution')
    plt.savefig(save_path_pie)
    plt.close()







def save_anomaly_logs(logs_df, isolation_scores, threshold=0.2):
    # Save logs with anomaly scores below the threshold
    anomaly_indices = isolation_scores < threshold
    anomaly_logs = logs_df[anomaly_indices]

    # Save to a text file
    anomaly_logs.to_csv('/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/text_files/anomaly_logs.txt', index=False)

# Example usage
# logs_df = process_logs('access.log', percentage=0.001)
# features = ['encoded_refers', 'encoded_user-agent', 'encoded_status', 'encoded_method']

# isolation_scores, scaler, isolation_model = train_isolation_forest(logs_df, features)
# evaluate_anomaly_detection(isolation_scores, (isolation_scores < 0).astype(int))
# # Example usage
# plot_anomaly_detection_with_pie(isolation_scores)
# save_anomaly_logs(logs_df, isolation_scores, threshold=0)

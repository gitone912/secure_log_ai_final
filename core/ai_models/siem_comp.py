import matplotlib.pyplot as plt
from .data_prep import process_logs
def save_status_distribution_bar_chart(logs_df):
    save_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/status_distribution_bar.jpg'
    status_counts = logs_df['status'].value_counts()
    plt.bar(status_counts.index, status_counts.values)
    plt.xlabel('Status Codes')
    plt.ylabel('Count')
    plt.title('Distribution of Status Codes')
    plt.savefig(save_path)
    plt.close()

# Example usage:

def save_traffic_label_distribution_pie_chart(logs_df):
    save_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/traffic_label_distribution_pie.jpg'
    traffic_label_counts = logs_df['traffic-label'].value_counts()
    plt.pie(traffic_label_counts, labels=traffic_label_counts.index, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Distribution of Traffic Labels')
    plt.savefig(save_path)
    plt.close()

# Example usage:

def save_requests_over_time_time_series_plot(logs_df):
    save_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/requests_over_time_time_series.jpg'
    requests_over_time = logs_df.groupby('datetime').size()
    requests_over_time.plot()
    plt.xlabel('Time')
    plt.ylabel('Number of Requests')
    plt.title('Requests Over Time')
    plt.savefig(save_path)
    plt.close()

# Example usage:

import seaborn as sns

def save_size_by_traffic_label_box_plot(logs_df):
    save_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/size_by_traffic_label_box.jpg'
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='traffic-label', y='size', data=logs_df)
    plt.xlabel('Traffic Label')
    plt.ylabel('Size of Requests')
    plt.title('Size of Requests by Traffic Label')
    plt.savefig(save_path)
    plt.close()

# Example usage:

def save_size_vs_status_scatter_plot(logs_df):
    save_path = '/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/size_vs_status_scatter.jpg'
    plt.scatter(logs_df['size'], logs_df['status'])
    plt.xlabel('Size of Requests')
    plt.ylabel('Status Code')
    plt.title('Size vs. Status Code')
    plt.savefig(save_path)
    plt.close()

# Example usage:
# logs_df = process_logs('access.log', percentage=0.001)
# save_size_vs_status_scatter_plot(logs_df)
# save_status_distribution_bar_chart(logs_df)
# save_traffic_label_distribution_pie_chart(logs_df)
# save_requests_over_time_time_series_plot(logs_df)
# save_size_by_traffic_label_box_plot(logs_df)
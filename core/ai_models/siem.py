import matplotlib.pyplot as plt
from .data_prep import process_logs

def save_status_distribution_chart(logs_df, save_path='/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/status_distribution.jpg'):
    status_counts = logs_df['status'].value_counts()
    plt.bar(status_counts.index, status_counts.values)
    plt.xlabel('Status Codes')
    plt.ylabel('Count')
    plt.title('Distribution of Status Codes')
    plt.savefig(save_path)
    plt.close()

def save_method_distribution_chart(logs_df, save_path='/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/method_distribution.jpg'):
    method_counts = logs_df['method'].value_counts()
    plt.bar(method_counts.index, method_counts.values)
    plt.xlabel('HTTP Methods')
    plt.ylabel('Count')
    plt.title('Distribution of HTTP Methods')
    plt.savefig(save_path)
    plt.close()

def save_user_agent_distribution_chart(logs_df, save_path='/Users/pranaymishra/Desktop/CU/secure_log_ai/core/static/charts/user_agent_distribution.jpg'):
    user_agent_counts = logs_df['user_agent'].value_counts().head(10)
    plt.bar(user_agent_counts.index, user_agent_counts.values)
    plt.xlabel('User Agents')
    plt.ylabel('Count')
    plt.title('Top User Agents Distribution')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

# Example usage:
# logs_df = process_logs('access.log', percentage=0.001)
# save_status_distribution_chart(logs_df, 'charts/status_distribution.jpg')
# save_method_distribution_chart(logs_df, 'charts/method_distribution.jpg')
# save_user_agent_distribution_chart(logs_df, 'charts/user_agent_distribution.jpg')

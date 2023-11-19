from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from data_prep import logs_to_df

logs_df = logs_to_df('../new_file.log')
features = [
    'encoded_refers', 'encoded_user-agent', 'encoded_status', 'encoded_method'
]
scaler = StandardScaler()
scaled_data = scaler.fit_transform(logs_df[features])

isolation_model = IsolationForest(contamination=0.05, random_state=42)
isolation_model.fit(scaled_data)

import matplotlib.pyplot as plt
isolation_scores = isolation_model.decision_function(scaled_data)


plt.figure(figsize=(12, 6))
plt.scatter(range(len(scaled_data)), isolation_scores, c=isolation_scores, cmap='coolwarm')
plt.title('Isolation Forest Anomaly Detection')
plt.xlabel('Data Points')
plt.ylabel('Isolation Forest Anomaly Score')
plt.show()
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from sklearn.neural_network import MLPRegressor

# # Features for the model
# features = ['encoded_refers', 'encoded_user-agent', 'encoded_status', 'encoded_method']

# # Standardize the data
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(logs_df[features])

# # Split the data into training and testing sets
# X_train, X_test = train_test_split(scaled_data, test_size=0.2, random_state=42)

# # Build the autoencoder model
# autoencoder = MLPRegressor(hidden_layer_sizes=(10,), activation='relu', solver='adam', random_state=42)
# autoencoder.fit(X_train, X_train)

# # Reconstruct the data and calculate reconstruction error
# reconstructed_data = autoencoder.predict(X_test)
# mse = ((X_test - reconstructed_data) ** 2).mean(axis=1)

# # Set a threshold for anomaly detection (adjust as needed)
# threshold = 0.1

# # Assuming 'logs_df' is your DataFrame
# logs_df['anomaly_autoencoder'] = mse > threshold

# # Check for missing values in 'logs_df' or 'mse'
# print("Missing values in logs_df:", logs_df.isnull().sum())
# print("Missing values in mse:", np.isnan(mse).sum())

# # Evaluate the Autoencoder model
# print(classification_report(logs_df['traffic-label'], logs_df['anomaly_autoencoder']))